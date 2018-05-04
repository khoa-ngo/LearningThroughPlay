import time
import sys
import gym
import numpy as np
import random
import math
import core
from joblib import Parallel
import multiprocessing


# Initialize Environment
env = gym.make('CartPole-v1')

# Environment Parameters
max_episodes = 40 # maximum number of episodes to run the simulation
max_steps = 100  # maximum number of steps per episode/epoch/generation
steps_solved = 199  # number of steps to be considered solved
goal_streak = 5  # number of episode successes before completion

# Learning Parameters
learning_rate_param = {'initial': 0.4, 'decay': 0.000, 'min': 0.00}  # default: 0.5, 0.003, 0.01
exploration_rate_param = {'initial': 0.4, 'decay': 0.004, 'min': 0.001}  # default: 0.4, 0.004, 0.001
discount_factor = 0.99  # the importance of future rewards

# Learning Parameters Experimental
# learning_rate_param_x = {'initial': 0.5, 'min': 0.1, 'decay': 27.0}
# exploration_rate_param_x = {'initial': 0.4, 'min': 0.005, 'decay': 27.0}

# Discount factor of 0 makes the AI myopic (short-sighted) and 1 makes the AI strive for long term rewards.
# In a sense, a lower discount factor means the AI's decision relies more on previous experience
# while a higher discount factor means he/she relies more on new experiences

# Q-learning
bins = np.array([[-0.2, -0.1, 0.0, 0.1, 0.2],  # defines the binning scheme applied to observations
                [-0.5, 0.5]],
                dtype=object)
bucket_size = (len(bins[0]) + 1, len(bins[1]) + 1)  # size of the binning buckets, differ for each observation types
ac_space_size = env.action_space.n  # size of the action space
# Q_table = np.zeros(bucket_size + (ac_space_size,))

# Logging
time_start = None
entry = []
filename = 'log_openai.csv'
log = 1
if log:
    core.log_initialize(filename)


def qlearn(Q_table):
    # Get initial learning parameters
    learning_rate = get_learning_rate(0, learning_rate_param)
    exploration_rate = get_exploration_rate(0, exploration_rate_param)

    # Initial values
    num_streaks = 0
    solved_episodes = 0

    # Reset Q_table
    # Q_table = np.zeros(bucket_size + (ac_space_size,))
    # initialize Q-table; q_table[angle, angular_velocity, action]

    for episode in range(max_episodes):
        # reset environment
        env.reset()
        observation, reward, done, _ = env.step(env.action_space.sample())

        t = -1
        action = -1
        if log:
            core.log_make_entry(entry, time.time(),
                                action, observation, reward, done,
                                learning_rate, exploration_rate, episode, 0)
        observation = observation[-2:]  # keep only angle & angular velocity
        state_previous = bucketize(observation, bins)  # output bucketized states

        for t in range(max_steps):
            action = select_action(state_previous, exploration_rate, Q_table)  # select action
            observation, reward, done, _ = env.step(action)  # perform action

            if log:
                core.log_make_entry(entry, time.time(), action, observation, reward, done,
                                    learning_rate, exploration_rate, episode, t)
            observation = observation[-2:]  # keep only angle & angular velocity
            state = bucketize(observation, bins)  # bin the observations

            # Update the Q based on the result
            max_Q = np.amax(Q_table[state])
            learned_value = reward + discount_factor * max_Q
            old_value = Q_table[state_previous + (action,)]
            Q_table[state_previous + (action,)] += (learned_value - old_value) * learning_rate

            # Setting up for the next iteration
            state_previous = state

            if done:
                num_streaks = 0
                print("Episode %d finished after %f time steps, done" % (episode, t))
                break
            elif t >= steps_solved:
                num_streaks += 1
                print("Episode %d finished after %f time steps, done" % (episode, t))
                break

        if num_streaks >= goal_streak or episode >= max_episodes-1:
            if num_streaks >= goal_streak:
                # print("Episode %d finished after %f time steps, solved" % (episode, t))
                solved_episodes = episode
            else:
                solved_episodes = 0
            break

        # Update parameters
        exploration_rate = get_exploration_rate(episode, exploration_rate_param)
        learning_rate = get_learning_rate(episode, learning_rate_param)

    # print("--- %s seconds ---" % (time.time() - start_time))
    core.log_write_entry(filename, entry)
    return Q_table, solved_episodes


def select_action(state, exploration, Q_table):
    if random.random() < exploration:
        action = random.randint(0, 1)  # Select a random action
    else:
        action = np.argmax(Q_table[state])  # Select the action with the highest q
    return action


def get_exploration_rate(t, param):
    rate = param['initial']-(param['decay']*t)
    return max(param['min'], rate)


def get_exploration_rate_new(t, param):
    rate = max(param['min'], min(1.0, 1.0 - math.log10((t + 1) / param['decay'])))
    return param['initial']*rate


def get_learning_rate(t, param):
    rate = param['initial'] - (param['decay'] * t)
    return max(param['min'], rate)


def get_learning_rate_new(t, param):
    rate = max(param['min'], min(1.0, 1.0 - math.log10((t + 1) / param['decay'])))
    return param['initial']*rate


def bucketize(ob_space, bins):
    bucket = np.empty(ob_space.size)
    for i in range(ob_space.size):
        bucket[i] = np.digitize(ob_space[i], bins[i])
    return totuple(bucket)


def crop(value, min_value, max_value):
    return min(max_value, max(value,min_value))


def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return int(a)


def experiment(q_table_optimized):
    ob_space = env.reset()
    ob_space = ob_space[-2:]  # keep only angle & angular velocity

    state = bucketize(ob_space, bins)  # bin the observations

    for episode in range(max_episodes):
        env.render()
        action = np.argmax(q_table_optimized[state])  # select action
        ob_space, reward, done, _ = env.step(action)
        ob_space = ob_space[-2:]  # filter observations (angle, angular_velocity)
        state = bucketize(ob_space, bins)  # bin the observations


def experiment_sample():
    env.reset()
    for episode in range(max_episodes):
        env.render()
        action = env.action_space.sample()  # select action
        ob_space, reward, done, _ = env.step(action)


if __name__ == "__main__":
    # Q_table_learned, _ = qlearn()
    # print("--- %s seconds ---" % (time.time() - start_time))

    # experiment(Q_table_learned)  # perform a benchmark run with the above Q table
    # experiment_sample()
    # print(Q_table_learned)

    # learning_rate_param = {'initial': 0.5, 'decay': 0.005, 'min': 0.01}  # default: 0.5, 0.003, 0.01
    # exploration_rate_param = {'initial': 0.5, 'decay': 0.004, 'min': 0.01}  # default: 0.4, 0.004, 0.001

    scoreboard = {}
    # Q_table = np.zeros(bucket_size + (ac_space_size,))

    # num_cores = multiprocessing.cpu_count()

    group_size = 1
    session_size = 1

    time_start = time.time()
    for _ in range(session_size):
        scoreboard = {}

        for _ in range(group_size):
            Q_table = np.zeros(bucket_size + (ac_space_size,))

            best_Q_table, solved_episodes = qlearn(Q_table)  # extract final Q table from learning session
            print(best_Q_table)

            if solved_episodes:
                scoreboard.setdefault('score', [])
                scoreboard['score'].append(solved_episodes)

        if 'score' not in scoreboard:
            print("A training session had failed")
            continue

        # arithmetic mean
        mean_score = np.mean(scoreboard['score'])
        scoreboard.setdefault('mean', [])
        scoreboard['mean'].append(float(mean_score))

        # success rate
        success_rate = float(len(scoreboard['score']))/float(group_size)
        scoreboard.setdefault('success rate', [])
        scoreboard['success rate'].append(success_rate*100.0)

        print(sorted(scoreboard.items()))

        # experiment(best_Q_table)

    sys.exit()
