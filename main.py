import pygame
import sys
from personaje import Personaje
from enemigo import Enemigo
import mapa

pygame.init()

TILE = 20
ANCHO_VENTANA = 600
ALTO_VENTANA = 400

fps = pygame.time.Clock()

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)

# Generar laberinto inicial
laberinto, filas, columnas = mapa.generar_mapas(ANCHO_VENTANA, ALTO_VENTANA)


#salida
salida_rect = pygame.Rect(60,60,TILE,TILE)


def dibujar_laberinto(ventana, laberinto):

    for y, fila in enumerate(laberinto):

        for x, tile in enumerate(fila):

            if tile == 1:

                pygame.draw.rect(
                    ventana,
                    (0,0,0),
                    pygame.Rect(x*TILE, y*TILE, TILE, TILE)
                )

    #salida dibujo
    pygame.draw.rect(ventana,(0,255,0),salida_rect)


def colision(nuevo_rect):

    for y, fila in enumerate(laberinto):

        for x, tile in enumerate(fila):

            if tile == 1:

                pared_rect = pygame.Rect(x*TILE, y*TILE, TILE, TILE)

                if nuevo_rect.colliderect(pared_rect):

                    return True

    return False


def mover_jugador(jugador, teclas):

    dx = 0
    dy = 0

    velocidad = 4

    if teclas[pygame.K_w]:
        dy = -velocidad

    if teclas[pygame.K_s]:
        dy = velocidad

    if teclas[pygame.K_a]:
        dx = -velocidad

    if teclas[pygame.K_d]:
        dx = velocidad


    nuevo_rect = jugador.rect.move(dx,0)

    if not colision(nuevo_rect):
        jugador.rect.x += dx


    nuevo_rect = jugador.rect.move(0,dy)

    if not colision(nuevo_rect):
        jugador.rect.y += dy


def regenerar_laberinto(nuevo_ancho, nuevo_alto):

    global laberinto, filas, columnas

    laberinto, filas, columnas = mapa.generar_mapas(nuevo_ancho, nuevo_alto)


#menu de perdiste
def menu_game_over():

    fuente_grande = pygame.font.Font(None,70)
    fuente = pygame.font.Font(None,40)

    boton_retry = pygame.Rect(200,200,200,60)
    boton_salir = pygame.Rect(200,280,200,60)

    while True:

        ventana.fill((30,30,30))

        texto = fuente_grande.render("PERDISTE a",True,(255,0,0))
        ventana.blit(texto,(170,120))

        pygame.draw.rect(ventana,(0,200,0),boton_retry)
        pygame.draw.rect(ventana,(200,0,0),boton_salir)

        ventana.blit(fuente.render("REINTENTAR",True,(255,255,255)),(235,215))
        ventana.blit(fuente.render("SALIR",True,(255,255,255)),(270,295))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if boton_retry.collidepoint(event.pos):
                    jugar()

                if boton_salir.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


#ganaste configuracion
def menu_ganaste():

    fuente_grande = pygame.font.Font(None,70)
    fuente = pygame.font.Font(None,40)

    boton_retry = pygame.Rect(200,200,200,60)
    boton_salir = pygame.Rect(200,280,200,60)

    while True:

        ventana.fill((20,60,20))

        texto = fuente_grande.render("¡GANASTE!",True,(0,255,0))
        ventana.blit(texto,(180,120))

        pygame.draw.rect(ventana,(0,200,0),boton_retry)
        pygame.draw.rect(ventana,(200,0,0),boton_salir)

        ventana.blit(fuente.render("REINTENTAR",True,(255,255,255)),(235,215))
        ventana.blit(fuente.render("SALIR",True,(255,255,255)),(270,295))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if boton_retry.collidepoint(event.pos):
                    jugar()

                if boton_salir.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


#menu inicial
def menu():

    pygame.display.set_caption("Escapa del Laberinto")

    boton_play = pygame.Rect(200,150,200,60)

    fuente = pygame.font.Font(None,40)

    while True:

        ventana.fill((255,255,255))

        pygame.draw.rect(ventana,(0,0,255),boton_play)

        texto = fuente.render("JUGAR",True,(255,255,255))

        ventana.blit(texto,(255,165))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if boton_play.collidepoint(event.pos):
                    jugar()


#juego
def jugar():

    global ventana

    jugador = Personaje()

    enemigo = Enemigo(60,60,jugador, laberinto)

    run = True

#Cargamos la musica
    pygame.mixer.music.load("laberinto.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    while run:

        fps.tick(60)

        ventana.fill((200,200,200))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:

                ventana = pygame.display.set_mode(event.size, pygame.RESIZABLE)

                regenerar_laberinto(event.w,event.h)

                enemigo.actualizar_laberinto(laberinto)

                jugador.rect.clamp_ip(pygame.Rect(0,0,event.w,event.h))
                enemigo.rect.clamp_ip(pygame.Rect(0,0,event.w,event.h))


        teclas = pygame.key.get_pressed()

        mover_jugador(jugador,teclas)

        enemigo.actualizar()


        #ganaste 
        if jugador.rect.colliderect(salida_rect):
            
            pygame.mixer.music.stop()

            pygame.time.delay(500)

            menu_ganaste()

            run = False


        #game over mi loco
        if jugador.muerto:

            pygame.mixer.music.stop()

            pygame.time.delay(500)

            menu_game_over()

            run = False


        dibujar_laberinto(ventana,laberinto)

        jugador.dibujar(ventana)

        enemigo.dibujar(ventana)

        pygame.display.flip()


menu()