from init import *
from button import *
from Myparty import *
from hover import *
from timerfired import *


def menuButtons(x, y):
    if pokeballBound(x, y) and data.pokeball == False:
        data.paused = True
        if data.coins >= 200:
            data.coins -= 200
            data.pokeball = True
        data.paused = False
    if inParty(x, y):
        curPoke = inParty(x, y)  # current pokemon
        if not curPoke.onBoard:  # only in party not on board yet
            data.selected = curPoke  # pick up pokemon
            data.selected.x, data.selected.y = x, y
        # already on board, show status
        else:
            data.status = curPoke


def mousePart2(x, y, data):  # part 2 of mousePresed wrap
    if data.pokeball:
        catchPokemon(data, x, y)
    elif inPlay(x, y):
        data.paused = False
    elif inPause(x, y):
        data.paused = True
    elif data.selected != None:
        # picked up to pokemon to put on board
        if onBoard(data, x, y) and isLegal(data, x, y):
            data.selected.x, data.selected.y = x, y
            data.selected.bounds = x - 10, y - 10, x + 10, y + 10
            data.selected.onBoard, data.selected = True, None
    elif data.status is not None and inReleaseBounds(x, y):
        data.party.remove(data.status)
        data.status = None
    elif inMenuBounds(x, y):
        menuButtons(x, y)


def mouseIntro(data, x, y):  # mouse pressed for intro
    for pokemon in data.starters:
        x0, y0, x1, y1 = pokemon.pokeball
        if x0 < x < x1 and y0 < y < y1:  # add chosen pokemon to party
            data.party.append(MyParty(pokemon.id, data))
            data.intro = False


def mouse(data):  # mouse pressed wrap
    x, y = pygame.mouse.get_pos()
    if data.gameOver:
        gameoverPressed(data, x, y)
    elif data.intro:
        mouseIntro(data, x, y)
    else:
        mousePart2(x, y, data)
