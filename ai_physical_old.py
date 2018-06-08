import time
import serial
import sys
import numpy as np
import core
import qlearn_old
import atexit

print("Initializing learning algorithm parameters...", end="  ", flush=True)
# Environment Parameters
max_episodes = 100 # maximum number of episodes to run the simulation
max_steps = 100  # maximum number of steps per episode/epoch/generation
steps_solved = max_steps-1  # number of steps to be considered solved
goal_streak = 5  # number of episode successes before completion
# Learning Parameters
learning_rate_param = {'initial': 0.4, 'decay': 0.000, 'min': 0.00}  # default: 0.5, 0.003, 0.01
exploration_rate_param = {'initial': 0.6, 'decay': 0.004, 'min': 0.001}  # default: 0.4, 0.004, 0.001

# tried the following:
# [0.4, 0.0, 0.0]; [0.4, 0.004, 0.001]; speed = 75
# [0.4, 0.0, 0.0]; [0.8, 0.004, 0.001]; speed = 75
# [0.4, 0.0, 0.0]; [1.8, 0.004, 0.001]; speed = 75
# [0.4, 0.0, 0.0]; [0.4, 0.004, 0.001]; speed = 90
# [0.4, 0.0, 0.0]; [0.4, 0.004, 0.001]; speed = 85
# [0.4, 0.0, 0.0]; [0.6, 0.004, 0.001]; speed = 85

discount_factor = 0.99  # the importance of future rewards
# Q-learning
bins = np.array([[-0.5, -0.25, 0.0, 0.25, 0.5],  # defines the binning scheme applied to observations
                 [-0.25, 0.25]],
                dtype=object)
bucket_size = (len(bins[0]) + 1, len(bins[1]) + 1)  # size of the binning buckets, differ for each observation types
ac_space_size = 2  # size of the action space
print("[SUCCESSFUL]")

print("Estalishing communication...", end="  ", flush=True)
# Communication Parameters
SERIALPORT = "COM4"
baudrate = 38400

time.sleep(2)  # Pause to stabilize Arduino
# Arduino is reset when a new serial connection is established

# Establish Serial Communication with Arduino
try:
    ser = serial.Serial(SERIALPORT, baudrate)
except serial.SerialException:
    print("Connection failed, please check port.")
    sys.exit()

print("[SUCCESSFUL]")

# Logging
time_start = None
entry = []
filename = 'log.csv'

time_start = time.time()

log = 1
if log:
    core.log_initialize(filename)


def learn(Q_table):
    print("Learning session started")
    # Get initial learning parameters
    learning_rate = qlearn_old.get_learning_rate(0, learning_rate_param)
    exploration_rate = qlearn_old.get_exploration_rate(0, exploration_rate_param)

    # Initial values
    num_streaks = 0

    for episode in range(max_episodes):
        # reset environment
        total_reward = 0
        # print("sending")
        action = 2  # initial action
        observation, reward, done, _ = core.step(action, ser)  # 'reset' environment
        # log data
        if log:
            core.log_make_entry(entry, time.time(),
                                action, observation, reward, done,
                                learning_rate, exploration_rate, episode, 0)  # t=0 because this is initial time
        observation = observation[-2:]  # keep only angle & angular velocity
        state_previous = qlearn_old.bucketize(observation, bins)  # output bucketized states

        for t in range(1, max_steps):
            # print("sending")
            action = qlearn_old.select_action(state_previous, exploration_rate, Q_table)  # select action
            observation, reward, done, _ = core.step(action, ser)  # perform action

            # log data
            if log:
                core.log_make_entry(entry, time.time(), action, observation, reward, done,
                                    learning_rate, exploration_rate, episode, t)

            observation = observation[-2:]  # filter observations (angle, angular_velocity)
            state = qlearn_old.bucketize(observation, bins)  # bin the observations

            if t >= steps_solved:
                num_streaks += reward
                print("Episode %d finished after %f time steps with total reward %d" % (episode, t, total_reward))
                break
            if done:
                num_streaks = 0
                print("Episode %d finished after %f time steps with total reward %d" % (episode, t, total_reward))
                break

            # Update the Q based on the result
            max_Q = np.amax(Q_table[state])  # 'Future' value, in reality this is obtained from observations
            learned_value = reward + discount_factor * max_Q
            old_value = Q_table[state_previous + (action,)]
            Q_table[state_previous + (action,)] += (learned_value - old_value) * learning_rate

            # Setting up for the next iteration
            total_reward += reward
            state_previous = state

        # Episode ends, check for number of streaks and update parameters
        if num_streaks >= goal_streak:
            # print("Episode %d finished after %f time steps with total reward %d" % episode, t, total_reward)
            break
        exploration_rate = qlearn_old.get_exploration_rate(episode, exploration_rate_param)
        learning_rate = qlearn_old.get_learning_rate(episode, learning_rate_param)

    # Training ends
    core.step(2, ser)
    return Q_table


def end_training():
    core.log_write_entry(filename, entry)
    core.step(2, ser)
    print("[system deactivated]")


if __name__ == "__main__":
    Q_table = np.zeros(bucket_size + (ac_space_size,))  # clear Q table
    Q_table = learn(Q_table)
    print("")

    print("Final Q-table")
    # print(Q_table)

    print("")
    atexit.register(end_training)
    sys.exit()
