import serial
import sys
import time

"Serial Connection Configuration"
SERIALPORT = "COM3"
baudrate = 9600

act = 1

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
    ob = step(act)

    if ob:
        ob = ob.decode('utf-8')
        ob = ob.split(",")
        print(ob)

    act = act + 1
    time.sleep(0.25)
