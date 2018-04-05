import gym
import numpy as np
import random_search
from bokeh.plotting import figure, show, output_file

env = gym.make("CartPole-v1")
parameters = np.random.rand(4)

num_of_episodes = 3

reward_log = np.zeros((1, num_of_episodes))

for i in range(num_of_episodes):
    reward_log[0,i] = random_search.run_episode(env, parameters,
                                   episode_length=500,
                                   render=0)

print(reward_log)

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

