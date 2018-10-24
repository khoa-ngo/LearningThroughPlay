import gym
import environments
import numpy as np
from time import sleep
from nec import EpisodicAgent
import core


def updateObNoise():
    noise_level = 0.0
    return np.array((core.getRandomFloat(1-noise_level, 1 + noise_level),
                    core.getRandomFloat(1-noise_level, 1 + noise_level),
                    core.getRandomFloat(1-noise_level, 1 + noise_level),
                    core.getRandomFloat(1-noise_level, 1 + noise_level),))


env = gym.make('CartPole-v2')
agent = EpisodicAgent(env.action_space)
obs = env.reset()

episode_count = 100
max_steps = 200
reward = 0
done = False
running_reward = 0
happiness = 0
force_scalar = 300

noise = 0.0  # uniform

for i in range(episode_count):
    ob = env.reset()
    # ob = np.multiply(ob, updateObNoise())
    ob = ob[2:]
    sum_reward = 0
    for j in range(max_steps):
        # env.render()
        action = agent.act(ob, reward, done, happiness, discreet=False)
        action += (noise * ((np.random.random() - 0.5) * 2)) * action
        action = action * force_scalar
        ob, reward, done, _ = env.step(action)
        # ob = np.multiply(ob, updateObNoise())
        ob = ob[2:]
        sum_reward += reward
        if done:
            break
    running_reward = running_reward * 0.5 + sum_reward * 0.5
    happiness = running_reward
    print('%d\trunning reward: %f\treward: %f' % (i, running_reward, sum_reward))
    if running_reward > 199.99:
        print('no of episodes: %d ' % (i))
        break

env.close()
