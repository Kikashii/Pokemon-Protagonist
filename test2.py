from test import game

class Struct(object):  # inherited from object which is base class. In python 3.x, If we don't write object it will also work
    pass  # null statement. Doesn't do anything.


data = Struct()

data.size = 4

def myf():
    return(data.size)
    



for i in range(5):
    data.enemies.append(game(data,i))

