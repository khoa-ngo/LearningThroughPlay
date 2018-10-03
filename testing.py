# Check Python bit version
# import struct
# print(struct.calcsize("P") * 8)

# Print all OpenAI gym environments
import gym
import time
import environments
import numpy as np
from gym import envs
print(envs.registry.all())

environment = gym.make('CartPole-v2')
observation = environment.reset()

max_step = 20
# render = True
render = True
totalreward=0

action_predetermined = [-123,-114,-108,-102,-95,-87,-81,-77,-72,-68,-65,-62,-60,-56,-54,-51,-48,-45,-42,-39,-36]

for step in range(max_step):
    if render:
        environment.render()
        time.sleep(0.1)
    # action = environment.action_space.sample()
    action = action_predetermined[step]
    print("%f\t%f\t%d" % (observation[2], observation[3], action))
    observation, reward, done, info = environment.step(-action)
    totalreward += reward
    if done:
        break
    # print("Total reward: %d" % (totalreward))
environment.close()
# import numpy as np
# class RandomSearch:
#     def run_episode(env, parameters, episode_length=500, render=1):
#         observation = env.reset()
#         totalreward = 0
#         for _ in range(episode_length):
#             action = 0 if np.matmul(parameters, observation) < 0 else 1
#             observation, reward, done, info = env.step(action)
#             totalreward += reward
#             if render:
#                 env.render()
#             if done:
#                 break
#         return totalreward