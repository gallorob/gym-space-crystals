from gym_space_crystals.envs._globals import *
from gym.envs.classic_control import rendering
import math
import random

# -- Entities --


class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
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
        # generate bullet with same velocity and rotation as spaceship
        return Bullet(self.x, self.y, self.rotation, self.velocity + 1)

    def advance(self):
        self.velocity += random.random() * SS_VELOCITY
        if self.velocity >= SS_MAXVEL:
            self.velocity = SS_MAXVEL
        self.x += math.cos(self.rotation) * self.velocity
        self.y += math.sin(self.rotation) * self.velocity
        self.trans.set_translation(self.x, self.y)


class Bullet:
    def __init__(self, x, y, rotation=0, velocity=1):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.velocity = velocity
        self.radius = B_RADIUS
        self.trans = rendering.Transform(translation=(x, y))
        self.shape = self.build_shape()

    def build_shape(self):
        img = rendering.make_circle(self.radius)
        img.set_color(B_COLOR[0], B_COLOR[1], B_COLOR[2])
        img.add_attr(self.trans)
        return img

    def advance(self):
        self.x += math.cos(self.rotation) * self.velocity
        self.y += math.sin(self.rotation) * self.velocity
        self.trans.set_translation(self.x, self.y)


class Crystal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = C_RADIUS
        self.trans = rendering.Transform(translation=(x, y))
        self.shape = self.build_shape()

    def build_shape(self):
        img = rendering.make_circle(self.radius)
        img.set_color(C_COLOR[0], C_COLOR[1], C_COLOR[2])
        img.add_attr(self.trans)
        return img


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.rotation = 0
        self.radius = E_RADIUS
        self.trans = rendering.Transform(translation=(x, y))
        self.shape = self.build_shape()

    def build_shape(self):
        img = rendering.make_circle(self.radius)
        img.set_color(E_COLOR[0], E_COLOR[1], E_COLOR[2])
        img.add_attr(self.trans)
        return img

    def rotate(self, cw=True):
        self.rotation += math.radians(SS_ROTATION) * (1 if cw else -1)

    def advance(self, target_x=0, target_y=0):
        if self.x == target_x and self.y == target_y:
            return
        self.velocity += random.random() * E_VELOCITY
        if self.velocity >= E_MAXVEL:
            self.velocity = E_MAXVEL
        # update rotation towards target
        to_rotate = math.atan2(target_y - self.y, target_x - self.x)
        if to_rotate >= math.radians(E_ROTATION):
            to_rotate = math.radians(E_ROTATION)
        self.rotation = to_rotate
        # update position
        self.x += math.cos(self.rotation) * self.velocity
        self.y += math.sin(self.rotation) * self.velocity
        self.trans.set_translation(self.x, self.y)


# -- Functions --

def are_intersecting(e1, e2):
    d1 = math.fabs(e1.x - e2.x)
    d2 = math.fabs(e1.y - e2.y)
    return (d1 < e1.radius or d1 < e2.radius) or (d2 < e1.radius or d2 < e2.radius)
