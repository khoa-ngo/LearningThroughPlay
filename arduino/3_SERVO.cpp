void servoResetPosition() {
  servo1.write(54); //Right
  servo2.write(130); //Left
}

void servoActivePosition() {
  servo1.write(160); //Right
  servo2.write(30); //Left
}
