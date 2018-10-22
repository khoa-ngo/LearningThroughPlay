import matplotlib.pyplot as plt
import pandas as pd
import gym
import environments

env = gym.make('CartPole-v2')
env.reset()
n = 1000
data = []

for _ in range(n):
    data.append(env.action_space.sample()[0])
# print(data)
data = pd.DataFrame(data=data)
fig, axes = plt.subplots(nrows=2, ncols=2)
