import gym
import environments
import numpy as np
from time import sleep
from nec import EpisodicAgent
import core
import math


def updateObNoise():
    noise_level = 0.05
    return np.array((core.getRandomFloat(1 - noise_level, 1 + noise_level, type="normal"),
                     core.getRandomFloat(1 - noise_level, 1 + noise_level, type="normal"),
                     core.getRandomFloat(1 - noise_level, 1 + noise_level, type="normal"),
                     core.getRandomFloat(1 - noise_level, 1 + noise_level, type="normal")
                     ))


env = gym.make('CartPole-v2')
agent = EpisodicAgent(env.action_space)
obs = env.reset()

episode_count = 100
max_steps = 250
reward = 0
done = False
running_reward = 0
happiness = 0
force_scalar = 200

action_noise = 0.05  # uniform
p_angle = 0
p_rate = 0
p_distance = 0

for i in range(episode_count):
    ob = env.reset()
    ob = np.multiply(ob, updateObNoise())
    ob_new = np.array((ob[0], ob[1], math.degrees(ob[2]), math.degrees(ob[3])))
    ob = ob[2:]
    sum_reward = 0
    for j in range(max_steps):
        if running_reward > max_steps-1:
            env.render()
        action = agent.act(ob, reward, done, happiness, discreet=False)  # agent action
        action *= core.getRandomFloat(1 - action_noise, 1 + action_noise, type="normal")  # action noise
        action = action * force_scalar  # force scalar
        action += p_distance * ob_new[0] + p_angle * ob_new[2] + p_rate * ob_new[3]  # PID Control
        action = min(300, max(action, -300))  # limit action
        # print(action)
        ob, reward, done, _ = env.step(action)
        ob_new = np.array((ob[0], ob[1], math.degrees(ob[2]), math.degrees(ob[3])))
        ob = np.multiply(ob, updateObNoise())
        ob = ob[2:]
        sum_reward += reward
        if done:
            break
    running_reward = running_reward * 0.5 + sum_reward * 0.5
    happiness = running_reward
    print('%d\trunning reward: %f\treward: %f' % (i, running_reward, sum_reward))
    if running_reward > max_steps-0.5:
        print('no of episodes: %d ' % (i))
        break

env.close()
