import math
from typing import Tuple

from gym.envs.classic_control import rendering
from gym.envs.classic_control.rendering import Geom

from gym_space_crystals.envs._globals import *


# -- Entities --


class Entity:
    def __init__(self, x: float, y: float, _type: str, rotation: float = None, velocity: float = None):
        """
        Create a generic entity

        :param x: The X coordinate
        :param y: The Y coordinate
        :param _type: The entity's type
        :param rotation: The initial rotation
        :param velocity: The initial velocity
        """
        self.x = x
        self.y = y
        self._type = _type
        self.radius = ENTITIES.get(_type).get('radius')
        self.rotation = ENTITIES.get(_type).get('initial_rotation') if rotation is None else rotation
        self.velocity = ENTITIES.get(_type).get('initial_velocity') if velocity is None else velocity
        self.trans = rendering.Transform(translation=(x, y))
        self.shape = self.build_shape()

    def build_shape(self) -> Geom:
        """
        Build the entity's shape

        :return: A Geom object for the renderer
        """
        img = rendering.Image(ENTITIES.get(self._type).get('shape'), self.radius, self.radius)
        # workaround to get the image colors to render correctly (https://github.com/openai/gym/issues/1994)
        img.set_color(1., 1., 1.)
        img.add_attr(self.trans)
        return img

    def rotate(self, cw: bool = True):
        """
        Rotate the entity by its step_rotation angle

        :param cw: Rotate clockwise if True, else counterclockwise
        """
        self.rotation += math.radians(ENTITIES.get(self._type).get('step_rotation')) * (1 if cw else -1)
        self.trans.set_rotation(self.rotation)


class Bullet(Entity):
    def __init__(self, x: float, y: float, rotation: float = 0.0, velocity: float = 1.0):
        """
        Create a bullet

        :param x: The X coordinate
        :param y: The Y coordinate
        :param rotation: The initial rotation
        :param velocity: The initial velocity
        """
        super(Bullet, self).__init__(x, y, _type='bullet', rotation=rotation, velocity=velocity)
        self.trans.set_rotation(self.rotation)

    def advance(self):
        """
        Update the bullet's position.

        The motion is at constant velocity at a constant angle
        """
        self.x += math.cos(self.rotation) * self.velocity
        self.y += math.sin(self.rotation) * self.velocity
        self.trans.set_translation(self.x, self.y)


class Spaceship(Entity):
    def __init__(self, x: float, y: float):
        """
        Create a spaceship

        :param x: The X coordinate
        :param y: The Y coordinate
        """
        super(Spaceship, self).__init__(x, y, _type='spaceship', rotation=0, velocity=0)
        self.acceleration = ENTITIES.get(self._type).get('initial_acceleration')

    def shoot(self) -> Bullet:
        """
        Generate bullet with same rotation as spaceship and with double the spaceship's velocity if it's moving, else 1.

        """
        return Bullet(self.x, self.y, self.rotation, (self.velocity * 2) if (self.velocity * 2) > 0.0 else 1)

    def change_acceleration(self, inc: float = True):
        """
        Change the spaceship acceleration

        :param inc: Increment or Decrement the acceleration
        """
        self.acceleration += ENTITIES.get(self._type).get('acceleration') * (1 if inc else -1)

    def advance(self):
        """
        Update the spaceship position.

        The motion is resets the acceleration at each step, simulating a motion in outer space.
        """
        self.velocity += self.acceleration
        self.acceleration = 0
        if self.velocity >= ENTITIES.get(self._type).get('max_velocity'):
            self.velocity = ENTITIES.get(self._type).get('max_velocity')
        self.x += math.cos(self.rotation) * self.velocity
        self.y += math.sin(self.rotation) * self.velocity
        self.trans.set_translation(self.x, self.y)


class Crystal(Entity):
    def __init__(self, x: float, y: float):
        """
        Create a crystal

        :param x: The X coordinate
        :param y: The Y coordinate
        """
        super(Crystal, self).__init__(x, y, _type='crystal', rotation=0, velocity=0)


class Enemy(Entity):
    def __init__(self, x: float, y: float):
        """
        Create an enemy

        :param x: The X coordinate
        :param y: The Y coordinate
        """
        super(Enemy, self).__init__(x, y, _type='enemy', rotation=0, velocity=0)

    def advance(self, target_x : float = 0.0, target_y: float = 0.0):
        """
        Update the enemy position.

        Motion hones to a specific target point with an increasing velocity.

        :param target_x: The target point's X
        :param target_y: The target point's Y
        """
        # update velocity
        self.velocity += ENTITIES.get(self._type).get('step_velocity')
        if self.velocity >= ENTITIES.get(self._type).get('max_velocity'):
            self.velocity = ENTITIES.get(self._type).get('max_velocity')
        # update rotation towards target
        self.rotation = math.atan2(target_y - self.y, target_x - self.x)
        # update position
        self.x += math.cos(self.rotation) * self.velocity
        self.y += math.sin(self.rotation) * self.velocity
        self.trans.set_translation(self.x, self.y)
        self.trans.set_rotation(self.rotation)


# -- Functions --

def entity_intersection(e1: Entity, e2: Entity) -> bool:
    """
    Check if two entities are intersecting.
    It uses a circle-circle hitbox intersection.

    :param e1: The first entity
    :param e2: The second entity
    :return: True if the entity are intersecting
    """
    d1 = math.fabs(e1.x - e2.x)
    d2 = math.fabs(e1.y - e2.y)
    return (d1 < e1.radius or d1 < e2.radius) and (d2 < e1.radius or d2 < e2.radius)


def line_entity_intersection(p1: Tuple[float, float], p2: Tuple[float, float], e: Entity) -> Tuple[float, float]:
    """
    Check if the line defined by two points intersect with the entity

    :param p1: The first point
    :param p2: The second point
    :param e: The entity
    :return: A tuple with the entity type and its distance from the original point, else (0.0, 0.0)
    """
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
            return ENTITIES.get(e._type).get('value'), distance(x1, y1, e)
    return 0.0, 0.0


def border_distance(x: float, y: float, theta: float) -> float:
    """
    Computes the closest distance from a point (x,y) to the window borders given the angle theta (in radians)

    :param x: The X point coordinate
    :param y:  The Y point coordinate
    :param theta: The angle (in radians)
    :return: The closest distance to the window borders
    """
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


def distance(x: float, y: float, e: Entity) -> float:
    """
    Compute the distance between a point and an entity's center

    :param x: The point's X coordinate
    :param y: The point's Y coordinate
    :param e: The entity
    :return: The distance between point and entity's center
    """
    return math.sqrt(math.pow(e.x - x, 2) + math.pow(e.y - y, 2))


def included(a: float, b: float, v: float) -> bool:
    """
    Check that v is a <= v <= b

    :param a: The lower bound
    :param b: The upper bound
    :param v: The value to check
    :return: The inclusion condition
    """
    return a <= v <= b if a <= b else b <= v <= a
