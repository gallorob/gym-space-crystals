import gym
import numpy as np
from gym import spaces, logger
from gym.utils import seeding

from gym_space_crystals.envs._entities import *


def init_scene(env: gym.Env):
    """
    Initialize the scene for the environment

    :param env: The environment
    """
    # clean existing scene
    del env.spaceship
    del env.crystals
    del env.enemies
    del env.bullets

    # initialize the scene
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
        # all available actions
        # int -> function
        self.actions = {
            0: self.accelerate,
            1: self.decelerate,
            2: self.rotate_cw,
            3: self.rotate_ccw,
            4: self.shoot
        }

        # action space depends on number of possible actions
        self.action_space = spaces.Discrete(len(self.actions))
        # observation space
        # tuple (entity type OR border, distance) given the observation angle
        self.observation_space = spaces.Box(np.zeros((N_OBSERVATIONS, 2)),
                                            np.ones((N_OBSERVATIONS, 2)) * SCREEN_WIDTH * SCREEN_HEIGHT,
                                            dtype=np.float64)
        # current state
        self.state = None
        # incremental angle for observations
        self.dtheta = math.radians(360 / N_OBSERVATIONS)
        # flag for end of episode
        self.done = False
        # flag for executions after end of episode
        self.steps_beyond_done = None

        # scene's entities
        self.spaceship = None
        self.crystals = []
        self.enemies = []
        self.bullets = []

        # renderer
        self.viewer = None

        # random seed fixing
        self.seed(10072020)

        # initialize the scene
        init_scene(self)

    def seed(self, seed: int = None):
        """
        Fix the random seed for reproducibility
        :param seed: Random seed
        """
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action: int):
        """
        Apply a single step in the environment using the given action
        :param action: The action to apply
        """
        # sanity check for the action
        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg

        # execute the action if possible
        if not self.done:
            reward = 0.0  # todo: base value
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
            for enemy in self.enemies:
                for bullet in self.bullets:
                    if entity_intersection(enemy, bullet):
                        self.bullets.remove(bullet)
                        self.viewer.geoms.remove(bullet.shape)
                        self.enemies.remove(enemy)
                        self.viewer.geoms.remove(enemy.shape)
                        # increment reward

            # remove spaceship if out of bounds or collided with enemy
            if self.spaceship.x >= SCREEN_WIDTH or self.spaceship.y >= SCREEN_HEIGHT or self.spaceship.x <= 0.0 or self.spaceship.y <= 0.0:
                self.done = True  # terminate session
                self.viewer.geoms.remove(self.spaceship.shape)
                # decrease reward
            else:
                for enemy in self.enemies:
                    if entity_intersection(self.spaceship, enemy):
                        self.done = True  # terminate session
                        self.viewer.geoms.remove(self.spaceship.shape)
                        # decrease reward

            self.make_observations()

        # allow one more step after done
        elif self.steps_beyond_done is None:
            self.steps_beyond_done = 0
            reward = 0.0  # todo: base value

        # emit a warning for repetitions after done
        else:
            if self.steps_beyond_done == 0:
                logger.warn("You called the 'step()' function after the environment ended. Use 'reset()' when you "
                            "receive 'done = True'!")
            self.steps_beyond_done += 1
            reward = 0.0  # todo: base value

        # end of step()
        # return observations, reward, done, infos
        return self.state, 0, self.done, {}

    def reset(self):
        # reset the scene
        init_scene(self)
        self.done = False
        self.steps_beyond_done = None
        self.reset_geoms()
        # compute obs
        self.make_observations()
        return self.state

    def render(self, mode='human'):
        if self.viewer is None:
            self.viewer = rendering.Viewer(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.reset_geoms()

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

# -- Sugar coding functions

    def check_bounds(self, entity: Entity, arr: list):
        """
        Check if an entity is within the window bounds and remove it from the scene in case it is

        :param entity: The entity to check
        :param arr: The array of the entity type
        """
        if entity.x >= SCREEN_WIDTH or entity.y >= SCREEN_HEIGHT or entity.x <= 0.0 or entity.y <= 0.0:
            # remove it from the scene
            arr.remove(entity)
            # remove it from the renderer
            self.viewer.geoms.remove(entity.shape)

    def reset_geoms(self):
        """
        Reset the entities in the renderer
        """
        if self.viewer:
            self.viewer.geoms = []
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

# -- Interacting with the environment --

    def make_observations(self):
        """
        Compute all observations, updating the state
        """
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
                t, d = line_entity_intersection((self.spaceship.x, self.spaceship.y), (x, y), crystal)
                if t == 0.0:
                    self.state[i] = np.array([t, d])
                    crystals.remove(crystal)
            # check for enemies
            for enemy in enemies:
                t, d = line_entity_intersection((self.spaceship.x, self.spaceship.y), (x, y), enemy)
                if t == 0.0:
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
        """
        Accelerate the spaceship
        """
        self.spaceship.change_acceleration()

    def decelerate(self):
        """
        Decelerate the spaceship
        """
        self.spaceship.change_acceleration(inc=False)

    def rotate_cw(self):
        """
        Rotate the spaceship clockwise
        """
        self.spaceship.rotate()

    def rotate_ccw(self):
        """
        Rotate the spaceship counterclockwise
        """
        self.spaceship.rotate(cw=False)

    def shoot(self):
        """
        Shoot a bullet from the spaceship

        The bullet is added to the scene
        """
        bullet = self.spaceship.shoot()
        self.bullets.append(bullet)
        self.viewer.add_geom(bullet.shape)
