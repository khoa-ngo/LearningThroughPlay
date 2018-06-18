## A.I. that can learn to perform robotic tasks from iteracting with the physical world

Requirements:
* Python 3.5
* Arduino IDE

### File Descriptions:
ai_physical.py: perform training on a physical robot  
ai_simulated.py: perform training in a simulated environment  
core.py: contains core functions like logging, serial communication, etc.  
qlearn.py: learning algorithm based on Q-learning   
random_search.py: learning algorithm based on random search (aka. Monte Carlo method)   

### Install Dependencies:
* Python:
```bash
pip install gym, pandas, matplotlib, seaborn
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
