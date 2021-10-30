from init import *

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

def drawEnemies(data):  # draws all enemies
    for enemy in data.enemies:
        if enemy.exit == False:  # make sure is not dead or reached goal
            enemy.drawEnemy(data.screen)
            percent = enemy.hp/enemy.maxHp
            # set color of life bar
            if percent > .5:
                color = 0, 207, 0
            elif percent < .25:
                color = 255, 0, 0
            else:
                color = 255, 160, 0
            # draw lifebar above pokemon
            colorRect = (enemy.x+17-enemy.size, enemy.y-enemy.size-10,
                         round(62*percent), 5)
            pygame.draw.rect(data.screen, color, colorRect)
            lifebarframe = pygame.image.load("Assets/lifebar.jpg")
            lifebarframe = pygame.transform.scale(lifebarframe, (81, 7))
            data.screen.blit(lifebarframe, (enemy.x-enemy.size,
                                            enemy.y-enemy.size-10))

def redrawAll():  # redraws all draw functions
    drawPlay()
    drawPause()
    drawEnemies(data)

