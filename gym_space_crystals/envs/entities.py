from gym_space_crystals.envs._globals import *
from gym.envs.classic_control import rendering
import math
import random

# -- Entities --


class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rotation = 0
        self.radius = SS_RADIUS
        self.trans = rendering.Transform(translation=(x, y))
        self.shape = self.build_shape()

    def build_shape(self):
        img = rendering.make_circle(self.radius)
        img.set_color(SS_COLOR[0], SS_COLOR[1], SS_COLOR[2])
        img.add_attr(self.trans)
        return img

    def rotate(self, cw=True):
        self.rotation += math.radians(SS_ROTATION) * (1 if cw else -1)

    def shoot(self):
        # generate bullet with same velocity as spaceship
        pass

    def advance(self):
        self.x += random.random() * SS_VELOCITY
        self.trans.set_translation(self.x, self.y)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = B_RADIUS
        self.trans = rendering.Transform(translation=(x, y))
        self.shape = self.build_shape()

    def build_shape(self):
        img = rendering.make_circle(self.radius)
        img.set_color(B_COLOR[0], B_COLOR[1], B_COLOR[2])
        img.add_attr(self.trans)
        return img

    def advance(self):
        self.x += random.random() * SS_VELOCITY
        self.trans.set_translation(self.x, self.y)


class Crystal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.l = C_LENGTH
        self.trans = rendering.Transform(translation=(x, y))
        self.shape = self.build_shape()

    def build_shape(self):
        vs = [(0, 0), (self.l, -self.l), (-self.l, -self.l)]
        img = rendering.make_polygon(vs, filled=True)
        img.set_color(C_COLOR[0], C_COLOR[1], C_COLOR[2])
        img.add_attr(self.trans)
        return img


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.l = E_SIZE
        self.trans = rendering.Transform(translation=(x, y))
        self.shape = self.build_shape()

    def build_shape(self):
        vs = [(0, 0), (self.l, 0), (self.l, self.l), (0, self.l)]
        img = rendering.FilledPolygon(vs)
        img.set_color(E_COLOR[0], E_COLOR[1], E_COLOR[2])
        img.add_attr(self.trans)
        return img

    def advance(self):
        self.x += random.random() * SS_VELOCITY
        self.trans.set_translation(self.x, self.y)
