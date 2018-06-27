import time
import numpy as np
import serial
import sys
from core import isfloat
import random


class Environment:
    def __init__(self, serial_port, baudrate):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.action_size = 2
        try:
            self.ser = serial.Serial(self.serial_port, self.baudrate)
        except serial.SerialException:
            print("Connection failed, please check port.")
            sys.exit()
        print('...connection established...')
        time.sleep(1)  # Pause to stabilize Arduino

    def step(self, act):
        string = '{}\n'.format(str(act))  # format outgoing data
        self.ser.write(string.encode())  # send data
        data = self.ser.readline()  # read all data from serial port until nextline is detected
        if data:  # if there is data
            data = data.decode('utf-8')
            data = data.split(",")
            if isfloat(data[0]) and len(data) == 7:
                observation = np.array([float(data[0]), float(data[1]), float(data[2]), float(data[3])])
                reward = int(data[4])
                done = int(data[5])
            else:
                observation = np.zeros(4)
                reward = 0
                done = 0
            return observation, reward, done, None
        else:
            print("Communication disrupted")

    def reset(self):
        pass

    def render(self):
        pass
