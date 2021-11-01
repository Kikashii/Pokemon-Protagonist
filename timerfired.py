from init import *
from classinit import *
from hover import *
from bullet import *


def roundOver(data):  # check whether round is over.
    # either all enemies killed or reached end
    for enemy in data.enemies:
        if not enemy.exit:
            return False
    return True


def levelUp(data):  # levels up if exp hits max exp and updates stats
    for tower in data.party:
        if tower.onBoard:
            if tower.exp >= tower.maxExp:
                tower.attackGrowth += 2
                tower.exp = 0
                tower.level += 1
                tower.maxExp += 5
                tower.updateStats()


def moveAllEnemies(data):  # move all enemies along path
    if data.waveEnemies:  # first add wave enemy to enemy one by one
        if data.count == data.maxCount:
            newEnemy = data.waveEnemies.pop(0)
            data.enemies.append(newEnemy)
            data.count = 0
        else:
            data.count += 1  # counter for time between adding each enemy on board
    for enemy in data.enemies:
        if not enemy.exit:
            enemy.moveEnemy()
            if enemy.exit:
                data.lives -= 1
                # if data.lives == 0:
                #     data.gameOver = True


def moveAllBullets(data):  # moves all bullets toward set direction
    for tower in data.party:
        for bullet in tower.bullets:
            bullet.moveBullet()
            width, height = data.size
            # if goes out of bounds, remove bullets
            x0, x1, y0, y1 = data.boardBounds
            if (bullet.x > x1 or bullet.x < 0 or bullet.y > y1
                    or bullet.y < 0):
                bullet.remove = True


def removeBullets(data):
    # check whether bullets are removed for every frame and replace bullet list
    for tower in data.party:
        if tower.onBoard and tower.bullets != []:
            temp = []
            for bullet in tower.bullets:
                if not bullet.remove:
                    temp.append(bullet)
            tower.bullets = temp


def setTarget(data):  # sets target for each tower
    if data.enemies != []:
        for tower in data.party:
            if tower.onBoard:
                enemyPoke = tower.target
                # set target, either when doesnt exist or changing targets
                if (tower.target == None or not tower.inRange((enemyPoke.x,
                                                               enemyPoke.y, enemyPoke.x + 10, enemyPoke.y + 10)) or
                        tower.target.exit):
                    for enemy in data.enemies:  # loops through all enemies
                        if not enemy.exit:  # make sure enemy hasn't died yet
                            bounds = enemy.x, enemy.y, enemy.x + 10, enemy.y + 10
                            if tower.inRange(bounds):
                                # sets first enemy found as target and breaks
                                tower.target = enemy
                                break
                # sets target as None if target goes out of range or target dies
                if tower.target != None and (tower.target.exit or not
                tower.inRange((tower.target.x, tower.target.y,
                               tower.target.x + 10, tower.target.y + 10))):
                    tower.target = None


def setBullets(data):  # set bullets for towers if tower has a target
    if data.enemies:
        for tower in data.party:
            if tower.onBoard and tower.target is not None:
                if tower.counter >= tower.maxCounter:
                    target = tower.target.x, tower.target.y
                    tower.bullets.append(Bullet(tower.x, tower.y,
                                                target, tower.element))
                    tower.counter = 0  # counter for time between new bullet
                else:
                    tower.counter += 1


def shootEnemies(data):  # check whether each bullet has shot an enemy
    for tower in data.party:
        if tower.onBoard and tower.bullets != []:
            for bullet in tower.bullets:
                for enemy in data.enemies:
                    if not enemy.exit:
                        if bullet.shotEnemy(enemy):
                            enemy.hp -= setDamage(data, tower.attack,
                                                  tower.element, enemy.element)
                            bullet.remove = True
                        if enemy.hp <= 0:  # kills an enemy, gains exp and money
                            tower.exp += enemy.level * 7
                            enemy.exit = True
                            data.coins += coinAmount(enemy)


# set damage of bullet according to stats of pokemon as well as type of bullet
def setDamage(data, attack, attackType, enemyType):
    notEffective = data.elementsChart[attackType][0]
    effective = data.elementsChart[attackType][1]
    noEffect = data.elementsChart[attackType][2]
    if notEffective is not None and enemyType in notEffective:
        return int(round(attack * 0.5))
    elif effective is not None and enemyType in effective:
        return attack * 2
    elif noEffect is not None and enemyType in noEffect:
        return 0
    else:
        return attack


def coinAmount(enemy):  # amount of money depending on pokemon level
    return enemy.level * 3


def allBulletsRemoved(data):
    # check whether all bullets are removed on board
    for tower in data.party:
        if tower.onBoard and tower.bullets != []:
            for bullet in tower.bullets:
                if not bullet.remove:
                    return False
    return True


def catchPokemon(data, x, y):  # thrwos pokeball. check for enemy bouds
    data.pokeball = False
    for enemy in data.enemies:
        if enemy.exit == False and enemy.catchEnemy(x, y):
            # run possibility of catching enemy
            if runPossibility(enemy) and len(data.party) < 6:  # max party is 6
                data.party.append(MyParty(enemy.id, data, enemy.level))
                enemy.exit = True


def runPossibility(enemy):
    # algorithm calculating the possibility of catching a pokemon based on level
    poss = round((1 - (enemy.hp / enemy.maxHp) ** 2) * 100)
    if random.randint(1, 100) <= poss:
        return True


def timerFired(data):  # general timerfired function wrap
    if not data.intro:
        hover(data)
        if not data.paused:
            moveAllEnemies(data)
            setTarget(data)
            setBullets(data)
            moveAllBullets(data)
            shootEnemies(data)
            levelUp(data)
            removeBullets(data)
            if data.enemies != [] and roundOver(data) and allBulletsRemoved(data):
                data.paused, data.enemies = True, []
                data.wave += 1
                setWave(data)

    else:
        introHover(data)
