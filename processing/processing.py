import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle


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
    bucket = np.empty((0, 1))
    for i in range(ob_space.size):
        bucket = np.append(bucket, np.digitize(ob_space[i], bins[i]))
    return totuple(bucket)


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
pkl_file = open('../qbrain.pkl', 'rb')
qbrain = pickle.load(pkl_file)
# print(qbrain)

qbrain_difference = np.empty(qbrain.shape)
for i in range(6):
    for j in range(3):
        qbrain_difference[i][j][0] = qbrain[i][j][0]-qbrain[i][j][1]
        qbrain_difference[i][j][1] = 0
# print(np.sign(qbrain_difference))
qbrain_difference = np.sign(qbrain_difference)
# print(qbrain_difference)
dat = np.array([[[0, 0], [0, 0], [0, 0]],
                [[-1, 0], [1, 0], [-1, 0]],
                [[1, 0], [1, 0], [-1, 0]],
                [[1, 0], [-1, 0], [-1, 0]],
                [[1, 0], [-1, 0], [-1, 0]],
                [[0, 0], [0, 0], [0, 0]]])
qbrain_pseudo = np.array(dat)
qbrain_pseudo = qbrain_pseudo * -1
# print(qbrain_pseudo)
# print(qbrain)

bins = np.array([[-90000, -45000, 0, 45000, 90000], [-1, 1]])
angle = np.array(angle)
action_ai = np.empty(len(angle))
action_ai_difference = np.empty(len(angle))
action_ai_pseudo = np.empty(len(angle))

SPEED = 70
for i in range(len(angle)):
    ob_space = np.array([int(angle[i]), int(rate[i])])
    ob_space = bucketize(ob_space, bins=bins)
    action_ai_entry = select_action(state=ob_space, Q_table=qbrain) * SPEED
    action_ai[i] = action_ai_entry
    action_ai_difference_entry = select_action(state=ob_space, Q_table=qbrain_difference) * SPEED
    action_ai_difference[i] = action_ai_difference_entry
    action_ai_pseudo_entry = select_action(state=ob_space, Q_table=qbrain_pseudo) * SPEED
    action_ai_pseudo[i] = action_ai_pseudo_entry
ai_error = action_ai_difference - action
# print(action_ai)
# Process imported data
rate = np.array(rate)
action = np.array(action)
action_predicted = np.array(action_predicted)

# Plotting
data = {'angle': angle,
        'rate': rate,
        'action': action,
        'action_predicted': action_predicted,
        'action_ai': action_ai,
        'action_ai_difference': action_ai_difference,
        'action_ai_pseudo': action_ai_pseudo,
        'ai_error': ai_error}

data = pd.DataFrame(data=data)

fig, axes = plt.subplots(nrows=2, ncols=2)
data.plot.scatter(x='angle',
                  y='rate',
                  c='action',
                  alpha=0.2,
                  title='action',
                  colormap='viridis',
                  ax=axes[0, 0])
data.plot.scatter(x='angle',
                  y='rate',
                  c='action_predicted',
                  alpha=0.2,
                  title='action_predicted',
                  colormap='viridis',
                  ax=axes[0, 1])
data.plot.scatter(x='angle',
                  y='rate',
                  c='action_ai_pseudo',
                  title='action_ai_pseudo',
                  alpha=0.2,
                  colormap='viridis',
                  ax=axes[1, 0])
data.plot.scatter(x='angle',
                  y='rate',
                  c='ai_error',
                  title='ai_error',
                  alpha=0.2,
                  colormap='viridis',
                  ax=axes[1, 1])
# print(data)
# print(data)
plt.show()
pkl_file.close()
