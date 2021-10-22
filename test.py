from test2 import myf

class game(object):
    def __init__(self,data,inf):
        self.x = data.size
        self.y = inf
    # def add(self):
    #     self.z = 6
    #     self.w = 9
    def show(self):
        print(self.x, " and ", self.y)


x = game(data ,4)
x.show()

for i in range(5):
    print(i)


        
