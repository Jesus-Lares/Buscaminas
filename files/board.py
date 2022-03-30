import pygame
import random
import sys

from box import Box
from utils import SIZE_HEADER 


class Board:
    def __init__(self, rows, columns, mines, width, height):
        self.width = int(width/rows)
        self.height = int(height/columns)
        
        self.pushed = False
        self.rows = rows #Numero de filas eje x
        self.columns = columns #Numero de columnas eje y
        self.x0 = self.y0 = 0
        self.xx = self.yy = 0
        
        self.hide_mines = [] # Matriz 1xN
        self.board   = [] # Matriz MxN
        self.boxes = [] # Matriz 1xN
        
        self.create_table_board()
        self.lay_mines(mines)
        self.place_clues()

        # Crea el arreglo de las casillas en "SIN MARCAR" con el valor de tabla
        color=False
        for y in range(columns):  #10
            color = not color
            for x in range(rows): #10
                self.boxes.append(Box(x*self.width, y*self.height+SIZE_HEADER, self.width-1, self.height-1,  1, str(self.board[x][y]),color))
                color = not color
       
    #Crea una matriz con las filas y columnas y valor que le pasemos
    def create_table_board(self):
        for i in range(self.rows):
            self.board.append([])
            for j in range(self.columns):
                self.board[i].append(0)

    #Coloca en el tablero el numero que le pasemos de minas
    def lay_mines(self,mines):
        num=0
        while num<mines:
            y=random.randint(0,self.rows-1)
            x=random.randint(0,self.columns-1)
            if self.board[y][x] != 9:
                self.board[y][x]=9
                num+=1
                self.hide_mines.append((y,x))

    #Coloca las pistas par el juego del buscaminas
    def place_clues(self):
        for y in range(self.rows):
            for x in range(self.columns):
                if self.board[y][x]==9:
                    for i in [-1,0,1]:
                        for j in [-1,0,1]:
                            if 0 <= y+i <= self.rows-1 and 0 <= x+j <= self.columns-1:
                                if self.board[y+i][x+j] != 9:
                                    self.board[y+i][x+j]+=1

    def get_box_close(self):
        retorno = 0
        for c in range(self.rows * self.columns):
            if self.boxes[c].get_status() != 3: retorno = retorno + 1
        return retorno

    def get_num_bombs(self):
        retorno = 0
        for y in range(self.columns):
            for x in range(self.rows):
                if self.board[x][y] == 9: retorno += 1
        return retorno


    #Abrir casillas
    def open_box(self, x, y):
        playing = False
        self.boxes[y*self.rows+x].set_status(3)
        if self.board[x][y] != 9:
            playing = True
            if self.board[x][y] == int('0'):
                for j in range(-1, 2):
                    for i in range(-1, 2):
                        if (x + j >= 0) and (x + j < self.rows) and (y + i >= 0) and (y + i < self.columns) :
                            if (self.boxes[(y+i)*self.rows+x+j].get_status() != 3):
                                self.open_box(x+j, y+i)
        return playing
    
    #Imprime las casillas
    def print_board(self, screen):
        for y in range(self.columns):
            for x in range(self.rows):
                self.boxes[y*self.rows+x].draw_box(screen)

    def play(self, screen):
        playing = True
        for event in pygame.event.get():
            #Evento para cuando presionas el boton izquierdo
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pushed = True
                position = pygame.mouse.get_pos()

                self.xx = self.x0 = int(position[0] // self.width)
                self.yy = self.y0 = int(position[1] // (self.height))-1
                
                if (self.boxes[self.yy* self.rows +self.xx].get_status() < 3):
                    self.boxes[self.yy* self.rows +self.xx].set_status(2)  
            #Evento para cuando mueves el mouse 
            elif event.type == pygame.MOUSEMOTION:
                position = pygame.mouse.get_pos()
                x = int(position[0] // self.width)
                y = int(position[1] // (self.height))-1
                if self.xx !=  x or self.yy != y:
                    if(x<self.rows and y< self.columns):
                        if self.boxes[self.yy*self.rows+self.xx].get_status() < 3:
                            self.boxes[self.yy*self.rows+self.xx].set_status(1)
                        if (self.boxes[y*self.rows+x].get_status() < 3):
                            self.boxes[y*self.rows+x].set_status(2)
                        self.xx = x
                        self.yy = y    
            
            #Evento para cuando dejas de presionar el boton izquierdo
            elif event.type == pygame.MOUSEBUTTONUP:
                self.pushed = False
                position = pygame.mouse.get_pos()

                x = int(position[0] // self.width)
                y = int(position[1] // (self.height))-1
                if(len(self.boxes)!= 0):
                    if self.x0 ==  x and self.y0 == y and self.boxes[y*self.rows+x].get_status() < 3:
                        playing = self.open_box(x, y) 
            elif event.type == pygame.QUIT:
                sys.exit()
        self.print_board(screen)
        return playing 