#functions depended on class and init

from enemy import *

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


def cinit():
    setWave(data)
