#!/anaconda3/bin/python3.6
import gym
import numpy as np
import random
import math
import matplotlib.pyplot as plt

# Initialize Environment
env = gym.make('CartPole-v1')

# Environment Parameters
max_episodes = 400  # maximum number of episodes to run the simulation
max_steps = 200  # maximum number of steps per episode/epoch/generation
steps_solved = 199  # number of steps to be considered solved
goal_streak = 100  # number of episode successes before completion

# Learning Parameters
learning_rate = {'initial': 0.5, 'decay': 0.003, 'min': 0.01}
exploration_rate = {'initial': 0.4, 'decay': 0.004, 'min': 0.001}
discount_factor = 0.99  # the importance of future rewards
# Discount factor of 0 makes the AI myopic (short-sighted) and 1 makes the AI
# strive for long term rewards. In a sense, a lower discount factor means the
# AI's decision relies more on previous experience while a higher discount
# factor means he/she relies more on new experiences

# Q-learning
bins = np.array([[-0.4, -0.2, 0.0, 0.2, 0.4],  # defines the binning scheme
# applied to observations
                [-math.radians(50 / 2), math.radians(50 / 2)]],
                dtype=object)
bucket_size = (len(bins[0])+1, len(bins[1])+1)  # size of the binning buckets,
# differ for each observation types
ac_space_size = env.action_space.n  # size of the action space
Q_table = np.zeros(bucket_size + (ac_space_size,))  # initialize Q-table;
# q_table[angle, angular_velocity, action]

# Logging and Debug
exploration_log = []
learning_rate_log = []
debug = False
plot = False
num_streaks = 0


def learn():
    # Instantiating the learning related parameters
    learning_rate = get_learning_rate(0)
    exploration_rate = get_exploration_rate(0)
    learning_rate_log.append(learning_rate)
    exploration_log.append(exploration_rate)

    for episode in range(max_episodes):

        # Reset environment
        ob_space = env.reset()
        ob_space = ob_space[-2:]  # keep only angle & angular velocity

        # the initial state
        state_previous = bucketize(ob_space, bins)  # output bucketized states

        for t in range(max_steps):
            action = select_action(state_previous, exploration_rate)  # select action
            ob_space, reward, done, _ = env.step(action)  # perform action
            ob_space = ob_space[-2:]  # filter observations (angle, angular_velocity)
            state = bucketize(ob_space, bins)  # bin the observations

            # Update the Q based on the result
            max_Q = np.amax(Q_table[state])  # 'Future' value, in reality this is obtained from observations
            learned_value = reward + discount_factor * max_Q
            old_value = Q_table[state_previous + (action,)]

            Q_table[state_previous + (action,)] += (learning_rate *
                                                (learned_value - old_value))

            # Setting up for the next iteration
            state_previous = state

            # Debug
            if debug:
                print("\nEpisode = %d" % episode)
                print("t = %d" % t)
                print("Action: %d" % action)
                print("State: %s" % str(state))
                print("Reward: %f" % reward)
                print("Best Q: %f" % max_Q)
                print("Explore rate: %f" % exploration_rate)
                print("Learning rate: %f" % learning_rate)
                print("Streaks: %d" % num_streaks)
                print("")

            if t >= steps_solved:
                num_streaks += 1
                # print("Episode %d finished after %f time steps" % (episode, t))
                break
            elif done:
                # print("Episode %d finished after %f time steps" % (episode, t))
                num_streaks = 0
                break

        if num_streaks > goal_streak:
            print("Episode %d finished after %f time steps" % (episode, t))
            break

        # Update parameters
        exploration_rate = get_exploration_rate(episode)
        learning_rate = get_learning_rate(episode)
        learning_rate_log.append(learning_rate)
        exploration_log.append(exploration_rate)

    if plot:
        plt.subplot(211)
        plt.title('learning rate')
        plt.plot(learning_rate_log)
        plt.subplot(212)
        plt.title('exploration rate')
        plt.plot(exploration_log)
        plt.show()

    return Q_table


def select_action(state, exploration):
    if random.random() < exploration:
        action = env.action_space.sample()  # Select a random action
    else:
        action = np.argmax(Q_table[state])  # Select the action with the highest q
    return action


def get_exploration_rate(t):
    rate = exploration_rate['initial']-(exploration_rate['decay']*t)
    return max(exploration_rate['min'], rate)


def get_learning_rate(t):
    rate = learning_rate['initial'] - (learning_rate['decay'] * t)
    return max(learning_rate['min'], rate)


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
    Q_table_learned = learn()  # extract final Q table from learning session
    # experiment(Q_table_learned)  # perform a benchmark run with the above Q table
    # experiment_sample()
