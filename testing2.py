import gym
import environments
import numpy as np
from time import sleep
from nec import EpisodicAgent

# env = gym.make('CartPole-v1')
env = gym.make('CartPole-v2')
obs = env.reset()
agent = EpisodicAgent(env.action_space)

# for step in range(200):
#     env.render()
#     action = env.action_space.sample()
#     observation, reward, done, info = env.step(action)
#     print("angle: {:7.0f}\trate: {:7.0f}\treward: {:5.0f}\tdone: {}".\
#           format(np.rad2deg(observation[2]),np.rad2deg(observation[3]),reward,done))
#     if done:
#         break

episode_count = 120
max_steps = 200
reward = 0
done = False
sum_reward_running = 0
last_episode_reward = 0
cumulative_reward = 0

for i in range(episode_count):
    ob = env.reset()
    ob = ob[2:]
    sum_reward = 0
    for j in range(max_steps):
        # env.render()
        action = agent.act(ob, reward, last_episode_reward, done)
        # print(action)
        # sleep(0.1)
        ob, reward, done, _ = env.step(action)
        ob = ob[2:]
        sum_reward += reward
        if done:
            last_episode_reward = sum_reward_running
            break
    sum_reward_running = sum_reward_running * 0.95 + sum_reward * 0.05
    # print('%d running reward: %f\treward: %f' % (i, sum_reward_running, sum_reward))
    print('%d\treward: %f' % (i, sum_reward))

# reward = 0
# done = False
# for l in range(5):
#     ob = env.reset()
#     ob = ob[2:]
#     sum_reward = 0
#     for k in range(300):
#         env.render()
#         action = agent.act(ob, 0, last_episode_reward, done)
#         ob, reward, done, _ = env.step(action)
#         ob = ob[2:]
#         sum_reward += reward
#     print('%d reward: %f' % (i, sum_reward))

env.close()