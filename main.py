import math


class cell():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed = 10
        self.color = 'g'
        self.vis_dist=100

    def view(self, world):
        distances=[self.vis_dist]*360
        colors=['n']*360
        for degree in range(360):
            stop=False
            for dist in range(self.vis_dist):
                break if stop==True
                x=round(math.sin(degree)+self.x)
                y=round(math.cos(degree)+self.y)
                for object in world:
                    break if stop==True
                    if object.x == x and object.y==y:
                        distances[degree]=dist
                        colors[degree]=object.color
                        stop=True


    def decision(self,view):
        angle=0,speed=1
        return angle, speed*self.speed

world = []
world.append(cell(0,0))
world.append(cell(10,5))
