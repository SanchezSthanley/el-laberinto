import pygame

#definir posicion y tamaño de personaje
class Personaje():

#posicion del personaje
    def __init__(self):
        self.x = 300 
        self.y = 300
        self.rect= pygame.rect(self.x -20, self.y -15, 20, 15)


#color del personaje
    def dibujar(self, interfaz):
        self.draw(interfaz)
            #pygame.draw.rect(interfaz,(255, 255, 0), self.forma)     

         