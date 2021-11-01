from init import *
from button import *


def inTowerBounds(data, bounds):  # make sure tower is not on top of another tower
    ax0, ay0, ax1, ay1 = bounds
    for tower in data.party:
        if tower.onBoard:
            bx0, by0, bx1, by1 = tower.bounds
            if (ax1 > bx0) and (bx1 > ax0) and (ay1 > by0) and (by1 > ay0):
                return False
    return True


def isLegal(data, x, y):  # make sure tower is not on route, in pond or trees
    ax0, ay0, ax1, ay1 = (x - data.pokemonSize, y - data.pokemonSize,
                          x + data.pokemonSize, y + data.pokemonSize)
    routeBounds = [(0, 565, 340, 642), (260, 236, 340, 642), (260, 236, 571, 315),
                   (485, 236, 571, 556), (830, 395,
                                          1019, 469), (489, 475, 714, 556),
                   (630, 475, 714, 650), (714, 571,
                                          1019, 648), (939, 395, 1019, 648),
                   (841, 188, 924, 469), (841, 188, 1019, 268), (931, 0, 1019, 268)]
    pondBounds = [(640, 247, 775, 411), (575, 312, 645, 411)]
    treesBounds = [(577, 374, 837, 475), (0, 0, 783, 105), (0, 73, 264, 167),
                   (0, 620, 280, 727), (488, 616, 1280, 720)]
    toTest = [routeBounds, pondBounds, treesBounds]
    for test in toTest:
        for bound in test:
            bx0, by0, bx1, by1 = bound
            if (ax1 > bx0) and (bx1 > ax0) and (ay1 > by0) and (by1 > ay0):
                return False
    if not inTowerBounds(data, (ax0, ay0, ax1, ay1)):
        return False
    return True


def buildTowerHover(x, y, data):
    # draw rect of size of pokemon when building if legal
    data.selected.x, data.selected.y = x, y
    if isLegal(data, x, y) and onBoard(data, x, y):
        pygame.draw.rect(data.screen, (255, 255, 255), (x - data.selected.size,
                                                        y - data.selected.size, data.selected.size * 2,
                                                        data.selected.size * 2),
                         3)


def introHover(data):  # for starts hover during intro
    x, y = pygame.mouse.get_pos()
    for pokemon in data.starters:
        x0, y0, x1, y1 = pokemon.pokeball
        if x0 < x < x1 and y0 < y < y1:
            pokemon.drawTower(data.screen)


def hover(data):  # general hover fucntion wrap
    x, y = pygame.mouse.get_pos()
    # if onHelp(x, y):  # when mouse on help button, show instructions
    #     data.help, data.paused, data.selected = True, True, None
    # else:
    #     data.help = False
    if data.selected is not None:  # put tower on board
        buildTowerHover(x, y, data)
    if inParty(x, y):
        data.hover = inParty(x, y)
    elif data.status is not None and inReleaseBounds(x, y):
        pygame.draw.rect(data.screen, (255, 0, 0), (1115, 412, 50, 18), 1)
    elif inParty(x, y):
        data.hover = inParty(x, y)
    # elif buttonHover(data, x, y) != False:
    #     data.hover = buttonHover(data, x, y)
    else:
        data.hover = None
