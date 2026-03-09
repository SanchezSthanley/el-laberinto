import pygame
import heapq
import random

TILE = 20

#arbol de comportamiento
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

#enemigo
class Enemigo:
    def __init__(self, x, y, jugador, laberinto):
        self.rect = pygame.Rect(x, y, TILE, TILE)
        self.jugador = jugador
        self.laberinto = laberinto
        self.camino = []
        self.timer = 0
        self.velocidad = 2
        self.crear_arbol()

    #A*
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
            if actual == destino: break
            for dx,dy in direcciones:
                vecino = (actual[0]+dx, actual[1]+dy)
                if 0 <= vecino[1] < len(self.laberinto) and 0 <= vecino[0] < len(self.laberinto[0]):
                    if self.laberinto[vecino[1]][vecino[0]] == 1: continue
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
            if actual is None: return []
        camino.reverse()
        return camino

    #lo que hace el enemigo
    def ver_jugador(self):
        dx = abs(self.rect.x - self.jugador.rect.x)
        dy = abs(self.rect.y - self.jugador.rect.y)
        return dx + dy < 200

    def atacar(self):
        dx = abs((self.rect.x // TILE) - (self.jugador.rect.x // TILE))
        dy = abs((self.rect.y // TILE) - (self.jugador.rect.y // TILE))
        if dx + dy <= 1:
            print("¡Enemigo ataca!")
            return True
        return False

    def perseguir(self):
        self.timer += 1
        if self.timer < self.velocidad:
            return False
        self.timer = 0
        inicio = (self.rect.x // TILE, self.rect.y // TILE)
        destino = (self.jugador.rect.x // TILE, self.jugador.rect.y // TILE)
        self.camino = self.a_star(inicio, destino)
        if self.camino:
            siguiente = self.camino.pop(0)

            # Movimiento solo si no colisiona
            nuevo_rect = pygame.Rect(siguiente[0]*TILE, siguiente[1]*TILE, TILE, TILE)
            if not self.colision(nuevo_rect):
                self.rect = nuevo_rect
            return True
        return False

    def patrullar(self):
        self.timer += 1
        if self.timer < self.velocidad: return True
        self.timer = 0
        direcciones = [(0,1),(1,0),(-1,0),(0,-1)]
        dx,dy = random.choice(direcciones)
        nuevo_rect = self.rect.move(dx*TILE, dy*TILE)
        if not self.colision(nuevo_rect):
            self.rect = nuevo_rect
        return True

    #control de la colision
    def colision(self, nuevo_rect):
        for y, fila in enumerate(self.laberinto):
            for x, tile in enumerate(fila):
                if tile == 1:
                    pared_rect = pygame.Rect(x*TILE, y*TILE, TILE, TILE)
                    if nuevo_rect.colliderect(pared_rect):
                        return True
        return False

    #arbol 
    def crear_arbol(self):
        root = Selector()
        root.agregar_hijo(Accion(self.atacar))  # Prioridad: atacar
        secuencia = Secuencia()
        secuencia.agregar_hijo(Accion(self.ver_jugador))
        secuencia.agregar_hijo(Accion(self.perseguir))
        root.agregar_hijo(secuencia)
        root.agregar_hijo(Accion(self.patrullar))
        self.arbol = root

    #update del arbol
    def actualizar(self):
        self.arbol.ejecutar()

    #dibujo del enemigo
    def dibujar(self, ventana):
        pygame.draw.rect(ventana,(0,0,255),self.rect)