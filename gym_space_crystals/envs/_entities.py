from gym_space_crystals.envs._globals import *
from gym.envs.classic_control import rendering
import math
import random

# -- Entities --


class Entity:
    def __init__(self, x, y, ent, rotation=None, velocity=None):
        self.x = x
        self.y = y
        self.ent = ent
        self.radius = properties.get(ent).get('radius')
        self.rotation = properties.get(ent).get('rotation') if rotation is None else rotation
        self.velocity = properties.get(ent).get('velocity') if velocity is None else velocity
        self.trans = rendering.Transform(translation=(x, y))
        self.shape = self.build_shape()

    def build_shape(self):
        img = rendering.make_circle(self.radius)
        c = properties.get(self.ent).get('color')
        img.set_color(c[0], c[1], c[2])
        img.add_attr(self.trans)
        return img

    def rotate(self, cw=True):
        self.rotation += math.radians(SS_ROTATION) * (1 if cw else -1)


class Spaceship(Entity):
    def __init__(self, x, y):
        super(Spaceship, self).__init__(x, y, ent='spaceship')

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


class Bullet(Entity):
    def __init__(self, x, y, rotation=0, velocity=1):
        super(Bullet, self).__init__(x, y, ent='bullet', rotation=rotation, velocity=velocity)

    def advance(self):
        self.x += math.cos(self.rotation) * self.velocity
        self.y += math.sin(self.rotation) * self.velocity
        self.trans.set_translation(self.x, self.y)


class Crystal(Entity):
    def __init__(self, x, y):
        super(Crystal, self).__init__(x, y, ent='crystal')


class Enemy(Entity):
    def __init__(self, x, y):
        super(Enemy, self).__init__(x, y, ent='enemy')

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
