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
        self.rotation = properties.get(_type).get('initial_rotation') if rotation is None else rotation
        self.velocity = properties.get(_type).get('initial_velocity') if velocity is None else velocity
        self.trans = rendering.Transform(translation=(x, y))
        self.shape = self.build_shape()

    def build_shape(self):
        img = rendering.make_circle(self.radius)
        c = properties.get(self._type).get('color')
        img.set_color(c[0], c[1], c[2])
        img.add_attr(self.trans)
        return img

    def rotate(self, cw=True):
        self.rotation += math.radians(properties.get(self._type).get('step_rotation')) * (1 if cw else -1)


class Spaceship(Entity):
    def __init__(self, x, y):
        super(Spaceship, self).__init__(x, y, _type='spaceship', rotation=0, velocity=0)
        self.acceleration = properties.get(self._type).get('initial_acceleration')

    def shoot(self):
        # generate bullet with same velocity and rotation as spaceship
        return Bullet(self.x, self.y, self.rotation, (self.velocity * 2) if (self.velocity * 2) > 0.0 else 1)

    def change_acceleration(self, inc=True):
        self.acceleration += properties.get(self._type).get('acceleration') * (1 if inc else -1)

    def advance(self):
        self.velocity += self.acceleration
        self.acceleration = 0
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
        super(Crystal, self).__init__(x, y, _type='crystal', rotation=0, velocity=0)


class Enemy(Entity):
    def __init__(self, x, y):
        super(Enemy, self).__init__(x, y, _type='enemy', rotation=0, velocity=0)

    def advance(self, target_x=0, target_y=0):
        self.velocity += properties.get(self._type).get('step_velocity')
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


def are_intersecting(p1, p2, e):
    x1, y1 = p1
    x2, y2 = p2
    r = e.radius
    # entity center
    x0 = e.x
    y0 = e.y
    # compute distance point-line
    dist = math.fabs((y2 - y1)*x0 - (x2 - x1)*y0 + x2*y1 - y2*x1) / math.sqrt(math.pow(y2 - y1, 2) + math.pow(x2 - x1, 2))
    if dist <= r:
        # make sure we're in the same quadrant
        if included(x1, x2, x0) and included(y1, y2, y0):
            return properties.get(e._type).get('value'), distance(x1, y1, e)
    return None, 0


def border_distance(x, y, theta):
    # distance from right border
    dx1 = (SCREEN_WIDTH - x) / math.cos(theta) if math.fabs(math.cos(theta)) > 1e-6 else 0.0
    # distance from left border
    dx2 = (x - 0) / math.cos(theta) if math.fabs(math.cos(theta)) > 1e-6 else 0.0
    # distance from lower border
    dy1 = (y - 0) * math.sin(theta)
    # distance from upper border
    dy2 = (SCREEN_HEIGHT - y) * math.sin(theta)
    # compute distance to closest borders
    return math.sqrt(math.pow(min(dx1, dx2), 2) + math.pow(min(dy1, dy2), 2))


def distance(x, y, e):
    return math.sqrt(math.pow(e.x - x, 2) + math.pow(e.y - y, 2))


def included(a, b, v):
    return a <= v <= b if a <= b else b <= v <= a
