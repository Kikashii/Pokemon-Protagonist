from __future__ import print_function, division
import sys, pygame, random, string, math
from database import setPokemonData, itemsData, elementsChart



class Struct(object): pass


data = Struct()


def init(data):
    # pygame init
    pygame.init()
    # set screen size and screen
    data.size = width, height = 1280, 720
    data.screen = pygame.display.set_mode(data.size)
    # set all lists
    listInit(data)
    # set all databases
    databaseInit(data)
    # set all mode inits
    modeInit(data)
    # set all player values
    playerInit(data)


def databaseInit(data):
    # set pokemon data from database.py
    data.database = setPokemonData()
    # size of sprites
    data.pokemonSize = 35
    # make tower defense route
    createRoute(data)
    # set starter pokemons
    setStarters(data)
    data.boardBounds = 0, 1020, 0, 630
    data.elementsChart = elementsChart()


def playerInit(data):
    data.lives = 10  # max num of lives
    data.wave = 1  # current wave count
    data.coins = 50  # money player has
    # whether to show pokemon status
    data.status = None
    # whether mouse is hovering on button or pokemon
    data.hover = None
    # to pick up pokemon to place on board
    data.selected = None
    # whether an item is selected to use on pokemon
    data.selectedItem = None



def listInit(data):
    # 3 starter pokemons for intro
    data.starters = []
    # all items in pokemart
    data.storeItems = []
    # all pokemon in party
    data.party = []

    # all bag items
    data.items = []


def modeInit(data):
    # all modes
    data.intro = True
    data.bag = False
    data.gameOver = False
    data.mart = False
    data.paused = True
    # current frame if mode is on intro
    data.introFrame = 0
    data.help = False


def setStarters(data):
    # append charmander, bulbasur and squirtle to set starters
    # set pokemon from database
    bulbasaur = MyParty(1, data)
    charmander = MyParty(4, data)
    squirtle = MyParty(7, data)
    # find bounds of pokeballs in the intro
    bulbasaur.pokeball = 388, 278, 508, 400
    # set x y so starters can be drawn when mouse hovers
    bulbasaur.x, bulbasaur.y, bulbasaur.size = 440, 235, 80
    # set img of pokemon bigger
    size = 160, 160
    bulbasaur.img = pygame.transform.scale(bulbasaur.img, size)
    charmander.pokeball = 571, 332, 700, 466
    charmander.x, charmander.y, charmander.size = 631, 310, 80
    charmander.img = pygame.transform.scale(charmander.img, size)
    squirtle.pokeball = 764, 278, 879, 400
    squirtle.x, squirtle.y, squirtle.size = 821, 235, 80
    squirtle.img = pygame.transform.scale(squirtle.img, size)
    data.starters.append(bulbasaur)
    data.starters.append(charmander)
    data.starters.append(squirtle)


def createRoute(data):  # creates path
    corners = [(0, 600), (290, 600), (290, 270), (520, 270), (520, 510),
               (660, 510), (660, 600), (970, 600), (970, 420), (870, 420), (870, 220), (970, 220),
               (970, 100)]
    data.checkPoints = []
    # adds all x,y positions into new list
    for i in range(1, len(corners)):
        x0, y0 = corners[i - 1]
        x1, y1 = corners[i]
        # check if horizontal or vertical
        # horizontal
        if x1 - x0 == 0:
            verticlePath(data, x0, y0, x1, y1)
        # verticle
        else:
            horizontalPath(data, x0, y0, x1, y1)


def verticlePath(data, x0, y0, x1, y1):
    # find difference = distance between 2corners
    d = y1 - y0
    # loops through every pixel between distance
    for i in range(abs(d)):
        # check if route is going up or down
        if d < 0:
            data.checkPoints.append((x0, y0 - i))
        else:
            data.checkPoints.append((x0, y0 + i))


def horizontalPath(data, x0, y0, x1, y1):
    # same as verticle path but using x coordinates
    d = x1 - x0
    for i in range(abs(d)):
        if d < 0:
            data.checkPoints.append((x0 - i, y0))
        else:
            data.checkPoints.append((x0 + i, y0))



###############classes################################

class Pokemon(object):  # pokemon class
    def __init__(self, pokemon, data):
        # pokemon = pokemon id
        tup = data.database[pokemon]
        self.id = pokemon
        self.pokemon = tup[0]
        self.element = tup[1]
        self.stage = tup[2]  # what evolution form pokemon is on
        self.evolve = tup[3]
        self.baseHp, self.baseAttack, self.baseDefense = tup[4], tup[5], tup[6]
        self.evolveConditions = tup[7]
        self.bounds = None
        self.setSize()
        self.button = None  # if is pressed to see status, items, etc
        image = pygame.image.load("%s.png" % self.pokemon)  # get image
        self.img = pygame.transform.scale(image, (self.size * 2, self.size * 2))

    def setSize(self):
        # set size of pokemon depending on stage.
        # more evolved pokemon = larger size
        if self.stage == 1:
            self.size = data.pokemonSize
        elif self.stage == 2:
            self.size = data.pokemonSize + 5
        elif self.stage == 3:
            self.size = data.pokemonSize + 20


class MyParty(Pokemon):
    # initially just in party/menu not on board
    def __init__(self, pokemon, data, level=5, x=None, y=None):
        Pokemon.__init__(self, pokemon, data)  # super
        # x and y not set until is on board
        self.x = x
        self.y = y
        self.setRange()
        self.maxCounter = 8  # when to shoot next bullet
        self.counter = self.maxCounter
        self.target = None  # target enemy
        self.bullets = []
        self.onBoard = False
        self.radius = False  # show radius or not
        self.level = level
        self.exp = 0
        self.maxExp = 50
        self.attackGrowth = 0
        self.attack = self.baseAttack + self.attackGrowth

    def setRange(self):  # range/radius of tower depending on evolved stage
        if self.stage == 1:
            self.range = 100
        if self.stage == 2:
            self.range = 150
        if self.stage == 3:
            self.range = 200

    def equation(self, x, y):  # equation for checking whether enemy is in range
        return (x - self.x) ** 2 + (y - self.y) ** 2 < self.range ** 2

    def inRange(self, bounds):  # check whether opbject is in radius
        x0, y0, x1, y1 = bounds
        if (self.equation(x1, y0) or self.equation(x1, y1) or self.equation(x0, y0)
                or self.equation(x0, y0)):
            return True
        else:
            return False

    def drawTower(self, canvas):  # draw pokemon once set on board
        data.screen.blit(self.img, (self.x - self.size, self.y - self.size))

    def drawRadius(self, canvas):  # draws radius sof pokemon
        pygame.draw.circle(canvas, (255, 255, 255), (self.x, self.y), self.range, 3)

    def updateStats(self):  # updatest attack stats
        baseLevel = 5
        self.attack = self.attackGrowth + self.baseAttack
        self.attackGrowth = self.level - baseLevel






#########################Buttons######################
# all button bounds
def onHelp(x, y):
    x0, y0, x1, y1 = 637, 16, 743, 63
    return x < x1 and x > x0 and y > y0 and y < y1


def onBoard(data, x, y):
    ax0, ay0, ax1, ay1 = (x - data.pokemonSize, y - data.pokemonSize,
                          x + data.pokemonSize, y + data.pokemonSize)
    bx0, bx1, by0, by1 = data.boardBounds
    return ((ax1 > bx0) and (bx1 > ax0) and (ay1 > by0) and (by1 > ay0))


def inMenuBounds(x, y):  # if clicks in menu button
    x0, x1, y0, y1 = 1020, 1270, 10, 630
    return x < x1 and x > x0 and y > y0 and y < y1


def bagBound(x, y):  # if clicks in bag button
    x0, y0, x1, y1 = 1030, 440, 1260, 490
    return x < x1 and x > x0 and y > y0 and y < y1


def evolveBound(x, y):  # if clicks in evolve button
    x0, y0, x1, y1 = 1030, 500, 1260, 550
    return x < x1 and x > x0 and y > y0 and y < y1


def pokemartBound(x, y):  # if blibk in pokemart button
    x0, y0, x1, y1 = 1030, 560, 1260, 610
    return x < x1 and x > x0 and y > y0 and y < y1


def inPlay(x, y):
    x0, y0, x1, y1 = 20, 20, 90, 90
    return x < x1 and x > x0 and y > y0 and y < y1


def inPause(x, y):
    x0, y0, x1, y1 = 110, 20, 180, 90
    return x < x1 and x > x0 and y > y0 and y < y1


def inReleaseBounds(x, y):
    x0, y0, x1, y1 = 1118, 412, 1164, 430
    return x < x1 and x > x0 and y > y0 and y < y1


def inRestartBounds(x, y):  # for gameover screen
    x0, y0, x1, y1 = 701, 575, 817, 611
    return x < x1 and x > x0 and y > y0 and y < y1


def inParty(x, y):
    # if clicks in pokemon button in party, returns pokemon, else returns False
    for pokemon in data.party:
        x0, y0, width, height = pokemon.button
        x1, y1 = x0 + width, y0 + height
        if x > x0 and x < x1 and y > y0 and y < y1:
            return pokemon
    return False


###################timerFired########################3333
# All timerFired functions




def introHover(data):  # for starts hover during intro
    if data.introFrame == 7:
        x, y = pygame.mouse.get_pos()
        for pokemon in data.starters:
            x0, y0, x1, y1 = pokemon.pokeball
            if x > x0 and x < x1 and y > y0 and y < y1:
                pokemon.drawTower(data.screen)





def gameoverHover(data):  # hover for restart button
    x, y = pygame.mouse.get_pos()
    if inRestartBounds(x, y):
        pygame.draw.rect(data.screen, (255, 0, 0), (698, 570, 119, 36), 2)


def timerFired(data):  # general timerfired function wrap
    if data.gameOver:
        gameoverHover(data)
    elif data.intro == False:
        hover(data)
    else:
        introHover(data)



def buildTowerHover(x, y, data):
    # draw rect of size of pokemon when building if legal
    data.selected.x, data.selected.y = x, y
    if isLegal(data, x, y) and onBoard(data, x, y):
        pygame.draw.rect(data.screen, (255, 255, 255), (x - data.selected.size,
                                                        y - data.selected.size, data.selected.size * 2,
                                                        data.selected.size * 2),
                         3)


def hover(data):  # general hover fucntion wrap
    x, y = pygame.mouse.get_pos()
    if onHelp(x, y):  # when mouse on help button, show instructions
        data.help, data.paused, data.selected = True, True, None
    else:
        data.help = False
    if data.selected != None:  # put tower on board
        buildTowerHover(x, y, data)
    if inParty(x, y) and data.selectedItem != None:
        data.hover = inParty(x, y)
    elif data.status != None and inReleaseBounds(x, y):
        pygame.draw.rect(data.screen, (255, 0, 0), (1115, 412, 50, 18), 1)
    elif inParty(x, y):
        data.hover = inParty(x, y)
    elif buttonHover(data, x, y) != False:
        data.hover = buttonHover(data, x, y)
    else:
        data.hover = None


def buttonHover(data, x, y):  # button hover for menu
    if bagBound(x, y):
        return 1
    elif evolveBound(x, y):
        return 2
    elif pokemartBound(x, y):
        return 3
    else:
        return False


def isLegal(data, x, y):  # make sure tower is not on route, in pond or trees
    ax0, ay0, ax1, ay1 = (x - data.pokemonSize, y - data.pokemonSize,
                          x + data.pokemonSize, y + data.pokemonSize)
    routeBounds = [(0, 565, 340, 642), (260, 236, 340, 642), (260, 236, 571, 315),
                   (485, 236, 571, 556), (830, 395, 1019, 469), (489, 475, 714, 556),
                   (630, 475, 714, 650), (714, 571, 1019, 648), (939, 395, 1019, 648),
                   (841, 188, 924, 469), (841, 188, 1019, 268), (931, 0, 1019, 268)]
    pondBounds = [(640, 247, 775, 411), (575, 312, 645, 411)]
    treesBounds = [(577, 374, 837, 475), (0, 0, 783, 105), (0, 73, 264, 167),
                   (0, 620, 280, 727), (488, 616, 1280, 720)]
    toTest = [routeBounds, pondBounds, treesBounds]
    for test in toTest:
        for bound in test:
            bx0, by0, bx1, by1 = bound
            if ((ax1 > bx0) and (bx1 > ax0) and (ay1 > by0) and (by1 > ay0)):
                return False
    if not inTowerBounds(data, (ax0, ay0, ax1, ay1)): return False
    return True


def inTowerBounds(data, bounds):  # make sure tower is not on top of another tower
    ax0, ay0, ax1, ay1 = bounds
    for tower in data.party:
        if tower.onBoard:
            bx0, by0, bx1, by1 = tower.bounds
            if ((ax1 > bx0) and (bx1 > ax0) and (ay1 > by0) and (by1 > ay0)):
                return False
    return True


def gameoverPressed(data, x, y):
    if inRestartBounds(x, y):  # if clicks on restart set init data
        init(data)


def mouseIntro(data, x, y):  # mouse pressed for intro
    if data.introFrame == 7:  # last frame for intro
        for pokemon in data.starters:
            x0, y0, x1, y1 = pokemon.pokeball
            if x > x0 and x < x1 and y > y0 and y < y1:  # add chosen pokemon to party
                data.party.append(MyParty(pokemon.id, data))
                data.intro = False
    else:
        data.introFrame += 1


# menuButtons for mousePressed
def menuButtons(x, y):
    if inParty(x, y):
        curPoke = inParty(x, y)  # current pokemon
        if curPoke.onBoard == False:  # only in party not on board yet
            data.selected = curPoke  # pick up pokemon
            data.selected.x, data.selected.y = x, y
        # already on board, show status
        else:
            data.status = curPoke


def mousePart2(x, y, data):  # part 2 of mousePresed wrap
    # if pokeballmode is on
    if inPause(x, y):
        data.paused = True
    elif data.selected != None:
        # picked up to pokemon to put on board
        if onBoard(data, x, y) and isLegal(data, x, y):
            data.selected.x, data.selected.y = x, y
            data.selected.bounds = x - 10, y - 10, x + 10, y + 10
            data.selected.onBoard, data.selected = True, None
    elif data.status != None and inReleaseBounds(x, y):
        data.party.remove(data.status)
        data.status = None
    elif data.status != None and evolveBound(x, y):
        evolve(data.status, data)
    elif inMenuBounds(x, y):
        menuButtons(x, y)


def mouse(data):  # mouse pressed wrap
    x, y = pygame.mouse.get_pos()
    if data.gameOver:
        gameoverPressed(data, x, y)
    elif data.intro:
        mouseIntro(data, x, y)
    else:
        mousePart2(x, y, data)



###############draw functions#################3
# adapted from course notes collapsespaces
def collapseNewLine(s):
    # return string with no spaces
    result = ""
    for c in s:
        if c == '\n':
            continue
        else:
            result += c
    return result


# generate text for instructions
def returnText(num):
    if num == 1:
        return ("""\
Click on the POKeMON in your party to set on board, see stats,and evolve.""")
    elif num == 3:
        return ("""\
You can buy items from the POKeMART, and use them by clicking bag.""")
    elif num == 4:
        return ("""\
Throw a Pokeball to expand your party, but make sure the enemy life is low!""")
    else:
        return collapseNewLine("""\
Evolve conditions may differ depending on the POKeMON. Some may require special
 stones.""")


def drawHelp(data):  # draws all instructions
    if data.help:
        font = pygame.font.Font("pokemon_pixel_font.ttf", 26)
        img = pygame.image.load("box.png")
        data.screen.blit(img, (23, 83))
        rect, color, rect4 = (41, 160, 312, 107), (0, 0, 0), (644, 455, 333, 71)
        text = "Use these buttons to play and pause to control the waves."
        drawTextRect(data.screen, text, color, rect, font)
        rect1, rect2, rect3 = (644, 94, 333, 133), (644, 143, 333, 71), (644, 388, 333, 133)
        text1 = returnText(1)
        text2 = returnText(2)
        text3 = returnText(3)
        text4 = returnText(4)
        drawTextRect(data.screen, text1, color, rect1, font)
        drawTextRect(data.screen, text2, color, rect2, font)
        drawTextRect(data.screen, text3, color, rect3, font)
        drawTextRect(data.screen, text4, color, rect4, font)




def drawIntro(data):  # draws intro
    if data.introFrame == 7:
        img = pygame.image.load("starter.png")
    else:
        img = pygame.image.load("intro.png")
    data.screen.fill((0, 0, 0))  # fill screen with black first
    img = pygame.transform.scale(img, (922, 691))
    data.screen.blit(img, (167, 8))
    drawIntroText(data)


def drawIntroText(data):
    font = pygame.font.Font("pokemon_pixel_font.ttf", 40)
    color = 0, 0, 0
    if data.introFrame == 0:    text = 'Welcome to the world of POKeMON.'
    if data.introFrame == 1:    text = "My name is OAK."
    if data.introFrame == 2:
        text = "People affectionately refer to me as the POkeMON PROFESSOR."
    if data.introFrame == 3:
        text = 'This world is inhabited far and wide by creatures called POKeMON.'
    if data.introFrame == 4:
        text = 'For some people, POKeMON are pets. Others use them for battling.'
    if data.introFrame == 5:
        text = "Are you ready to start your very own POKeMON adventure?"
    if data.introFrame == 6:
        text = "First, I would like to give you your first POKeMON!"
    if data.introFrame == 7:
        text, color = "Choose a POKeMON.", (255, 255, 255)
    rect = 248, 571, 793, 104
    drawTextRect(data.screen, text, color, rect, font)



def drawDescription(item):  # draws description and pic for item
    x, y, _, _ = item.bounds
    if data.bag:
        arrow = pygame.image.load("bagArrow.png")
        arrow = pygame.transform.scale(arrow, (33, 33))
        data.screen.blit(arrow, (492, y))
    elif data.mart:
        pygame.draw.rect(data.screen, (255, 0, 0), (x - 10, y - 5, 350, 30), 2)
    color = 255, 255, 255
    rect = (379, 490, 519, 91)
    font = pygame.font.Font("pokemon_pixel_font.ttf", 28)
    drawTextRect(data.screen, item.info, color, rect, font)
    item.drawItem(data.screen)


def drawStatus(data):  # draws status of pokemon in status box
    color = 0, 0, 0
    font = pygame.font.Font("pokemon_pixel_font.ttf", 20)
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
    font = pygame.font.Font("pokemon_pixel_font.ttf", 30)
    Help = font.render("Help", True, (255, 255, 255))
    data.screen.blit(Help, (670, 27))


def drawPause():  # draws pause button
    x0, y0 = 126, 32
    width, height = 70, 70
    img = pygame.image.load("pause.png")
    img = pygame.transform.scale(img, (50, 50))
    data.screen.blit(img, (x0, y0))


def drawPlay():  # draw play button
    x0, y0 = 34, 32
    width, height = 70, 70
    img = pygame.image.load("arow.png")
    img = pygame.transform.scale(img, (50, 50))
    data.screen.blit(img, (x0, y0))


def drawMenu():  # draws menu with all buttons and text
    leftbound, width, topbound, height, color = 1020, 250, 10, 620, (255, 255, 255)
    menuStart, buttonHeight = 440, 50
    font = pygame.font.Font("pokemon_pixel_font.ttf", 40)
    party = font.render("POKeMON", True, (0, 0, 0))
    data.screen.blit(party, (leftbound + 70, 23))
    for i in range(1, 4):
        if i == data.hover:
            color = 255, 0, 0
            pygame.draw.rect(data.screen, color, (leftbound + 10,
                                                  menuStart, width - 20, buttonHeight), 2)
        menuStart += buttonHeight + 10
    font = pygame.font.Font("pokemon_pixel_font.ttf", 35)
    bag = font.render("BAG", True, (0, 0, 0))
    data.screen.blit(bag, (leftbound + 30, 440 + 10))
    evolve = font.render("EVOLVE", True, (0, 0, 0))
    data.screen.blit(evolve, (leftbound + 30, 500 + 12))
    pokemart = font.render("POKeMART", True, (0, 0, 0))
    data.screen.blit(pokemart, (leftbound + 30, 560 + 12))



# draw my party menu on the right side of game
# max number that can be added is 6, just like the actual pokemon game
def drawParty():
    startY = 60
    startX = 1030
    width = 230
    height = 25
    font = pygame.font.Font("pokemon_pixel_font.ttf", 20)
    for i in range(len(data.party)):
        pokemon = data.party[i]  # display name of each pokemon
        name = pokemon.pokemon
        pokemon.button = startX, startY, width, height
        if data.hover == pokemon or data.selected == pokemon:
            pygame.draw.rect(data.screen, (255, 0, 0), (pokemon.button), 1)
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


# Source for drawText() = http://pygame.org/wiki/TextWrap
# draws and wraps text in rect
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



def drawTowers(data):  # draw all towers on board
    for pokemon in data.party:
        if pokemon.onBoard == True:
            pokemon.drawTower(data.screen)


def loadBackground():  # load main background map
    img = pygame.image.load("TPbackground.jpg")
    data.screen.blit(img, (0, 0))


def drawGameOver(data):  # draws gameover
    font = pygame.font.Font("pokemon_pixel_font.ttf", 40)
    img = pygame.image.load("gameover.png")
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
        drawTowers(data)
        drawRadius(data)
        drawText(data)
        drawPlay()
        drawPause()
        drawMenu()
        drawParty()
        drawStatus(data)
        drawHelp(data)


# basic game structure source
# adapted from :https://www.pygame.org/docs/tut/tom/games2.html
def game():  # runs game
    init(data)
    while True:
        if data.intro == False and data.gameOver == False:
            loadBackground()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: mouse(data)
        redrawAll()
        timerFired(data)
        pygame.display.flip()


game()