import gym
import numpy as np
from qlearn import QLearn
import time
from multiprocessing import cpu_count, Manager, Pool
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Create Simulated Environment and Define Environment Parameters:
environment = gym.make('CartPole-v1')
environment_param = {'max_episodes': 200, 'max_steps': 200, 'goal_score': 199, 'goal_streak': 20,
                     'bins': np.array([[-0.2, -0.175, 0.0, 0.175, 0.2], [-0.2, 0.2]], dtype=object),
                     'action_size': environment.action_space.n}
# An episode is an attempt to learn. Each episode consists of a number of timesteps. At each time step,
# we can collect observations. Once an action is chosen and executed, we proceed to the next timestep,
# obtaining a new set of observations.
# An episode is considered solved when the AI achieve a score higher or equal to goal_score.
# The problem is considered solved when the AI solved 20 episodes consecutively.

# Define Learning Parameters:
learning_rate_param = {'initial': 0.5}  # determines how much the AI learns from new experiences.
# higher learning rate means the AI learns a lot from new experiences, but also tend to forget past lessons.
# lower learning rate means they learn slower, while remembering a lot of the past lessons.

exploration_rate_param = {'initial': 0.3}  # the AI's tendency to try new things.
# higher exploration rate means the AI tend to diverge more and try newer things.
# lower exploration rate means they tend to act based on only past experiences.

discount_factor = 0.99  # The AI's patience for future rewards.
# higher discount factor makes the AI far-sighted, striving for long term rewards.
# lower discount factor makes them myopic (short-sighted), settling for immediate/short-term rewards.

# Data Visualization
plot = True
render = False


def worker(unused):
    ai = QLearn(environment_param, logging=False)  # create an instance of the AI.
    q_table, episode_count = ai.train(environment, environment_param,
                                      learning_rate_param, exploration_rate_param,
                                      discount_factor)  # train the AI.
    # scoreboard.append(episode_count)  # store amount of trials the AI took to solve the problem.
    # brain_bucket.append(q_table)  # store the brain of the trained AI in form of the Q-table.
    return episode_count, q_table


if __name__ == '__main__':
    start_time = time.time()  # start stopwatch.
    batch_size = 1  # the desired number of training sessions.
    # train the AI in batches by running multiple simutaneous processes.
    # this is done to speed up the simulation.

    # Train the AI
    scoreboard = list()
    brain_bucket = list()
    listofzeros = [0] * batch_size
    with Pool(1) as p:  # cpu_count()
        results = p.map(worker, listofzeros)

    for item in results:
        scoreboard.append(item[0])
        brain_bucket.append(item[1])

    # Results
    time_elapsed = time.time() - start_time
    success_rate = 100 * (1 - scoreboard.count(0) / len(scoreboard))
    print('scoreboard: {}'.format(scoreboard))
    print('average score: {:.2f}'.format(np.mean(scoreboard)))
    print('standard deviation: {:.2f}'.format(np.std(scoreboard)))
    print('success rate: {:.2f}'.format(success_rate))
    print('--- {:.5f} seconds ---'.format(time_elapsed))
    # print('Q-tables: %s' % brain_bucket[0])

    if plot:
        data1 = np.zeros((6, 3))
        data2 = np.zeros((6, 3))
        for i in range(6):
            for j in range(3):
                data1[(i, j)] = brain_bucket[0][i][j][0]
                data2[(i, j)] = brain_bucket[0][i][j][1]
        data_difference = data2 - data1

        column = ['0', '1', '2']
        index = ['0', '1', '2',
                 '3', '4', '5']

        data1 = pd.DataFrame(data1, index=index, columns=column)
        data2 = pd.DataFrame(data2, index=index, columns=column)
        data_difference = pd.DataFrame(data_difference, index=index, columns=column)
        data_difference = np.sign(data_difference)

        plt.figure(dpi=200)

        plt.subplot(1, 3, 1)
        sns.heatmap(data1, annot=True, linewidths=0.5,
                    robust=True, square=True,
                    cmap="RdPu", cbar=False)
        plt.subplot(1, 3, 2)
        sns.heatmap(data2, annot=True, linewidths=0.5,
                    robust=True, square=True,
                    cmap="RdPu", cbar=False)
        plt.subplot(1, 3, 3)
        sns.heatmap(data_difference, annot=True, linewidths=0.5,
                    robust=False, square=True,
                    cmap="Spectral", cbar=False,
                    center=0)
        plt.show()
        # output = open('qbrain.csv', 'wb')
        # data_difference.dump(data1, output)
        # output.close()
        data_difference.to_csv('qbrain', index=False)
        # np.save('qbrain', np.sign(data_difference))
        # print(brain_bucket[0])
        difference_brain = pd.read_csv('qbrain')
        print(difference_brain)

    if render:
        pass
        QLearn(environment_param).run_trial(environment, environment_param, brain_bucket[-1])
        # for _ in range(3):
        #     QLearn(environment_param, logging=False).run_dummy_trial(environment, environment_param)

    sys.exit()
