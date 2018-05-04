import time
import numpy as np
import csv


def step(act, ser):
    time.sleep(0.01)
    data = ""  # clear data queue
    string = '{}\n'.format(str(act))  # format to-be-sent data

    # while ser.inWaiting()!=0:  # wait for incoming data
    #     ser.flushOutput()
    #     pass

    ser.write(string.encode())  # send data
    # print('sent')
    data = ser.readline()

    if data:
        # print("got")
        # print("")
        data = data.decode('utf-8')
        data = data.split(",")
        if isfloat(data[0]):
            ob_space = np.array([float(data[0]), float(data[1]),
                                float(data[2]), float(data[3])])
            reward = int(data[4])
            done = int(data[5])
        else:
            ob_space = np.zeros(4)
            reward = 0
            done = 0
        return ob_space, reward, done, None
    else:
        print("Communication disrupted")


def log_initialize(filename):
    f = open(filename, 'w+')
    f.close()


def get_elapsed_time(initial_time):
    return time.time()-initial_time


def log_make_entry(entry, elapsed_time, act, ob_space, reward, done,
                   learning_rate, exploration_rate, episode, t):
    data = [elapsed_time, act, ob_space[0], ob_space[1], ob_space[2], ob_space[3],
             reward, done, learning_rate, exploration_rate, episode, t]
    entry.append(data)
    return entry


def log_write_entry(filename, entry):
    with open(filename, 'a') as logbook:
        writer = csv.writer(logbook)
        for i in range(len(entry)):
            writer.writerow(entry[i])


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False
