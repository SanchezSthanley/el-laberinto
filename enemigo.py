import pygame
import heapq
import random

TILE = 20

# arbol de comportamiento
class Nodo:
    def __init__(self):
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def ejecutar(self):
        pass


class Selector(Nodo):
    def ejecutar(self):
        for hijo in self.hijos:
            if hijo.ejecutar():
                return True
        return False


class Secuencia(Nodo):
    def ejecutar(self):
        for hijo in self.hijos:
            if not hijo.ejecutar():
                return False
        return True


class Accion(Nodo):
    def __init__(self, accion):
        super().__init__()
        self.accion = accion

    def ejecutar(self):
        return self.accion()


# enemigo
class Enemigo:

    def __init__(self, x, y, jugador, laberinto):

        self.rect = pygame.Rect(x, y, TILE, TILE)
        self.jugador = jugador
        self.laberinto = laberinto
        self.camino = []
        self.timer = 0

        #velocidades
        self.velocidad_normal = 6
        self.velocidad_ataque = 2
        self.velocidad = self.velocidad_normal

        self.crear_arbol()
        self.jugador_muerto = False

    # actualizar laberinto
    def actualizar_laberinto(self, laberinto):
        self.laberinto = laberinto

    # A*
    def a_star(self, inicio, destino):

        def heuristica(a,b):
            return abs(a[0]-b[0]) + abs(a[1]-b[1])

        direcciones = [(0,1),(1,0),(0,-1),(-1,0)]
        frontera = []
        heapq.heappush(frontera,(0,inicio))
        vino_de = {inicio:None}
        costo = {inicio:0}

        while frontera:
            _, actual = heapq.heappop(frontera)
            if actual == destino:
                break

            for dx,dy in direcciones:
                vecino = (actual[0]+dx, actual[1]+dy)
                if not (0 <= vecino[0] < len(self.laberinto[0]) and 0 <= vecino[1] < len(self.laberinto)):
                    continue
                if self.laberinto[vecino[1]][vecino[0]] == 1:
                    continue
                nuevo_costo = costo[actual]+1
                if vecino not in costo or nuevo_costo < costo[vecino]:
                    costo[vecino] = nuevo_costo
                    prioridad = nuevo_costo + heuristica(destino,vecino)
                    heapq.heappush(frontera,(prioridad,vecino))
                    vino_de[vecino] = actual

        camino=[]
        actual=destino
        while actual != inicio:
            camino.append(actual)
            actual = vino_de.get(actual)
            if actual is None:
                return []
        camino.reverse()
        return camino

    #ver jugador usando tiles
    def ver_jugador(self):
        enemigo_x = self.rect.x // TILE
        enemigo_y = self.rect.y // TILE
        jugador_x = self.jugador.rect.centerx // TILE
        jugador_y = self.jugador.rect.centery // TILE

        dx = abs(enemigo_x - jugador_x)
        dy = abs(enemigo_y - jugador_y)

        if dx + dy <= 10:  # rango de detección en tiles
            self.velocidad = self.velocidad_ataque   # más rápido
            return True
        else:
            self.velocidad = self.velocidad_normal   # vuelve a normal
            return False

    # atacar
    def atacar(self):
        dx = abs((self.rect.x // TILE) - (self.jugador.rect.centerx // TILE))
        dy = abs((self.rect.y // TILE) - (self.jugador.rect.centery // TILE))
        if dx + dy <= 1:
            print("¡Enemigo ataca!")
            self.jugador.muerto = True
            self.jugador_muerto = True
            return True
        return False

    # perseguir
    def perseguir(self):
        self.timer += 1
        if self.timer < self.velocidad:
            return False
        self.timer = 0

        inicio = (self.rect.x // TILE, self.rect.y // TILE)
        destino = (self.jugador.rect.centerx // TILE, self.jugador.rect.centery // TILE)

        self.camino = self.a_star(inicio, destino)

        if self.camino:
            siguiente = self.camino.pop(0)
            tile_x = siguiente[0]
            tile_y = siguiente[1]

            if self.laberinto[tile_y][tile_x] == 0:
                # Mover enemigo
                self.rect.x = tile_x * TILE
                self.rect.y = tile_y * TILE
            return True
        return False

    # patrullar
    def patrullar(self):
        self.timer += 1
        if self.timer < self.velocidad:
            return True
        self.timer = 0

        direcciones = [(0,1),(1,0),(-1,0),(0,-1)]
        dx,dy = random.choice(direcciones)
        tile_x = (self.rect.x // TILE) + dx
        tile_y = (self.rect.y // TILE) + dy

        if 0 <= tile_x < len(self.laberinto[0]) and 0 <= tile_y < len(self.laberinto):
            if self.laberinto[tile_y][tile_x] == 0:
                self.rect.x = tile_x * TILE
                self.rect.y = tile_y * TILE
        return True

    # arbol
    def crear_arbol(self):
        root = Selector()
        root.agregar_hijo(Accion(self.atacar))

        secuencia = Secuencia()
        secuencia.agregar_hijo(Accion(self.ver_jugador))
        secuencia.agregar_hijo(Accion(self.perseguir))
        root.agregar_hijo(secuencia)

        root.agregar_hijo(Accion(self.patrullar))
        self.arbol = root

    # actualizar
    def actualizar(self):
        if not self.jugador_muerto:
            self.arbol.ejecutar()

    # dibujar
    def dibujar(self, ventana):
        # CAMBIO: color rojo si está en modo ataque
        if self.velocidad == self.velocidad_ataque:
            color = (255,0,0)
        else:
            color = (0,0,255)
        pygame.draw.rect(ventana,color,self.rect)