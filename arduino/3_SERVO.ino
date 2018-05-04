void servoResetPosition() {
  servo2.write(129); //Left
  servo1.write(52); //Right
}

void servoActivePosition() {
  servo2.write(30); //Left
  servo1.write(160); //Right
}
