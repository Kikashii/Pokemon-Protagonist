from __future__ import print_function, division
import sys
import pygame
import random
import string
import math

class Struct(object):  # inherited from object which is base class. In python 3.x, If we don't write object it will also work
    pass  # null statement. Doesn't do anything.


data = Struct()

data.size = width, height = 1280, 720  # tuple integer
data.screen = pygame.display.set_mode(data.size)


def loadBackground():  # load main background map
    img = pygame.image.load("Assets/TPbackground.jpg")
    data.screen.blit(img, (0, 0))

def drawPlay():  # draw play button
    x0, y0 = 40, 40
    #width, height = 70, 70
    img = pygame.image.load("Assets/arow.jpg")
    #img = pygame.transform.scale(img, (50, 50))
    data.screen.blit(img, (x0, y0))

def drawPause():  # draws pause button
    x0, y0 = 126, 32
    width, height = 70, 70
    img = pygame.image.load("Assets/pause.jpg")
    img = pygame.transform.scale(img, (50, 50))
    data.screen.blit(img, (x0, y0))

def redrawAll():  # redraws all draw functions
    drawPlay()
    drawPause()
        
      

def game():  # runs game
    while True:
        

        loadBackground()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:   
                x, y = pygame.mouse.get_pos()
                print(x, y)
        redrawAll()
                
        pygame.display.flip()
        

game()