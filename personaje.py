import pygame

#definir posicion y tamaño de personaje
class Personaje():

#posicion del personaje
    def __init__(self):
        self.x = 300 
        self.y = 300
        self.rect= pygame.Rect(self.x -20, self.y -15, 20, 15)


#color del personaje
    def crear(self, interfaz):
        self.dibujar(interfaz) 

    def dibujar(self, interfaz):
      pygame.draw.rect(interfaz, (255, 255, 255), self.rect)
      

 #definicion de controles

    def mover(self, teclas):
        dx = 0
        dy = 0
        if teclas[pygame.K_w]: 
            dy = -1
            self.y -= 5
        elif teclas[pygame.K_s]:
            dy = 1
            self.y += 5
        elif teclas[pygame.K_a]:
            dx = -1
            self.x -= 5
        elif teclas[pygame.K_d]:
            dx = 1
            self.x += 5
        print(dy, dx)         
        self.rect.topleft = (self.x, self.y)