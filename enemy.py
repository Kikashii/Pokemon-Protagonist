from pokemon import *

class Enemy(Pokemon):
    def __init__(self, pokemon, data, x=-1, y=-1):  # index pokemon
        Pokemon.__init__(self, pokemon, data)
        self.x = x
        self.y = y
        self.exit = False  # when out of board or hp <=0
        self.loc = 0  # index of data.checkpoints
        self.img = pygame.transform.flip(self.img, True, False)
        self.setLevel(data)  # set level depending on wave number
        self.hp = self.setHP()  # set hp depending on wave number
        self.maxHp = self.hp

    def setHP(self):  # sets hp of enemies based on level
        growthHp = self.level*10
        return self.baseHp+growthHp

    def setLevel(self, data):
        # sets level of enemies with the wave number along with some random factors
        avg = data.wave*3
        num = random.randint(-2, 2)
        self.level = avg+num

    def moveEnemy(self):  # move the enemy along the path
        try:
            self.loc += data.speed
            self.x, self.y = data.checkPoints[self.loc]
            self.bounds = (self.x-self.size, self.y-self.size,
                           self.x+self.size, self.y+self.size)
        except:  # reached end
            self.exit = True  # disappears
            self.bounds = None

    # def catchEnemy(self, x, y):  # if catches enemy when pokeball mode is on
    #     x0, y0, x1, y1 = self.bounds
    #     return x > x0 and x < x1 and y > y0 and y < y1

    def drawEnemy(self, canvas):
        data.screen.blit(self.img, (self.x - self.size, self.y - self.size))
    

