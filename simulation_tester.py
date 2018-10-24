import gym
import environments
import numpy as np
from time import sleep
from nec import EpisodicAgent
import math
import core
env = gym.make('CartPole-v2')
agent = EpisodicAgent(env.action_space)
obs = env.reset()

episode_count = 1
max_steps = 200
reward = 0
done = False
running_reward = 0
happiness = 0


def updateObNoise():
    noise_level = 1
    return np.array((core.getRandomFloat(1-noise_level, 1 + noise_level),
                    core.getRandomFloat(1-noise_level, 1 + noise_level),
                    core.getRandomFloat(1-noise_level, 1 + noise_level),
                    core.getRandomFloat(1-noise_level, 1 + noise_level),))


action_noise = 0.15  # uniform
p_angle = 90
p_rate = 10
p_distance = 60

for i in range(episode_count):
    ob = env.reset()
    ob = np.multiply(ob, updateObNoise())
    sum_reward = 0
    for j in range(max_steps):
        env.render()
        ob_new = np.array((ob[0], ob[1], math.degrees(ob[2]), math.degrees(ob[3])))
        action = p_distance * ob_new[0] + p_angle * ob_new[2] + p_rate * ob_new[3]
        action = min(100, max(action, -100))
        action += (action_noise * ((np.random.random() - 0.5) * 2)) * action
        print(action)
        ob, reward, done, _ = env.step(action)
        print(" ")
        print(ob)
        ob = np.multiply(ob, updateObNoise())
        print(ob)
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
