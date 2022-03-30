import pygame
import sys

from utils import *
from ui import *

class Main():
    def __init__(self):
        pygame.init()
        # Declarar fuentes
        self.bigFont = pygame.font.SysFont("arial",25)
        self.smallFont = pygame.font.SysFont("arial",18)

        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Buscaminas")

        self.screen.fill(BACKGROUND)
        self.cursor = Cursor()  
        clock = pygame.time.Clock()

        self.btnHeaderSettings, self.textNumMines = self.headerDesign() 
        self.numMines=15

        openInterface = True
        while openInterface:
            clock.tick(60)
            
            self.cursor.update() 
            self.btnHeaderSettings.update(self.screen,self.cursor)
            self.textNumMines.update(str(self.numMines).rjust(2, '0')) ##Posibilidad de mover el 2 al redondear el numero de bombas que se tiene
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.cursor.colliderect(self.btnHeaderSettings.getRect()):
                        print("click")
                        self.numMines-=1
            
            pygame.display.flip()
        

    def headerDesign(self):
        pygame.draw.rect(self.screen,HEADER,(0,0,WIDTH,SIZE_HEADER))

        #Numero de bombas
        imgMines = pygame.image.load("images/mina.png")
        pictureMines = pygame.transform.scale(imgMines,[40,40])
        self.screen.blit(pictureMines,[0,0])
        
        textNumMines = Text(self.screen,str(self.numMines),40,5,self.bigFont) 
        btnSettings = Button(self.screen,"Opciones",WIDTH-110,7,self.smallFont)
        
        return btnSettings,textNumMines


if __name__ == "__main__":
    Main()