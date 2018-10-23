import matplotlib.pyplot as plt
import pandas as pd
import gym
import environments

env = gym.make('CartPole-v2')
env.reset()
n = 10000
data = []

for _ in range(n):
    data.append(env.action_space.sample())
# print(data)
data = pd.DataFrame(data=data)
data.hist()
plt.show()