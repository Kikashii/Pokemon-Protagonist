from init import *


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
        self.size = data.pokemonSize
        self.button = None  # if is pressed to see status, items, etc
        image = pygame.image.load("Assets/%s.png" % self.pokemon)  # get image
        self.img = pygame.transform.scale(image, (self.size * 2, self.size * 2))
