from init import *

def inPlay(x, y):
    x0, y0, x1, y1 = 20, 20, 90, 90
    return x < x1 and x > x0 and y > y0 and y < y1


def inPause(x, y):
    x0, y0, x1, y1 = 110, 20, 180, 90
    return x < x1 and x > x0 and y > y0 and y < y1

def onBoard(data, x, y):
    ax0, ay0, ax1, ay1 = (x - data.pokemonSize, y - data.pokemonSize,
                          x + data.pokemonSize, y + data.pokemonSize)
    bx0, bx1, by0, by1 = data.boardBounds
    return ((ax1 > bx0) and (bx1 > ax0) and (ay1 > by0) and (by1 > ay0))

def inMenuBounds(x, y):  # if clicks in menu button
    x0, x1, y0, y1 = 1020, 1270, 10, 630
    return x < x1 and x > x0 and y > y0 and y < y1
    
def inReleaseBounds(x, y): #release pokemon
    x0, y0, x1, y1 = 1118, 412, 1164, 430
    return x < x1 and x > x0 and y > y0 and y < y1

def inParty(x, y):
    # if clicks in pokemon button in party, returns pokemon, else returns False
    for pokemon in data.party:
        x0, y0, width, height = pokemon.button
        x1, y1 = x0 + width, y0 + height
        if x > x0 and x < x1 and y > y0 and y < y1:
            return pokemon
    return False

