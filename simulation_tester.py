import gym
import environments
import numpy as np
from time import sleep
from nec import EpisodicAgent

env = gym.make('CartPole-v2')
agent = EpisodicAgent(env.action_space)
obs = env.reset()

episode_count = 100
max_steps = 200
reward = 0
done = False
sum_reward_running = 0
last_episode_reward = 0
happiness = 0

for i in range(episode_count):
    ob = env.reset()
    ob = ob[2:]
    sum_reward = 0
    for j in range(max_steps):
        # env.render()
        action = agent.act(ob, reward, done, happiness)
        ob, reward, done, _ = env.step(action)
        ob = ob[2:]
        sum_reward += reward
        if done:
            last_episode_reward = sum_reward_running
            break
    sum_reward_running = sum_reward_running * 0.5 + sum_reward * 0.5
    happiness = sum_reward_running
    print('%d\trunning reward: %f\treward: %f' % (i, sum_reward_running, sum_reward))

env.close()