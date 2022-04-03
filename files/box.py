from utils import *

import pygame
import pygame.gfxdraw

class Box():
    def __init__(self, x, y, size_x, size_y,  status, value,color):
        self.font = pygame.font.SysFont("arial",18)
        self.color = color
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.status = status # Estado de la casilla SIN MARCAR, CURSOR_ENCIMA, MARCADA.
        self.value = value # Valor de la casilla ' ', '0'...'8' bomba

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def draw_box(self, screen):
        colorBox=BACKGROUND if self.color else PRIMARY
        if self.status == 1:# SIN MARCAR
            pygame.gfxdraw.box(screen, (self.x, self.y, self.size_x, self.size_y), colorBox)
           
        elif self.status == 2: # CURSOR_ENCIMA
            pygame.gfxdraw.box(screen, (self.x, self.y, self.size_x, self.size_y), GRAY)
        elif self.status == 3: # MARCADA
            if int(self.value) == 9:
                pygame.gfxdraw.box(screen, (self.x, self.y, self.size_x, self.size_y), RED)
                imgMines = pygame.image.load("images/mina.png")
                pictureMines = pygame.transform.scale(imgMines,[20,20])
                screen.blit(pictureMines, (self.x + (self.size_x / 2) - (pictureMines.get_width()/2), self.y + (self.size_y / 2) - (pictureMines.get_height()/2)))
            else:
                pygame.gfxdraw.box(screen, (self.x, self.y, self.size_x, self.size_y), SILVER)
                size = self.font.size(self.value)
                texto = self.font.render(self.value, 1, COLORS_BOXES[int(self.value)])
                screen.blit(texto, (self.x + (self.size_x / 2) - (size[0] / 2), self.y + (self.size_y / 2) - (size[1] / 2)))
        elif self.status == 4: # FLAG
            pygame.gfxdraw.box(screen, (self.x, self.y, self.size_x, self.size_y), colorBox)
            imgFlag = pygame.image.load("images/flag.png")
            pictureFlag = pygame.transform.scale(imgFlag,[20,20])
            screen.blit(pictureFlag, (self.x + (self.size_x / 2) - (pictureFlag.get_width()/2), self.y + (self.size_y / 2) - (pictureFlag.get_height()/2)))

