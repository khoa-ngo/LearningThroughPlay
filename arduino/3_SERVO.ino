void servoResetPosition() {
  servo2.write(129); //Right, default: 130
  servo1.write(34); //Left, default: 33
}

void servoActivePosition() {
  servo2.write(10); //Right, default: 10
  servo1.write(153); //Left, default: 153
}
