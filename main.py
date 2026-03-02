import pygame
import sys
from personaje import Personaje

#Inicio de Pygame
pygame.init()

#tamaño de ventana
ANCHO_VENTANA = 600
ALTO_VENTANA = 400

fps=pygame.time.Clock()

#redimencionar la ventana del programa
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
def menu():
    pygame.display.set_caption("Escapa del Laberinto")
    boton_play = pygame.Rect(300,200,200,60)
    letras_fuente = pygame.font.Font(None, 30)

    #para hacer que la ventana se cierre
    run = True

    while run:
        ventana.fill((0, 0, 0))
        pygame.draw.rect(ventana, (0, 0, 255), boton_play)
        text_play = letras_fuente.render("vamo a juga", True, (0, 255, 0))
        ventana.blit(text_play, (boton_play.x + 10, boton_play.y + 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_play.collidepoint(event.pos):
                    run = False
                    jugar()

def jugar():
    run = True
    jugador = Personaje()
    while run:
        fps.tick(30)
        ventana.fill((255, 0, 0))
        jugador.dibujar(ventana)
        pygame.display.flip()
      
        for event in pygame.event.get():
            jugador.mover(pygame.key.get_pressed()) 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return
            
menu()