import serial
import sys
import time
import numpy as np

"Serial Connection Configuration"
SERIALPORT = "COM4"
baudrate = 9600


def step(act):
    data = ""
    string = '{}\n'.format(str(act))
    ser.write(string.encode())
    if ser.in_waiting > 0:
        data = ser.readline()
    if data:
        return data


try:
    ser = serial.Serial(SERIALPORT, baudrate)
except serial.SerialException:
    print("Connection failed, please check port.")
    sys.exit()

while 1:
    act = 0
    time.sleep(0.1)
    # Must check and clear serial stream before sending new ones
    # Same for the Arduino side
    ob = step(act)
    if ob:
        ob = ob.decode('utf-8')
        ob = ob.split(",")
        print(ob)
