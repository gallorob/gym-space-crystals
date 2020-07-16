import math

# -- Global variables --
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
DIAG = math.sqrt(math.pow(SCREEN_WIDTH, 2) + math.pow(SCREEN_HEIGHT, 2))
N_OBSERVATIONS = 12
BORDER_VALUE = -1
# -- Environment properties --
ENVIRONMENT = {
    'n_crystals': 7,
    'crystals_mean_1': SCREEN_WIDTH / 2,
    'crystals_std_1': SCREEN_WIDTH / 6,
    'crystals_mean_2': SCREEN_HEIGHT / 2,
    'crystals_std_2': SCREEN_HEIGHT / 6,
    'n_enemies': 4,
    'enemies_mean_1': SCREEN_WIDTH / 2,
    'enemies_std_1': SCREEN_WIDTH / 4,
    'enemies_mean_2': SCREEN_HEIGHT / 2,
    'enemies_std_2': SCREEN_HEIGHT / 4,
}
# -- Entities properties --
ENTITIES = {
    'spaceship': {
        'radius': 20,
        'initial_velocity': 0,
        'max_velocity': 5,
        'initial_acceleration': 0,
        'acceleration': 0.5,
        'initial_rotation': 0,
        'step_rotation': 10,
        'value': 0,
        'shape': 'gym_space_crystals/envs/assets/spaceship.png'
    },
    'bullet': {
        'radius': 10,
        'initial_velocity': 0,
        'step_velocity': 0,
        'max_velocity': 0,
        'initial_rotation': 0,
        'value': 1,
        'shape': 'gym_space_crystals/envs/assets/bullet.png'
    },
    'crystal': {
        'radius': 8,
        'initial_velocity': 0,
        'step_velocity': 0,
        'max_velocity': 0,
        'initial_rotation': 0,
        'value': 2,
        'shape': 'gym_space_crystals/envs/assets/crystal.png'
    },
    'enemy': {
        'radius': 20,
        'initial_velocity': 0,
        'step_velocity': 0.5,
        'max_velocity': 3,
        'initial_rotation': 0,
        'step_rotation': 15,
        'value': 3,
        'shape': 'gym_space_crystals/envs/assets/enemy.png'
    }
}
# rewards
GOT_CRYSTAL = 5
SHOT = -1e-2
KILLED_ENEMY = 10
DIED = -100
MOVED = -5e-4
COLLECTED_ALL = 200
