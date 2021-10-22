from __future__ import print_function, division
import sys
import pygame
import random
import string
import math
from database import *


class Struct(object):  # inherited from object which is base class. In python 3.x, If we don't write object it will also work
    pass  # null statement. Doesn't do anything.


data = Struct()

def init(data):
     # pygame init - Initializes pygame modules
    pygame.init()
    # set screen size and screen
    data.size = width, height = 1280, 720  # tuple integer
    # Initialize a window or screen for display
    data.screen = pygame.display.set_mode(data.size)
    # set all lists
    listInit(data)
    # set all databases
    databaseInit(data)
    # set all mode inits
    modeInit(data)
    # set all player values
    playerInit(data)
    # set all values to do with enemies
    enemyInit(data)

def databaseInit(data):
    # set pokemon data from database.py
    data.database = setPokemonData()
    # size of my pokemons- placing rectangle size
    data.pokemonSize = 35
    # make tower defense route
    #createRoute(data)
    data.boardBounds = 0, 1020, 0, 630

def playerInit(data):
    data.lives = 10  # max num of lives
    data.wave = 1  # current wave count

def enemyInit(data):
    # speed of enemy
    data.speed = 4
    # counter for frames before placing a new enemy
    data.count = 30
    # max frames to place new enemy
    data.maxCount = 30
    # num of enemies per wave
    data.num = 7
    # make tower defense route
    createRoute(data)
    # set pokemons for current wave
    setWave(data)

def listInit(data):
    # pokemon to be appended to enemies
    data.waveEnemies = []
    # wild pokemon for current wave
    data.enemies = []

def modeInit(data):
    #screen is paused
    data.paused = True
    
def createRoute(data):  # creates path
    corners = [(0, 600), (290, 600), (290, 270), (520, 270), (520, 510),
               (660, 510), (660, 600), (970, 600), (970,
                                                    420), (870, 420), (870, 220), (970, 220),
               (970, 100)]  # creates path for enemy
    # this list contains the info where the enemey will traverse pixel by pixel
    data.checkPoints = []
    # adds all x,y positions into new list
    for i in range(1, len(corners)):
        x0, y0 = corners[i-1]
        x1, y1 = corners[i]
        # check if horizontal or vertical
        # horizontal
        if x1-x0 == 0:
            verticlePath(data, x0, y0, x1, y1)
        # verticle
        else:
            horizontalPath(data, x0, y0, x1, y1)


def verticlePath(data, x0, y0, x1, y1):
    # find difference = distance between 2corners
    d = y1-y0
    # loops through every pixel between distance
    for i in range(abs(d)):
        # check if route is going up or down
        if d < 0:  # will go downward
            data.checkPoints.append((x0, y0-i))
        else:  # will go upward
            data.checkPoints.append((x0, y0+i))


def horizontalPath(data, x0, y0, x1, y1):
    # same as verticle path but using x coordinates
    d = x1-x0
    for i in range(abs(d)):
        if d < 0:  # will go left
            data.checkPoints.append((x0-i, y0))
        else:  # will go right
            data.checkPoints.append((x0 + i, y0))
            

