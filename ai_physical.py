import numpy as np
from qlearn import QLearn
from environment import Environment

# Create Simulated Environment and Define Environment Parameters:
serial_port = "COM3"
baudrate = 57600

environment = Environment(serial_port, baudrate)
environment_param = {'max_episodes': 50, 'max_steps': 200, 'goal_score': 100, 'goal_streak': 2,
                     'bins': np.array([[-0.18, -0.15, 0.0, 0.15, 0.18], [-0.15, 0.15]], dtype=object),
                     'action_size': environment.action_size}

# Define Learning Parameters:
learning_rate_param = {'initial': 0.5}  # determines how much the AI learns from new experiences.
exploration_rate_param = {'initial': 0.3}  # the AI's tendency to try new things.
discount_factor = 0.99  # The AI's patience for future rewards.

if __name__ == '__main__':
    ai = QLearn(environment_param, logging=True, telemetry=True, filename='ai_physical_log.csv')  # create an instance of the AI.
    environment.step("hi")
    q_table, episode_count = ai.train(environment, environment_param,
                                      learning_rate_param, exploration_rate_param,
                                      discount_factor)  # train the AI.

    print(q_table)
