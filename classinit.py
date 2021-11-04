#functions depended on class and init

from enemy import *
from Myparty import *

def setWave(data):  # set enemies when play is pressed before each wave
    # list of wild pokemon by id that would appear
    wildPoke = [1,5,10,15,20]
    if data.wave % 3 == 0:
        data.speed += 1
    if data.wave % 5 == 0:
        data.num += 1
    # make list of enemies that would be appended to board
    data.waveEnemies = [Enemy(wildPoke[random.randint(0, len(wildPoke))-1], data)
                        for i in range(data.num)]


def setStarters(data):
    # append charmander, bulbasur and squirtle to set starters
    # set pokemon from database
    bulbasaur = MyParty(1, data)
    charmander = MyParty(5, data)
    squirtle = MyParty(10, data)
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


def cinit():
    setWave(data)
    setStarters(data)
