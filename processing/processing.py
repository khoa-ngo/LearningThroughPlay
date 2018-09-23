import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import andrews_curves
import numpy as np

angle = []
rate = []
action = []

file = open('log1.txt', 'r')
for line in file:
    angle.append(float(line.split()[0]))
    rate.append(float(line.split()[1]))
    action.append(float(line.split()[1]))

angle = np.array(angle)
rate = np.array(rate)
action = np.array(action)

angle_scaled = np.interp(angle, (0, 90000), (0, 1))

print(type(angle))

data = {'angle': angle_scaled, 'rate': rate, 'action': action}
data = pd.DataFrame(data=data)
print(data)
x = data.index.tolist()

plt.figure()
# data.plot()
data.plot(y='angle')
plt.show()

# print(angle)
# print(rate)
# print(action)
