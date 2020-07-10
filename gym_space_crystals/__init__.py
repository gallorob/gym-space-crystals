from gym.envs.registration import register

register(
    id='SpaceCrystals-v0',
    entry_point='gym_space_crystals.envs:SpaceCrystalsEnv',
)