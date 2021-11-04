def setPokemonData():  # some sample pokemons for testing
    # pokemon=type,stage,next pokemon to evolve into
    pokemons = dict()
    pokemons[1] = ("Bulbasaur", "grass", 1, 2, 45, 57, 57, 16)
    pokemons[5] = ("Charmander", "fire", 1, 5, 39, 56, 47, 16)
    pokemons[10] = ("Squirtle", "water", 1, 8, 44, 49, 65, 16)
    pokemons[15] = ("Pidgey", "flying", 1, 17, 40, 40, 37, 18)
    pokemons[20] = ("Rattata", "normal", 1, 20, 30, 41, 35, 20)
    return pokemons


# d[element] = 2D list:not very effective,super effective,no effect
def elementsChart():
    d = dict()
    d["fire"] = [["fire", "water", "rock", "dragon"],
                 ["grass", "ice", "bug", "steel"], None]
    d["normal"] = [["rock", "steel"], None, ["ghost"]]
    d["water"] = [['water', 'grass', 'dragon'], ['fire', 'ground', 'rock'], None]
    d['electric'] = [['electric', 'grass', 'dragon'], ['water', 'flying'],
                     ['ground']]
    d['grass'] = [['fire', 'grass', 'poison', 'flying', 'bug', 'dragon', 'steel'],
                  ['water', 'ground', 'rock'], None]
    d['poison'] = [['poison', 'ground', 'rock', 'ghost'], ['grass'], ['steel']]
    d['flying'] = [['electric', 'rock', 'steel'], ['grass', 'fighting', 'bug'], None]
    d['bug'] = [['fire', 'fighting', 'poison', 'flying', 'ghost', 'steel'],
                ['grass', 'dark', 'psychic'], None]
    d['ghost'] = [['dark'], ['psychic', 'ghost'], ['normal']]
    d['dragon'] = [['steel'], ['dragon'], None]
    return d
