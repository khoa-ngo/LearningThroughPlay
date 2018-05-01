import numpy as np
import matplotlib.pyplot as plt
import csv

def extract_observations(filename):
    local_time = []
    time = []
    ob_space = []
    reward = []
    done = []
    info = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row:
                local_time.append(row[0])
                time.append(row[1])
                ob_space.append([row[2], row[3], row[4], row[5]])
                reward.append(row[6])
                done.append(row[7])
                info.append(row[8])

    for j in range(len(ob_space)):
        ob_space[j] = [float(i) for i in ob_space[j]]

    ob_space = np.array(ob_space)

    x = np.arange(len(time))
    y1 = ob_space[:,2]  # 2: theta, 3: dtheta
    y2 = ob_space[:,3]
    colors = np.random.rand(len(time))

    return x, y1, y2, colors


if __name__ == "__main__":
    # Main Plot
    crop = 1
    fig = plt.figure(dpi=250)

    # Comparative
    # filename = 'log.csv'
    # x, y1, y2, colors= extract_observations(filename)
    # fig.add_subplot(221)
    # plt.title('Angle')
    # plt.scatter(x, y1, s=1, c=colors, alpha=0.5)
    # if crop: plt.ylim(-2.0, 2.0)
    #
    # fig.add_subplot(222)
    # plt.title('Angular Velocity')
    # plt.scatter(x, y2, s=1, c=colors, alpha=0.5)
    # if crop: plt.ylim(-3.0, 3.0)
    #
    # filename = 'log_openai.csv'
    # x, y1, y2, colors = extract_observations(filename)
    # fig.add_subplot(223)
    # plt.scatter(x, y1, s=1, c=colors, alpha=0.5)
    # if crop: plt.ylim(-0.4, 0.4)
    #
    # fig.add_subplot(224)
    # plt.scatter(x, y2, s=1, c=colors, alpha=0.5)
    # if crop: plt.ylim(-1, 1)
    # Ends

    #Diagnostics
    filename = 'log.csv'
    x, y1, y2, colors = extract_observations(filename)

    plt.show()
