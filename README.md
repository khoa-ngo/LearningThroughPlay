## Artificial intelligence that can learn to perform robotic tasks from iteracting with the physical world

### Brief Overview:   
* What is it about robots that make them so robotic?   
In this project, we will teach a robot to learn and perform a simple athletic task using Q-learning. The foundation of this teaching consists of: a reward system, a learning algorithm, and a way for the A.I. to interact with the environment. By providing incentives for the them to do well, we can train the A.I. to become proficient in a variety of tasks. Without this incentive, the A.I. lacks purpose. In the end, the types of behavior that we endorse (and reward) determines the kind of A.I. that is produced.

### Requirements:
* Python 3.6.5
* Arduino IDE > 1.8.5

### File Descriptions:
ai_physical.py: perform training on a physical robot  
ai_simulated.py: perform training in a simulated environment  
core.py: contains core functions like logging, serial communication, etc.  
qlearn.py: learning algorithm based on Q-learning   
random_search.py: learning algorithm based on random search (aka. Monte Carlo method)   

### Install Dependencies:
* Python:
```bash
pip install gym, pandas, matplotlib, seaborn, pyserial
```   
* Arduino: ([tutorial](https://www.arduino.cc/en/guide/libraries))
```
Adafruit United Sensor > 1.0.2
Adafruit TLC5947 > 1.0.2
Adafruit BNO055 > 1.1.3
```

### Installation
```bash
git clone https://github.com/khoa-ngo/ai_pendulum
```

### Test Simulated Learning
```bash
cd ai_pendulum
./ai_simulated.py
```
