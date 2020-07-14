import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from gym_space_crystals.envs._entities import *


def init_scene(env: gym.Env):
    del env.spaceship
    del env.crystals
    del env.enemies
    del env.bullets

    env.spaceship = Spaceship(100, 100)
    env.crystals = [
        Crystal(300, 300)
    ]
    env.enemies = [
        Enemy(300, 100),
        Enemy(300 + 100*math.cos(math.radians(30)), 200 + 100*math.sin(math.radians(30)))
                   ]
    env.bullets = [Bullet(200, 100),
                   ]


class SpaceCrystalsEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(np.zeros((N_OBSERVATIONS, 2)),
                                            np.ones((N_OBSERVATIONS, 2)) * max(SCREEN_WIDTH, SCREEN_HEIGHT),
                                            dtype=np.float64)
        self.state = None
        self.dtheta = math.radians(360 / N_OBSERVATIONS)
        self.done = False

        self.spaceship = None
        self.crystals = []
        self.enemies = []
        self.bullets = []

        self.actions = {
            0: self.accelerate,
            1: self.decelerate,
            2: self.rotate_cw,
            3: self.rotate_ccw,
            4: self.shoot
        }

        self.viewer = None
        self.seed()
        init_scene(self)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action: int):
        # apply action
        if action is not None:
            self.actions.get(action)()

        # update positions
        self.spaceship.advance()
        for bullet in self.bullets:
            bullet.advance()
            self.check_bounds(bullet, self.bullets)
        for enemy in self.enemies:
            enemy.advance(self.spaceship.x, self.spaceship.y)
            self.check_bounds(enemy, self.enemies)

        # remove enemies if hit by bullet
        # todo

        self.make_observations()

        return self.state, 0, False, {}

    def reset(self):
        init_scene(self)
        # compute obs
        self.make_observations()
        return self.state

    def render(self, mode='human'):
        if self.viewer is None:
            self.viewer = rendering.Viewer(SCREEN_WIDTH, SCREEN_HEIGHT)
            # add spaceship
            self.viewer.add_geom(self.spaceship.shape)
            # add crystals
            for crystal in self.crystals:
                self.viewer.add_geom(crystal.shape)
            # add enemies
            for enemy in self.enemies:
                self.viewer.add_geom(enemy.shape)
            # add bullets
            for bullet in self.bullets:
                self.viewer.add_geom(bullet.shape)

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

# -- Sugar coding functions

    def check_bounds(self, entity: Entity, arr: list):
        if entity.x >= SCREEN_WIDTH or entity.y >= SCREEN_HEIGHT:
            arr.remove(entity)
            self.viewer.geoms.remove(entity.shape)

# -- Interacting with the environment --

    def make_observations(self):
        # reset state
        self.state = np.zeros((N_OBSERVATIONS, 2))
        # reference arrays for quicker computations
        crystals = self.crystals.copy()
        enemies = self.enemies.copy()
        # make observations
        for i in range(N_OBSERVATIONS):
            x = self.spaceship.x + (max(SCREEN_HEIGHT, SCREEN_WIDTH)) * math.cos(self.spaceship.rotation + i * self.dtheta)
            y = self.spaceship.y + (max(SCREEN_HEIGHT, SCREEN_WIDTH)) * math.sin(self.spaceship.rotation + i * self.dtheta)
            # check for crystals
            for crystal in crystals:
                t, d = are_intersecting((self.spaceship.x, self.spaceship.y), (x, y), crystal)
                if t is not None:
                    self.state[i] = np.array([t, d])
                    crystals.remove(crystal)
            # check for enemies
            for enemy in enemies:
                t, d = are_intersecting((self.spaceship.x, self.spaceship.y), (x, y), enemy)
                if t is not None:
                    if self.state[i][0] != 0:
                        if self.state[i][1] > d:
                            self.state[i] = np.array([t, d])
                            enemies.remove(enemy)
                    else:
                        self.state[i] = np.array([t, d])
                        enemies.remove(enemy)
            # else, set border distance
            if self.state[i][0] == 0.0:
                self.state[i][0] = BORDER_VALUE
                self.state[i][1] = border_distance(self.spaceship.x, self.spaceship.y, self.spaceship.rotation + i * self.dtheta)

# -- Spaceship's actions --

    def accelerate(self):
        self.spaceship.change_acceleration()

    def decelerate(self):
        self.spaceship.change_acceleration(inc=False)

    def rotate_cw(self):
        self.spaceship.rotate()

    def rotate_ccw(self):
        self.spaceship.rotate(cw=False)

    def shoot(self):
        bullet = self.spaceship.shoot()
        self.bullets.append(bullet)
        self.viewer.add_geom(bullet.shape)
