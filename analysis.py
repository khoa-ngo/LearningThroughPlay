import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cl
import csv
import math


def scatter_subplot(data, key, limit=False, dpi=250):
    n = len(data['elapsed_time'])
    a = len(key)
    b = 1

    fig = plt.figure(dpi=dpi, figsize=(7,17))  # aspect ratio of figure
    # colors = cl.to_rgb(str(np.random.rand()))
    colors = 'y'

    # x = [i for i in data['elapsed_time']]
    x = range(len(data['elapsed_time']))
    c = 1
    for k in key:
        if len(key) >= 2:
            fig.add_subplot(a,b,c)
            c += 1
        y = data[k]
        plt.title(k, fontsize=12)
        # plt.scatter(x, y, s=20, c=colors, alpha=0.5)
        plt.bar(x, y, color=colors, linewidth=0)
        plt.xticks(np.arange(0, n, step=100), fontsize=5)
        plt.grid(which='major', color='k', linestyle='--', linewidth=0.25)
        if k in limit:
            plt.ylim(min(limit[k]), max(limit[k]))


def combined_plot(data, key, limit=False, dpi=250):
    n = len(data['elapsed_time'])  # length of data
    fig = plt.figure(dpi=dpi)
    colors = np.random.rand(n)
    x = [i * 1000.0 for i in data['elapsed_time']]

    for k in key:
        y = data[k]
        plt.title(k)
        plt.plot(x, y)

    if limit:
        plt.ylim(min(limit[k]), max(limit[k]))


def parse_data(filename):
    headers = ['elapsed_time', 'act', 'observation0', 'observation1', 'observation2', 'observation3',
               'reward', 'done', 'learning_rate', 'exploration_rate', 'episode', 'step']
    data = {}
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        previous_angle = 0
        for row in reader:
            if not row:
                continue

            for key in headers:
                data_buffer = row[headers.index(key)]  # row[index]
                if data_buffer == 'True':
                    data_buffer = '1'
                elif data_buffer == 'False':
                    data_buffer = '0'
                data.setdefault(key, [])
                data[key].append(float(data_buffer))

            # key_custom1 = 'error'
            # key_custom2 = 'observation3_predicted'
            #
            # delta_angle = 30.7 * (float(row[headers.index('observation2')]) - previous_angle)
            # data.setdefault(key_custom1, [])
            # error = delta_angle - float(row[headers.index('observation3')])
            # data[key_custom1].append(float(error))
            # previous_angle = float(row[headers.index('observation2')])

            # data.setdefault(key_custom2, [])
            # data[key_custom2].append(delta_angle)

    return dict(data)


if __name__ == "__main__":
    plot_setting = {"dpi": 280}
    headers = ['elapsed_time', 'act', 'observation0', 'observation1', 'observation2', 'observation3',
               'reward', 'done', 'learning_rate', 'exploration_rate', 'episode', 'step']

    # plot experimental data
    log = parse_data('log.csv')
    # log = parse_data('log_openai.csv')
    n = len(log['elapsed_time'])

    # key = ['act', 'observation2', 'observation3', 'done']
    key = headers
    limit = {}

    scatter_subplot(log, key, limit, dpi=plot_setting["dpi"])

    plt.tight_layout()
    # plt.tight_layout()
    plt.show()

    # plot data from openai gym
    # log_openai = parse_data('log_openai.csv')
    # limit = {
    #     'observation3': [-1.0, 1.0]
    # }

    # key = ['ob_space3', 'ob_space3_predicted']
    # key = ['observation2', 'observation3', 'observation3_predicted', 'error']
    # scatter_subplot(log, key, limit, dpi=plot_setting["dpi"])
    # scatter_subplot(log_openai, key, limit, dpi=plot_setting["dpi"])

    # plt.show()
    # combined_plot(log_openai, key)

    # print(np.mean([abs(number) for number in log_openai['observation3']]))
    # print(np.mean([abs(number) for number in log_openai['observation3_predicted']]))

