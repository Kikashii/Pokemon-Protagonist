from init import *
from classinit import *

def roundOver(data):  # check whether round is over.
    # either all enemies killed or reached end
    for enemy in data.enemies:
        if enemy.exit == False:
            return False
    return True

    
def moveAllEnemies(data):  # move all enemies along path
    if data.waveEnemies != []:  # first add wave enemy to enemy one by one
        if data.count == data.maxCount:
            newEnemy = data.waveEnemies.pop(0)
            data.enemies.append(newEnemy)
            data.count = 0
        else:
            data.count += 1  # counter for time between adding each enemy on board
    for enemy in data.enemies:
        if enemy.exit == False:
            enemy.moveEnemy()
            if enemy.exit:
                data.lives -= 1
                # if data.lives == 0:
                #     data.gameOver = True

def timerFired(data):  # general timerfired function wrap
    if data.paused == False:
        moveAllEnemies(data)
        if (data.enemies != [] and roundOver(data)):
            data.paused, data.enemies = True, []
            data.wave += 1
            setWave(data)