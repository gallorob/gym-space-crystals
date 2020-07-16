# gym-space-crystals
The Space Crystal environment is an [OpenAI gym](https://gym.openai.com/) environment for reinforcement learning. No additional libraries were used.

Loosely inspired by the [Crystal Quest](https://www.mobygames.com/game/crystal-quest_) game for MacOS and other platforms.

## Characteristics
### The environment
In the environment you control a spaceship equipped with unlimited ammo. In the scene you have to collect crystals and avoid being swarmed by the aliens.

#### The spaceship 
![The spaceship](gym_space_crystals/envs/assets/spaceship.png?raw=true)

The spaceship has the following actions (this is the discrete action space):
1. Accelerate
2. Decelerate
3. Rotate clockwise
4. Rotate counterclockwise
5. Shoot

When moving, the spaceship can collect the crystals that lie randomly in the environment.
When shooting, a bullet is created such that it has the same orientation of the spaceship and double its velocity (if the spaceship is moving, otherwise it has a default velocity).
When the spaceship crashes against an enemy, it dies.

The spaceship can see what's around it at different angle intervals (`360 / N_OBSERVATIONS`); this makes up the observation space.

#### The enemy
![The spaceship](gym_space_crystals/envs/assets/enemy.png?raw=true)

The enemy spaceship always tries to get to the spaceship, destroying it.

## Preview

An example of the environment using a random agent for 1000 steps:

![GIF or random agent](gym_space_crystals/docs/random_agent.gif?raw=true)

## Setup
Clone the repo to your disk.

Move to the right directory by
```bash
cd gym-space-crystals
```

Make sure you have all the necessary libraries by running
```bash
pip install -r requirements.txt
```

Install by running
```bash
pip install -e .
```

## Additional notes
Future updates for curriculum learning & open-endedness compatibility are planned. Learn more about this [here](https://eng.uber.com/poet-open-ended-deep-learning/).

PR are welcome 😀.