void servoResetPosition() {
  servo2.write(130); //Left
  servo1.write(50); //Right
}

void servoActivePosition() {
  servo2.write(0); //Left
  servo1.write(180); //Right
}
