import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import shutil


# AI
def run_trial(self, env, env_param, Q_table):
    ob_space = env.reset()
    ob_space = ob_space[-2:]
    state = self.bucketize(ob_space, env_param['bins'])
    for _ in range(env_param['max_steps']):
        env.render()
        action = np.argmax(Q_table[state])
        ob_space, reward, done, _ = env.step(action)
        ob_space = ob_space[-2:]
        state = self.bucketize(ob_space, env_param['bins'])


def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return int(a)


def bucketize(ob_space, bins):
    bucket = np.empty((0,1))
    for i in range(ob_space.size):
        bucket = np.append(bucket, np.digitize(ob_space[i], bins[i]))
    return bucket


def select_action(state, Q_table):
    return np.argmax(Q_table[state])  # Select the action with the highest q


# Data properties
angle = []
angle_lim = {'min': -100000, 'max': 100000}
rate = []
rate_lim = {'min': -100, 'max': 100}
action = []
action_lim = {'min': -100, 'max': 100}
action_predicted = []
difference = []
action_ai = np.array((0,1))

# Control constants
ANGLE_RATE_RATIO = 250
ANGLE_RESPONSE = 11
GEAR_RATIO = 111

# Import Data
file = open('log1.txt', 'r')
for line in file:
    angle_entry = float(line.split()[0])
    rate_entry = float(line.split()[1])
    action_entry = float(line.split()[2])
    actionPredicted_entry = (rate_entry * ANGLE_RATE_RATIO + (angle_entry)) * ANGLE_RESPONSE / 100 / GEAR_RATIO

    angle.append(angle_entry)
    rate.append(rate_entry)
    action.append(action_entry)
    action_predicted.append(np.ceil(actionPredicted_entry))

# Process AI controls
qbrain = pd.read_csv('../qbrain')
print(qbrain)

bins = np.array([[-90000, -45000, 0, 45000, 90000], [-1, 1]])
angle = np.array(angle)
for i in range(len(angle)):
    ob_space = np.array([int(angle[i]), int(rate[i])])
    action_ai_entry = select_action(state=ob_space, Q_table=qbrain)
    action_ai = np.append(action_ai, action_ai_entry)

print(action_ai)
# Process imported data
rate = np.array(rate)
action = np.array(action)
action_predicted = np.array(action_predicted)
# print(action)
# print(action_ai)
difference = abs(action - action_ai)

# Plotting
data = {'angle': angle,
        'rate': rate,
        'action': action,
        'action_predicted': action_predicted,
        'difference': difference}

data = pd.DataFrame(data=data)

ax = data.plot.scatter(x='angle',
                       y='rate',
                       c='difference',
                       colormap='viridis')

plt.show()
# print(data)
