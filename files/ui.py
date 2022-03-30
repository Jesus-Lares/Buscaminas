import pygame
from utils import *

class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,0,0,1,1)
    def update(self):
        self.left,self.top = pygame.mouse.get_pos()
    def get_pos(self):
        return pygame.mouse.get_pos()

class Button(pygame.sprite.Sprite):
    def __init__(self,screen,text,x,y,font,colorFont=BACKGROUND,colorBackground=PRIMARY):
        self.text = text
        self.font = font
        self.colorFont = colorFont
        self.colorBackground = colorBackground
        self.rect = pygame.Rect(x,y,100,25)
        self.showBtn(screen,colorBackground,colorFont,font)        

    def showBtn(self,screen,colorRect,colorFont,font):
        pygame.draw.rect(screen,colorRect,self.rect,0)
        textRender = font.render(self.text,True,colorFont)
        screen.blit(textRender,(self.rect.x + (self.rect.width - textRender.get_width())/2,self.rect.y + (self.rect.height - textRender.get_height())/2))

    def update(self,screen,cursor):
        if cursor.colliderect(self.rect):
            self.showBtn(screen,self.colorFont,HEADER,self.font)
        else: 
            self.showBtn(screen,self.colorBackground,self.colorFont,self.font)

    def getRect(self):
        return self.rect

class Text(pygame.sprite.Sprite):
    def __init__(self,screen,text,x,y,font,colorFont=BACKGROUND,colorBackground=HEADER):
        self.text = text
        self.font = font
        self.colorFont = colorFont
        self.colorBackground= colorBackground
        self.x = x
        self.y = y
        self.screen = screen

        self.update(text)        
  
    def update(self,text):
        textRender = self.font.render(text,True,self.colorFont,self.colorBackground)
        self.screen.blit(textRender,(self.x,self.y))

    