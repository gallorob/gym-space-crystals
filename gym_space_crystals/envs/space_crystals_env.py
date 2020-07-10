import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from gym_space_crystals.envs._entities import *


def init_scene(env):
    del env.spaceship
    del env.crystals
    del env.enemies
    del env.bullets

    env.spaceship = Spaceship(30, 50)
    env.crystals = [Crystal(300, 200)]
    env.enemies = [Enemy(100, 300)]
    env.bullets = [Bullet(200, 100)]


class SpaceCrystalsEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(np.zeros(12), np.ones(12) * 10,  dtype=np.float64)

        self.spaceship = None
        self.crystals = []
        self.enemies = []
        self.bullets = []

        self.viewer = None
        self.seed()
        init_scene(self)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        # move spaceship
        self.spaceship.advance()
        # move enemies
        for enemy in self.enemies:
            enemy.advance()
        # move bullets
        for bullet in self.bullets:
            bullet.advance()
        return [], 0, False, {}

    def reset(self):
        init_scene(self)
        # compute obs
        # return obs

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
