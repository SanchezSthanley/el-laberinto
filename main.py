import pygame
import sys
from personaje import Personaje
from enemigo import Enemigo
import mapa

# ===== CONFIG =====
pygame.init()
TILE = 20
ANCHO_VENTANA = 600
ALTO_VENTANA = 400
fps = pygame.time.Clock()

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)

# Generar laberinto inicial
laberinto, filas, columnas = mapa.generar_mapas(ANCHO_VENTANA, ALTO_VENTANA)

#funciones de la ventana dentro del juego color de los muros "si"
def dibujar_laberinto(ventana, laberinto):
    for y, fila in enumerate(laberinto):
        for x, tile in enumerate(fila):
            if tile == 1:
                pygame.draw.rect(ventana, (0,0,0), pygame.Rect(x*TILE, y*TILE, TILE, TILE))

def colision(nuevo_rect):
    for y, fila in enumerate(laberinto):
        for x, tile in enumerate(fila):
            if tile == 1:
                pared_rect = pygame.Rect(x*TILE, y*TILE, TILE, TILE)
                if nuevo_rect.colliderect(pared_rect):
                    return True
    return False

#movimiento y velocidad del jugador
def mover_jugador(jugador, teclas):
    dx = dy = 0
    if teclas[pygame.K_w]: dy = -10
    if teclas[pygame.K_s]: dy = 10
    if teclas[pygame.K_a]: dx = -10
    if teclas[pygame.K_d]: dx = 10

    nuevo_rect = jugador.rect.move(dx,0)
    if not colision(nuevo_rect): jugador.rect.x += dx

    nuevo_rect = jugador.rect.move(0,dy)
    if not colision(nuevo_rect): jugador.rect.y += dy

def regenerar_laberinto(nuevo_ancho, nuevo_alto):
    global laberinto, filas, columnas
    laberinto, filas, columnas = mapa.generar_mapas(nuevo_ancho, nuevo_alto)

#el menu de la ventana color y definicion del boton de inicio
def menu():
    pygame.display.set_caption("Escapa del Laberinto")
    boton_play = pygame.Rect(200,150,200,60)
    fuente = pygame.font.Font(None, 30)
    run = True
    while run:
        ventana.fill((255,255,255))
        pygame.draw.rect(ventana,(0,0,255),boton_play)
        text_play = fuente.render("vamo a juga", True, (0,255,0))
        ventana.blit(text_play,(boton_play.x+50, boton_play.y+15))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_play.collidepoint(event.pos):
                    run = False
                    jugar()

#control de la ventana del juego iniciado
def jugar():
    global ventana
    jugador = Personaje()
    enemigo = Enemigo(60,60,jugador, laberinto)
    enemigo.tile_w = TILE
    enemigo.tile_h = TILE
    run = True
    while run:
        fps.tick(15)
        ventana.fill((200,200,200))

        # Dibujar laberinto
        dibujar_laberinto(ventana, laberinto)

        # Mover jugador
        mover_jugador(jugador, pygame.key.get_pressed())

        # Actualizar enemigo
        enemigo.actualizar()

        # Dibujar jugador y enemigo
        jugador.dibujar(ventana)
        enemigo.dibujar(ventana)

        #poder serar la ventana y el programa
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                ventana = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                regenerar_laberinto(event.w, event.h)

                #Ajustar posiciones para que no queden fuera
                jugador.rect.clamp_ip(pygame.Rect(0,0,event.w,event.h))
                enemigo.rect.clamp_ip(pygame.Rect(0,0,event.w,event.h))

menu()