void servoResetPosition() {
  servo2.write(131); //Left, default: 130
  servo1.write(34); //Right, default: 0
}

void servoActivePosition() {
  servo2.write(0); //Left, default: 0
  servo1.write(130); //Right, default: 130
}
