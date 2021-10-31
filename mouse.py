from init import *
from button import *


def mousePart2(x, y, data):  # part 2 of mousePresed wrap
    if inPlay(x, y):
        data.paused = False
    elif inPause(x, y):
        data.paused = True
    elif data.selected != None:
        # picked up to pokemon to put on board
        if onBoard(data, x, y) and isLegal(data, x, y):
            data.selected.x, data.selected.y = x, y
            data.selected.bounds = x-10, y-10, x+10, y+10
            data.selected.onBoard, data.selected = True, None
    elif data.status != None and inReleaseBounds(x, y):
        data.party.remove(data.status)
        data.status = None
    elif inMenuBounds(x, y):
        menuButtons(x, y)

def mouseIntro(data, x, y):  # mouse pressed for intro
    for pokemon in data.starters:
        x0, y0, x1, y1 = pokemon.pokeball
        if x > x0 and x < x1 and y > y0 and y < y1:  # add chosen pokemon to party
            data.party.append(MyParty(pokemon.id, data))
            data.intro = False


def mouse(data):  # mouse pressed wrap
    x, y = pygame.mouse.get_pos()
    # if data.gameOver:
    #     gameoverPressed(data, x, y)
    if data.intro:
        mouseIntro(data, x, y)
    else:
        mousePart2(x, y, data)

