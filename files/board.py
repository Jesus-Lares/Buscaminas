from time import clock_getres
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
        for y in range(columns):  
            color = not color if columns%2==0 else color 
            for x in range(rows): 
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

    def open_all_mines(self,screen):
        for hide_mine in self.hide_mines:
            self.open_box(hide_mine[0], hide_mine[1]) 
        self.print_board( screen)
    
    def change_status_box(self,x,y,new_status=1,status=[3,4]):
        if 0<=x < self.rows and 0<= y < self.columns:
            if self.boxes[y* self.columns +x].get_status() not in status :
                self.boxes[y* self.rows +x].set_status(new_status)  
    
    def mouse_motion_board(self,positionX,positionY):
        x = int(positionX // self.width)
        y = int(positionY // (self.height))-1
        if y < 0:
            self.change_status_box(self.xx,self.yy)

        if self.xx !=  x or self.yy != y:
            self.change_status_box(self.xx,self.yy)
            self.change_status_box(x,y,2)
            self.xx = x
            self.yy = y 

    def mouse_button_left_down(self,positionX,positionY):
        self.pushed = True
        self.xx = self.x0 = int(positionX // self.width)
        self.yy = self.y0 = int(positionY // (self.height))-1
        self.change_status_box(self.xx,self.yy,2)

    def mouse_button_left_up(self,positionX,positionY):
        playing=True
        self.pushed = False
        x = int(positionX // self.width)
        y = int(positionY // (self.height))-1
        if len(self.boxes)!= 0 and y>=0:
            if self.x0 ==  x and self.y0 == y and self.boxes[y*self.rows+x].get_status() < 3:
                playing = self.open_box(x, y) 
        return playing

    def mouse_button_right_down(self,positionX,positionY):
        self.pushed = True
        self.xx = self.x0 = int(positionX // self.width)
        self.yy = self.y0 = int(positionY // (self.height))-1
        new_status = 4 if self.boxes[self.yy* self.columns +self.xx].get_status() not in [4,3] else 1 
        self.change_status_box(self.xx,self.yy,new_status,[3])
        return -1 if new_status == 4 else 1