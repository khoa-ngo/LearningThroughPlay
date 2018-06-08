import numpy as np
import random


class QLearn:
    def __init__(self, env_param):
        self.bucket_size = (len(env_param['bins'][0]) + 1, len(env_param['bins'][1]) + 1)
        self.action_size = env_param['action_size']
        self.Q_table = np.zeros(self.bucket_size + (self.action_size,))
        self.num_streaks = 0  # number of consecutive episodes solved
        self.solved_episodes = 0  # number of episodes took to solve the problem

    def train(self, env, env_param, learning_rate_param, exploration_rate_param, discount_factor):
        self.learning_rate = self.get_learning_rate(learning_rate_param, env_param['goal_score'])
        self.exploration_rate = self.get_exploration_rate(exploration_rate_param, env_param['goal_score'])
        for episode in range(env_param['max_episodes']):
            env.reset()
            observation, reward, done, _ = env.step(env.action_space.sample())
            observation = observation[-2:]  # keep only angle & angular velocity
            state_previous = self.bucketize(observation, env_param['bins'])  # output bucketized states

            for t in range(env_param['max_steps']):
                action = self.select_action(state_previous, self.exploration_rate, self.Q_table)  # select action
                observation, reward, done, _ = env.step(action)  # perform action
                observation = observation[-2:]  # keep only angle & angular velocity
                state = self.bucketize(observation, env_param['bins'])  # bin the observations
                # Update Q-table based on the result
                max_Q = np.amax(self.Q_table[state])
                learned_value = reward + discount_factor * max_Q
                old_value = self.Q_table[state_previous + (action,)]

                self.Q_table[state_previous + (action,)] = (1-self.learning_rate)*old_value + self.learning_rate*(learned_value)

                # self.Q_table[state_previous + (action,)] += (learned_value - old_value) * self.learning_rate

                # Setting up for the next iteration
                state_previous = state
                if done:
                    self.num_streaks = 0
                    # print("Episode %d finished after %f time steps, done" % (episode, t))
                    break
                elif t >= env_param['goal_score']:
                    self.num_streaks += 1
                    # print("Episode %d finished after %f time steps, done" % (episode, t))
                    break

            if self.num_streaks >= env_param['goal_streak'] or episode >= env_param['max_episodes'] - 1:
                if self.num_streaks >= env_param['goal_streak']:
                    self.episode_count = episode  # if the training was a success, return the number of
                                                  # trials the AI took to learn
                else:
                    self.episode_count = 0  # if the training failed, return 0
                break

            self.exploration_rate = self.get_exploration_rate(exploration_rate_param,
                                                              env_param['goal_score'], score=t)
            self.learning_rate = self.get_learning_rate(learning_rate_param,
                                                        env_param['goal_score'], score=t)
        return self.Q_table, self.episode_count

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

    def run_dummy_trial(self, env, env_param):
        env.reset()
        for _ in range(env_param['max_steps']):
            env.render()
            action = env.action_space.sample()
            ob_space, reward, done, _ = env.step(action)

    def select_action(self, state, exploration, Q_table):
        if random.random() < exploration:
            action = random.randint(0, 1)  # Select a random action
        else:
            action = np.argmax(Q_table[state])  # Select the action with the highest q
        return action

    def get_learning_rate(self, param, expected_score, score=0):
        rate = param['initial'] * (1-(score/expected_score))
        return max(param['min'], rate)

    def get_exploration_rate(self, param, expected_score, score=0):
        rate = param['initial'] * (1-(score/expected_score))
        return max(param['min'], rate)

    def bucketize(self, ob_space, bins):
        bucket = np.empty(ob_space.size)
        for i in range(ob_space.size):
            bucket[i] = np.digitize(ob_space[i], bins[i])
        return self.totuple(bucket)

    def crop(self, value, min_value, max_value):
        return min(max_value, max(value, min_value))

    def totuple(self, a):
        try:
            return tuple(self.totuple(i) for i in a)
        except TypeError:
            return int(a)
