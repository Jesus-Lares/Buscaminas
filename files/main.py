import pygame
import sys

from utils import *
from ui import *
from board import Board

numRows = MEASURES["normal"]["mines"]
numCols = MEASURES["normal"]["mines"]

class Main():
    def __init__(self):
        pygame.init()
        # Declarar fuentes
        self.bigFont = pygame.font.SysFont("arial",25)
        self.smallFont = pygame.font.SysFont("arial",18)
        pygame.display.set_caption("Buscaminas")
        clock = pygame.time.Clock()
        self.width,self.height,mines=MEASURES["normal"].values()

        self.init_design(mines,numRows,numCols)
        
        openInterface = True
        self.playing = True
        self.win = True
        while openInterface:
            clock.tick(60)

            self.cursor.update() 
            self.btnHeaderSettings.update(self.screen,self.cursor)
            self.textNumMines.update(str(self.numMines).rjust(2, '0')) ##Posibilidad de mover el 2 al redondear el numero de bombas que se tiene
                

            for event in pygame.event.get():
                self.btns_playing(event)
                    
                if event.type == pygame.QUIT:
                    sys.exit()

            if(self.playing):
                self.board.print_board(self.screen)
                self.end_game()
                

            else:
                if self.win:
                    size = self.bigFont.size("GANASTE")
                    texto = self.bigFont.render("GANASTE", 1, GREEN)
                    self.screen.blit(texto, ((self.width/ 2) - (size[0] / 2), (self.height / 2) - (size[1] / 2)))
                else:
                    self.board.open_all_mines(self.screen)
                    size = self.bigFont.size("PERDISTE")
                    texto = self.bigFont.render("PERDISTE", 1, RED)
                    self.screen.blit(texto, ((self.width / 2) - (size[0] / 2), (self.height / 2) - (size[1] / 2))) 

            pygame.display.flip()
        
    def init_design(self,mines,rows,cols):
        self.screen = pygame.display.set_mode((self.width,self.height))

        self.screen.fill(BACKGROUND)
        self.cursor = Cursor()  

        self.numMines=mines 
        self.numRows = rows
        self.numCols = cols
        #Creacion de la cabecera
        self.btnHeaderSettings, self.textNumMines = self.headerDesign() 
        #Creacion del tablero
        self.board = Board(self.numRows, self.numCols, self.numMines, self.width,self.height-SIZE_HEADER)

    def headerDesign(self):
        pygame.draw.rect(self.screen,HEADER,(0,0,self.width,SIZE_HEADER))
        #Numero de bombas
        imgMines = pygame.image.load("images/mina.png")
        pictureMines = pygame.transform.scale(imgMines,[40,40])
        self.screen.blit(pictureMines,[0,0])
        
        textNumMines = Text(self.screen,str(self.numMines),40,5,self.bigFont) 
        btnSettings = Button(self.screen,"Opciones",self.width-110,7,self.smallFont)
        
        return btnSettings,textNumMines

    def btns_playing(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = self.cursor.get_pos()
            if event.button == 1:
                self.board.mouse_button_left_down(position[0],position[1])
            elif event.button==3:
                self.numMines += self.board.mouse_button_right_down(position[0],position[1],self.numMines)

        elif event.type == pygame.MOUSEMOTION:
            position = self.cursor.get_pos()
            self.board.mouse_motion_board(position[0],position[1])  
        
        #Evento para cuando dejas de presionar el boton izquierdo
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                position = self.cursor.get_pos()
                if self.cursor.colliderect(self.btnHeaderSettings.getRect()):
                    self.numMines-=1
                    self.width,self.height,mines=MEASURES["easy"].values()
                    self.init_design(mines,10,10)
                self.playing = self.board.mouse_button_left_up(position[0],position[1])
            
    def end_game(self):
        if self.numMines==0:
            if self.board.compare_mines():
                self.playing=False 
                self.win = True    
        if self.board.get_box_close() == self.board.get_num_bombs():
            self.playing=False 
            self.win = True

if __name__ == "__main__":
    Main()