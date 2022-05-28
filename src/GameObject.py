from random import randint
from numpy import random as randnp


class GameObject:
    images = {}
    mass_by_type = {}
    screen_dimensions = None
    image_dimensions = (32, 32)

    def __init__(self, object_type, pos):
        self.pos = pos
        self.object_type = object_type
        self.speed = (randnp.normal(0, 5, 1)[0], randnp.normal(0, 5, 1)[0])

    def nextMove(self):
        """
        if randint(0, 50) == 25:
            self.speed = (randnp.normal(0, 5, 1)[0], randnp.normal(0, 5, 1)[0])
        """

        newx = self.pos[0] + self.speed[0]
        if newx > self.screen_dimensions[0] - 32 or newx < 0:
            self.speed = (-self.speed[0], self.speed[1])
            newx = self.pos[0]

        newy = self.pos[1] + self.speed[1]
        if newy > self.screen_dimensions[1] - 32 or newy < 0:
            self.speed = (self.speed[0], -self.speed[1])
            newy = self.pos[1]

        self.pos = (newx, newy)

    def xrange(self):
        return self.pos[0], self.pos[0] + self.image_dimensions[0]

    def yrange(self):
        return self.pos[1], self.pos[1] + self.image_dimensions[1]
