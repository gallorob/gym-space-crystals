from gym_space_crystals.envs._globals import *
from gym.envs.classic_control import rendering
import math
import random

# -- Entities --


class Entity:
    def __init__(self, x, y, _type, rotation=None, velocity=None):
        self.x = x
        self.y = y
        self._type = _type
        self.radius = properties.get(_type).get('radius')
        self.rotation = properties.get(_type).get('rotation') if rotation is None else rotation
        self.velocity = properties.get(_type).get('velocity') if velocity is None else velocity
        self.trans = rendering.Transform(translation=(x, y))
        self.shape = self.build_shape()

    def build_shape(self):
        img = rendering.make_circle(self.radius)
        c = properties.get(self._type).get('color')
        img.set_color(c[0], c[1], c[2])
        img.add_attr(self.trans)
        return img

    def rotate(self, cw=True):
        self.rotation += math.radians(properties.get(self._type).get('rotation')) * (1 if cw else -1)


class Spaceship(Entity):
    def __init__(self, x, y):
        super(Spaceship, self).__init__(x, y, _type='spaceship')

    def shoot(self):
        # generate bullet with same velocity and rotation as spaceship
        return Bullet(self.x, self.y, self.rotation, self.velocity + 1)

    def advance(self):
        self.velocity += random.random() * properties.get(self._type).get('velocity')
        if self.velocity >= properties.get(self._type).get('max_velocity'):
            self.velocity = properties.get(self._type).get('max_velocity')
        self.x += math.cos(self.rotation) * self.velocity
        self.y += math.sin(self.rotation) * self.velocity
        self.trans.set_translation(self.x, self.y)


class Bullet(Entity):
    def __init__(self, x, y, rotation=0, velocity=1):
        super(Bullet, self).__init__(x, y, _type='bullet', rotation=rotation, velocity=velocity)

    def advance(self):
        self.x += math.cos(self.rotation) * self.velocity
        self.y += math.sin(self.rotation) * self.velocity
        self.trans.set_translation(self.x, self.y)


class Crystal(Entity):
    def __init__(self, x, y):
        super(Crystal, self).__init__(x, y, _type='crystal')


class Enemy(Entity):
    def __init__(self, x, y):
        super(Enemy, self).__init__(x, y, _type='enemy')

    def advance(self, target_x=0, target_y=0):
        self.velocity += random.random() * properties.get(self._type).get('velocity')
        if self.velocity >= properties.get(self._type).get('max_velocity'):
            self.velocity = properties.get(self._type).get('max_velocity')
        # update rotation towards target
        self.rotation = math.atan2(target_y - self.y, target_x - self.x)
        # update position
        self.x += math.cos(self.rotation) * self.velocity
        self.y += math.sin(self.rotation) * self.velocity
        self.trans.set_translation(self.x, self.y)


# -- Functions --

def are_intersecting(e1, e2):
    d1 = math.fabs(e1.x - e2.x)
    d2 = math.fabs(e1.y - e2.y)
    return (d1 < e1.radius or d1 < e2.radius) and (d2 < e1.radius or d2 < e2.radius)
