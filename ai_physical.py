import gym
import numpy as np
from qlearn import QLearn
import time
import sys
from environment import Environment
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Create Simulated Environment and Define Environment Parameters:
action_size = 2
environment_param = {'max_episodes': 20, 'max_steps': 200, 'goal_score': 199, 'goal_streak': 20,
                     'bins': np.array([[-0.2, -0.1, 0.0, 0.1, 0.2], [-0.5, 0.5]], dtype=object),
                     'action_size': action_size}

# Define Learning Parameters:
learning_rate_param = {'initial': 0.4}  # determines how much the AI learns from new experiences.
exploration_rate_param = {'initial': 0.4}  # the AI's tendency to try new things.
discount_factor = 0.99  # The AI's patience for future rewards.

if __name__ == '__main__':
    serial_port = "COM3"
    baudrate = 57600
    environment = Environment(serial_port, baudrate)
    ai = QLearn(environment_param, logging=True, filename='ai_physical_log.csv')  # create an instance of the AI.
    environment.step("hi")
    q_table, episode_count = ai.train(environment, environment_param,
                                      learning_rate_param, exploration_rate_param,
                                      discount_factor)  # train the AI.

    print(q_table)
