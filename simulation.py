import gym
import numpy as np
from random_search import RandomSearch
from bokeh.plotting import figure, show, output_file

num_of_episodes = 10
episode_length = 500
batch_size = 4
reward_log = np.zeros((1, num_of_episodes))
parameters_log = np.zeros((4, num_of_episodes))
successrate_log = np.zeros((1, num_of_episodes))
count = 0

env = gym.make("CartPole-v1")

for j in range(int(num_of_episodes/batch_size)):
    parameters = np.random.rand(4)
    success_pool = []
    for i in range(batch_size):
        parameters_log[0:4, count] = parameters
        reward_log[0,count] = RandomSearch.run_episode(env, parameters,
                                       episode_length=episode_length,
                                       render=0)
        if reward_log[0, count] >= episode_length:
            success = 1
        else:
            success = 0

        success_pool.append(success)

        if len(success_pool) >= batch_size:
            # successrate_log[0, count] = (sum(success_pool)/batch_size) * np.ones((1,1))
            successrate_log[0, count] = 2
            # successrate_log[0, (count-3):count] = np.ones((1,1))

            print(successrate_log)
            # successrate_log[0, count-1] = sum(success_pool) / batch_size
            # successrate_log[0, count-2] = sum(success_pool) / batch_size
        count += 1

print(successrate_log)

# p = figure(plot_width=400, plot_height=400)
# p.ray(x=[0, 0, 0], y=[0, 0, 0], length=45, angle=[180, 90, 0],
#       angle_units="deg", color="#FB8072", line_width=2)
# show(p)

# N = 4000
# x = np.random.random(size=N) * 100
# y = np.random.random(size=N) * 100
# radii = np.random.random(size=N) * 1.5
# colors = [
#     "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)
# ]
#
# TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
#
# p = figure(tools=TOOLS)
#
# p.scatter(x, y, radius=radii,
#           fill_color=colors, fill_alpha=0.6,
#           line_color=None)
#
#
# show(p)  # open a browser

