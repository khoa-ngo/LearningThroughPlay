# A.I. that can learn to perform robotic tasks from iteracting with the physical world

Requirements:
* Python 3.5
* Arduino IDE

# File Descriptions:
ai_physical.py: perform training on a physical robot
ai_simulated.py: perform training on a simulated environment
core.py: contains core functions like logging, serial communication, etc.
qlearn.py: learning algorithm based on Q-learning
random_search.py: learning algorithm based on random search (aka. Monte Carlo method)

# Install Dependencies:
```bash
pip install gym, pandas, matplotlib, seaborn
```

# Installation
```bash
git clone https://github.com/khoa-ngo/ai_pendulum
cd ai_pendulum
./ai_simulated.py
```
