from pokemon import *


class MyParty(Pokemon):
    # initially just in party/menu not on board
    def __init__(self, pokemon, data, level=5, x=None, y=None):
        Pokemon.__init__(self, pokemon, data)  # super
        # x and y not set until is on board
        self.x = x
        self.y = y
        self.range = 100
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

    def equation(self, x, y):  # equation for checking whether enemy is in range
        return (x - self.x) ** 2 + (y - self.y) ** 2 < self.range ** 2

    def inRange(self, bounds):  # check whether object is in radius
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

    def updateStats(self):  # update attack stats
        baseLevel = 5
        self.attack = self.attackGrowth + self.baseAttack
        self.attackGrowth = self.level - baseLevel
