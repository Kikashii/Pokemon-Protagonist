from init import *
from Myparty import *


def drawStatus(data):  # draws status of pokemon in status box
    color = 0, 0, 0
    font = pygame.font.Font("Assets/pokemon_pixel_font.ttf", 20)
    pygame.draw.rect(data.screen, color, (1030, 235, 225, 200), 2)
    if data.status != None or type(data.hover) == MyParty:  # pokemon is selected
        if data.status != None:
            pokemon = data.status
        else:
            pokemon = data.hover  # status of hover pokemon
        name = font.render(pokemon.pokemon, True, color)
        data.screen.blit(name, (1035, 240))
        level = font.render(("Level: %d" % pokemon.level), True, color)
        data.screen.blit(level, (1035, 280))
        attack = font.render(("Attack: %d" %
                              (pokemon.baseAttack + pokemon.attackGrowth)), True, color)
        data.screen.blit(attack, (1035, 265))
        release = font.render("Release", True, color)
        data.screen.blit(release, (1118, 412))
        if pokemon.onBoard:
            exp = font.render(("EXP untill next level: %d" %
                               (pokemon.maxExp - pokemon.exp)), True, color)
            data.screen.blit(exp, (1035, 295))


def drawText(data):  # draws all menu text
    font = pygame.font.Font("Assets/pokemon_pixel_font.ttf", 30)
    x0, y0 = 400, 30
    wave = font.render(("WAVE %d" % data.wave), True, (60, 59, 48))
    data.screen.blit(wave, (x0, y0))
    x1, y1 = 270, 30
    life = font.render(("HEALTH %d" % data.lives), True, (60, 59, 48))
    data.screen.blit(life, (x1, y1))
    x2, y2, = 517, 30
    money = font.render(str(data.coins), True, (60, 59, 48))
    data.screen.blit(money, (x2, y2))
    Help = font.render("Help", True, (255, 255, 255))
    data.screen.blit(Help, (670, 27))


def returnText(num):
    if num == 1:
        return ("""\
Click on the POKeMON in your party to set on board, see stats.""")
    elif num == 2:
        return ("""\
You can buy Pokeball, and use it by clicking on the Pokeball text .""")
    elif num == 3:
        return ("""\
Throw a Pokeball to expand your party, but make sure the enemy life is low!""")


def drawHelp(data):  # draws all instructions
    if data.help:
        font = pygame.font.Font("Assets/pokemon_pixel_font.ttf", 26)
        img = pygame.image.load("Assets/box.png")
        data.screen.blit(img, (23, 83))
        rect, color, rect3 = (41, 160, 312, 107), (0, 0, 0), (644, 455, 333, 71)
        text = "Use these buttons to play and pause to control the waves."
        drawTextRect(data.screen, text, color, rect, font)
        rect1, rect2 = (644, 94, 333, 133), (644, 388, 333, 133)
        text1 = returnText(1)
        text2 = returnText(2)
        text3 = returnText(3)
        drawTextRect(data.screen, text1, color, rect1, font)
        drawTextRect(data.screen, text2, color, rect2, font)
        drawTextRect(data.screen, text3, color, rect3, font)


def drawMenu():  # draws menu with all buttons and text
    leftbound, width, topbound, height, color = 1020, 250, 10, 620, (
        255, 255, 255)
    menuStart, buttonHeight = 440, 50
    font = pygame.font.Font("Assets/pokemon_pixel_font.ttf", 40)
    party = font.render("POKeMON", True, (0, 0, 0))
    data.screen.blit(party, (leftbound + 70, 23))
    for i in range(1, 4):
        if i == data.hover:
            color = 255, 0, 0
            pygame.draw.rect(data.screen, color, (leftbound + 10,
                                                  menuStart, width - 20, buttonHeight), 2)
        menuStart += buttonHeight + 10
    font = pygame.font.Font("Assets/pokemon_pixel_font.ttf", 35)
    pkbl = font.render("Pokeball", True, (0, 0, 0))
    data.screen.blit(pkbl, (leftbound + 30, 440 + 10))
    price = font.render(str(200), True, (0, 0, 0))
    data.screen.blit(price, (leftbound + 180, 440 + 10))
    moneySign = pygame.image.load("Assets/money.png")
    moneySign = pygame.transform.scale(moneySign, (30, 30))
    data.screen.blit(moneySign, (leftbound + 155, 440 + 10))


def drawParty():
    startY = 60
    startX = 1030
    width = 230
    height = 25
    font = pygame.font.Font("Assets/pokemon_pixel_font.ttf", 20)
    for i in range(len(data.party)):
        pokemon = data.party[i]  # display name of each pokemon
        name = pokemon.pokemon
        pokemon.button = startX, startY, width, height
        if data.hover == pokemon or data.selected == pokemon:
            pygame.draw.rect(data.screen, (255, 0, 0), pokemon.button, 1)
        name = font.render(name, True, (0, 0, 0))
        data.screen.blit(name, (startX + 5, startY + 5))
        startY += 25


def drawRadius(data):  # draws radius if a tower is selected
    if data.status != None or data.selected != None:
        if data.selected != None:
            pokemon = data.selected
        else:
            pokemon = data.status
        pokemon.drawRadius(data.screen)


def drawTextRect(surface, text, color, rect, font, aa=False, bkg=None):
    rect, lineSpacing = pygame.Rect(rect), -2
    # get the height of the font
    fontHeight, y = font.size("Tg")[1], rect.top
    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + fontHeight >= rect.bottom:
            break
        # determine maximum width of line
        while font.size(text[:i])[0] <= rect.width and i <= len(text):
            i += 1
        # if we've wrapped the text, then adjust the wrap to the last word
        if i <= len(text):
            i = text.rfind(" ", 0, i) + 1
        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
        # remove the text we just blitted
        text = text[i:]
    return text


def drawIntroText(data):
    font = pygame.font.Font("Assets/pokemon_pixel_font.ttf", 40)
    color = 0, 0, 0
    text, color = "Choose a POKeMON.", (255, 255, 255)
    rect = 248, 571, 793, 104
    drawTextRect(data.screen, text, color, rect, font)


def drawIntro(data):  # draws intro
    img = pygame.image.load("Assets/starter.png")
    data.screen.fill((0, 0, 0))  # fill screen with black first
    img = pygame.transform.scale(img, (922, 691))
    data.screen.blit(img, (167, 8))
    drawIntroText(data)


def loadBackground():  # load main background map
    img = pygame.image.load("Assets/TPbackground.jpg")
    data.screen.blit(img, (0, 0))


def drawPlay():  # draw play button
    x0, y0 = 40, 40
    # width, height = 70, 70
    img = pygame.image.load("Assets/arow.png")
    # img = pygame.transform.scale(img, (50, 50))
    data.screen.blit(img, (x0, y0))


def drawPause():  # draws pause button
    x0, y0 = 126, 32
    width, height = 70, 70
    img = pygame.image.load("Assets/pause.png")
    img = pygame.transform.scale(img, (50, 50))
    data.screen.blit(img, (x0, y0))


def drawEnemies(data):  # draws all enemies
    for enemy in data.enemies:
        if not enemy.exit:  # make sure is not dead or reached goal
            enemy.drawEnemy(data.screen)
            percent = enemy.hp / enemy.maxHp
            # set color of life bar
            if percent > .5:
                color = 0, 207, 0
            elif percent < .25:
                color = 255, 0, 0
            else:
                color = 255, 160, 0
            # draw lifebar above pokemon
            colorRect = (enemy.x + 17 - enemy.size, enemy.y - enemy.size - 10,
                         round(62 * percent), 5)
            pygame.draw.rect(data.screen, color, colorRect)
            lifebarframe = pygame.image.load("Assets/lifebar.png")
            lifebarframe = pygame.transform.scale(lifebarframe, (81, 7))
            data.screen.blit(lifebarframe, (enemy.x - enemy.size,
                                            enemy.y - enemy.size - 10))


def drawTowers(data):  # draw all towers on board
    for pokemon in data.party:
        if pokemon.onBoard:
            pokemon.drawTower(data.screen)


def drawAllBullets(data):  # draws all bullets on board
    for tower in data.party:
        if tower.onBoard and tower.bullets != []:
            for bullet in tower.bullets:
                bullet.drawBullet(data.screen)


def drawPokeball(data):  # draws pokeball if is selected
    if data.pokeball:
        x, y = pygame.mouse.get_pos()
        img = pygame.image.load("Assets/Pokeball.png")
        data.screen.blit(img, (x - 42, y - 42))


def drawGameOver(data):  # draws gameover
    font = pygame.font.Font("Assets/pokemon_pixel_font.ttf", 40)
    img = pygame.image.load("Assets/gameover.png")
    img = pygame.transform.scale(img, (data.size))
    data.screen.blit(img, (0, 0))
    gameover = font.render("Game Over", True, (0, 0, 0))
    data.screen.blit(gameover, (880, 452))
    wave = font.render(("Last wave: %d" % data.wave), True, (0, 0, 0))
    data.screen.blit(wave, (701, 512))
    restart = font.render("Restart?", True, (0, 0, 0))
    data.screen.blit(restart, (701, 572))


def redrawAll():  # redraws all draw functions
    if data.gameOver:
        drawGameOver(data)
    elif data.intro:
        drawIntro(data)
    else:
        drawAllBullets(data)
        drawTowers(data)
        drawRadius(data)
        drawText(data)
        drawPokeball(data)
        drawMenu()
        drawParty()
        drawStatus(data)
        drawPlay()
        drawPause()
        drawEnemies(data)
        drawHelp(data)
