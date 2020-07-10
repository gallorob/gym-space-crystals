# -- Global variables --
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
# -- Entities properties --
properties = {
    'spaceship': {
        'radius': 9,
        'color': (.5, .5, .5),
        'velocity': 5,
        'rotation': 5,
        'max_velocity': 5
    },
    'bullet': {
        'radius': 3,
        'color': (.0, 1., .0),
        'velocity': 0,
        'rotation': 0,
        'max_velocity': 0
    },
    'crystal': {
        'radius': 5,
        'color': (.0, .0, 1.),
        'velocity': 0,
        'rotation': 0,
        'max_velocity': 0
    },
    'enemy': {
        'radius': 8,
        'color': (1., .0, .0),
        'velocity': 3,
        'rotation': 5,
        'max_velocity': 3
    }
}