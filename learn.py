import serial
import time
import sys
import numpy as np
from core import step
from core import create_entry
from core import write_to_log
from qlearn import get_exploration_rate
from qlearn import get_learning_rate
from qlearn import bucketize
from qlearn import select_action

# Environment Parameters
max_episodes = 3  # maximum number of episodes to run the simulation
max_steps = 200  # maximum number of steps per episode/epoch/generation
steps_solved = 199  # number of steps to be considered solved
goal_streak = 5  # number of episode successes before completion

# Learning Parameters
learning_rate_param = {'initial': 0.5, 'decay': 0.003, 'min': 0.01}  # default: 0.5, 0.003, 0.01
exploration_rate_param = {'initial': 0.6, 'decay': 0.003, 'min': 0.001}  # default: 0.4, 0.004, 0.001
discount_factor = 0.99  # the importance of future rewards

# Q-learning
bins = np.array([[-1.0, -0.5, 0.0, 0.5, 1.0],  # defines the binning scheme applied to observations
                 [-1.5, 1.5]],
                dtype=object)
bucket_size = (len(bins[0]) + 1, len(bins[1]) + 1)  # size of the binning buckets, differ for each observation types
ac_space_size = 2  # size of the action space
Q_table = np.zeros(bucket_size + (ac_space_size,))  # initialize Q-table; q_table[angle, angular_velocity, action]

# Communication Parameters
SERIALPORT = "COM4"
baudrate = 19200

time.sleep(0.5)  # Pause to stabilize Arduino
# Arduino is reset when a new serial connection is established

# Logging
log = 0
if log:
    f = open('log.csv', 'w+')
    f.close()

# Establish Serial Communication with Arduino
try:
    ser = serial.Serial(SERIALPORT, baudrate)
except serial.SerialException:
    print("Connection failed, please check port.")
    sys.exit()

def learn():
    # Get initial learning parameters
    learning_rate = get_learning_rate(0, learning_rate_param)
    exploration_rate = get_exploration_rate(0, exploration_rate_param)

    # Logging and Debug
    num_streaks = 0

    for episode in range(max_episodes):
        total_reward = 0

        action = 3
        ob_space, reward, done, info = step(action, ser)  # 'reset' environment

        # log data
        if log:
            entry = create_entry(ob_space, reward, done, info)
            write_to_log(entry)

        ob_space = ob_space[-2:]  # keep only angle & angular velocity

        # initial observation
        state_previous = bucketize(ob_space, bins)  # output bucketized states

        for t in range(max_steps):
            action = select_action(state_previous, exploration_rate)  # select action
            ob_space, reward, done, info = step(action, ser)  # perform action
            total_reward += reward

            # log data
            if log:
                entry = create_entry(ob_space, reward, done, info)
                write_to_log(entry)

            ob_space = ob_space[-2:]  # filter observations (angle, angular_velocity)
            state = bucketize(ob_space, bins)  # bin the observations

            # Update the Q based on the result
            max_Q = np.amax(Q_table[state])  # 'Future' value, in reality this is obtained from observations
            learned_value = reward + discount_factor * max_Q
            old_value = Q_table[state_previous + (action,)]

            Q_table[state_previous + (action,)] += (learned_value - old_value) * learning_rate

            # Setting up for the next iteration
            state_previous = state

            if done:
                num_streaks = 0
                print("%d, %d" % (episode, total_reward))
                break
            # elif t >= steps_solved:
            #     print("%d, %f" % (episode, t))
            #     num_streaks += 1
            #     break

        if num_streaks > goal_streak:
            # print("Episode %d finished after %f time steps" % (episode, t))
            break

        # Update parameters
        exploration_rate = get_exploration_rate(episode, exploration_rate_param)
        learning_rate = get_learning_rate(episode, learning_rate_param)
    return Q_table


if __name__ == "__main__":
    Q_table_learned = learn()
    print(Q_table)
    while 1:
        step(3, ser)  # reset environment
