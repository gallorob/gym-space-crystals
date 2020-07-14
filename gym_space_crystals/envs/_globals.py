# -- Global variables --
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
N_OBSERVATIONS = 12
BORDER_VALUE = -1
# -- Entities properties --
properties = {
    'spaceship': {
        'radius': 9,
        'color': (.5, .5, .5),
        'initial_velocity': 0,
        'max_velocity': 5,
        'initial_acceleration': 0,
        'acceleration': 0.5,
        'initial_rotation': 0,
        'step_rotation': 5,
        'value': 0
    },
    'bullet': {
        'radius': 3,
        'color': (.0, 1., .0),
        'initial_velocity': 0,
        'step_velocity': 0,
        'max_velocity': 0,
        'initial_rotation': 0,
        'value': 1
    },
    'crystal': {
        'radius': 5,
        'color': (.0, .0, 1.),
        'initial_velocity': 0,
        'step_velocity': 0,
        'max_velocity': 0,
        'initial_rotation': 0,
        'value': 2
    },
    'enemy': {
        'radius': 8,
        'color': (1., .0, .0),
        'initial_velocity': 3,
        'step_velocity': 1,
        'max_velocity': 3,
        'initial_rotation': 0,
        'step_rotation': 15,
        'value': 3
    }
}