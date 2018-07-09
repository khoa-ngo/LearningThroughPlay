import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# filename = 'ai_physical_log.csv'
filename = 'ai_simulated_log.csv'
df = pd.read_csv(filename)
# print(df)

acceleration = list()
last_velocity = 0
for index, row in df.iterrows():
    velocity = row['Velocity']
    acceleration.append(velocity-last_velocity)
    last_velocity = velocity

# print(acceleration)
# print(df['Velocity'])
# df.plot(kind='scatter', y='Velocity')
# for _ in
# df.plot(y='Velocity')

data = acceleration
colors = np.random.rand(len(data))
plt.figure(dpi=500)
plt.scatter(range(len(data)), data, c=colors, alpha=0.2)
plt.show()
