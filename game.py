from classinit import *
from draw import *
from mouse import *
from timerfired import *


def game():  # runs game
    init(data)
    cinit()
    while True:
        if not data.intro and not data.gameOver:
            loadBackground()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # x, y = pygame.mouse.get_pos()
                # print(x, y)
                mouse(data)
        redrawAll()
        timerFired(data)
        pygame.display.flip()


game()
