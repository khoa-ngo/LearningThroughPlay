from environments.envs.cartpole_continuous import CartPoleEnv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import core

# a = np.array((1, 2, 3, 4))
# b = np.array((2, 3, 4, 5))
#
# c = np.multiply(a,b)
# print(c)

n = 1000
data = []
for _ in range(n):
    data.append(core.getRandomFloat(-1, 1, type="normal"))

data = pd.DataFrame(data)
data.hist()
plt.show()
