import numpy as np

def run_episode(env, parameters, episode_length=500, render=1):
    observation = env.reset()
    totalreward = 0
    for _ in range(episode_length):
        action = 0 if np.matmul(parameters, observation) < 0 else 1
        observation, reward, done, info = env.step(action)
        totalreward += reward
        if render:
            env.render()
        if done:
            break
    return totalreward