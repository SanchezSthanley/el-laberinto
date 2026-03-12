import pygame

#definir posicion y tamaño de personaje
class Personaje():

#posicion del personaje
    def __init__(self):
        self.x = 560
        self.y = 360
        self.rect= pygame.Rect(self.x -20, self.y -15, 20, 15)
        self.muerto = False


#color del personaje
    def crear(self, interfaz):
        self.dibujar(interfaz) 

# Solo dibuja el jugador si no está muerto
    def dibujar(self, interfaz):
        if not self.muerto:  
            pygame.draw.rect(interfaz, (255, 0, 0), self.rect)

    def dibujar(self, interfaz):
      pygame.draw.rect(interfaz, (255, 0, 0), self.rect)
      

 #definicion de controles

    def mover(self, teclas):
        if not self.muerto:
            
            dx = 0
            dy = 0

            if teclas[pygame.K_w]: 
                dy = -1
                self.y -= 12
            elif teclas[pygame.K_s]:
                dy = 1
                self.y += 12
            elif teclas[pygame.K_a]:
                dx = -1
                self.x -= 12
            elif teclas[pygame.K_d]:
                dx = 1
                self.x += 12
            print(dy, dx)         
            self.rect.topleft = (self.x, self.y)