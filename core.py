import time
import numpy as np
import csv


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

def getRandomFloat(min, max):
  val = (np.random.rand() - 0.5)  # generate random float (-0.5,0.5)
  ret = val * (max - min) + mean((min, max))
  return ret

def mean(numbers):
  return float(sum(numbers)) / max(len(numbers), 1)