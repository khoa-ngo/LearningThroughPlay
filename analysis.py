import pandas as pd
from pandas import DataFrame, read_csv
import os

names = ['Bob','Jessica','Mary','John','Mel']
births = [968, 155, 77, 578, 973]
names2 = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5']
births2 = [1, 2, 3, 4, 5]
BabyDataSet = list(zip(names,births))
BabyDataSet2 = list(zip(names2,births2))
filename = 'ai_simulated_log.csv'

BabyDataSet = [('Bob', 968)]
print(BabyDataSet)

df = pd.DataFrame(data = BabyDataSet, columns=['Names', 'Births'])
df2 = pd.DataFrame(data = BabyDataSet2, columns=['Names', 'Births'])
frames = [df, df2]
df3 = pd.concat(frames)
print(df)
print('')
print(df2)
print('')
print(df3)
print('')
print(df3.get('x'))


df.to_csv(filename, index=True, header=True)
df2.to_csv(filename, mode='a', header=False)

path = os.path.dirname(__file__) + "/" + filename
df = pd.read_csv(path, header=None)

columns = ['Position', 'Velocity', 'Angle', 'Angular Velocity', 'Reward', 'Done', 'Episode', 'Step']
