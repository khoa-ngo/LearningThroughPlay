import serial
import sys
import time
import numpy as np
import csv


def create_entry(ob_space, reward, done, info):
    entry = [time.ctime(), time.time(), ob_space[0], ob_space[1], ob_space[2], ob_space[3],
             reward, done, info]
    return entry


def write_to_log(entry):
    with open('log.csv', 'a') as logbook:
        writer = csv.writer(logbook)
        writer.writerow(entry)


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def step(act, ser):
    data = ""  # clear data queue
    string = '{}\n'.format(str(act))  # format to-be-sent data
    ser.write(string.encode())  # send data

    # while ser.in_waiting < 0:  # wait for incoming data
    #     print("waiting for data")
    data = ser.readline()
    ser.flushOutput()

    if data:
        data = data.decode('utf-8')
        data = data.split(",")
        if isfloat(data[0]):
            ob_space = np.array([float(data[0]), float(data[1]),
                                float(data[2]), float(data[3])])
            reward = int(data[4])
            done = int(data[5])
            info = 1
        else:
            ob_space = np.zeros(4)
            reward = 0
            done = 0
            info = 0

        return ob_space, reward, done, info