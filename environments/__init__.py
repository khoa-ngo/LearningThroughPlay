from gym.envs.registration import register

register(
    id='CartPole-v2',
    entry_point='environments.envs:CartPoleEnv',
)
