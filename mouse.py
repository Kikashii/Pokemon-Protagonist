from init import *
from button import *


def mousePart2(x, y, data):  # part 2 of mousePresed wrap
    if inPlay(x, y):
        data.paused = False
    elif inPause(x, y):
        data.paused = True

def mouse(data):  # mouse pressed wrap
    x, y = pygame.mouse.get_pos()
    # if data.gameOver:
    #     gameoverPressed(data, x, y)
    # elif data.intro:
    #     mouseIntro(data, x, y)
    # else:
    mousePart2(x, y, data)

