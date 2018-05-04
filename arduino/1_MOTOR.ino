void driveMotor(int direction, int speed, int timegap, float x, int MOTOR_IN1, int MOTOR_IN2) {
  //direction [0 or 1]
  //speed [0-inf]

  if (direction == 0) { //Left
    if (positionAtLow(x) == 0) {
      digitalWrite(MOTOR_IN2, LOW);
      analogWrite(MOTOR_IN1, speed);
      delay(timegap);
    }
    else {
      digitalWrite(MOTOR_IN1, LOW);
      digitalWrite(MOTOR_IN2, LOW);
    }
  }
  if (direction == 1) { //Right
    if (positionAtHigh(x) == 0) {
      digitalWrite(MOTOR_IN1, LOW);
      analogWrite(MOTOR_IN2, speed * 1.45);
      delay(timegap);
    }
    else {
      digitalWrite(MOTOR_IN1, LOW);
      digitalWrite(MOTOR_IN2, LOW);
    }
  }
  if (direction == 2) {
    digitalWrite(MOTOR_IN1, LOW);
    digitalWrite(MOTOR_IN2, LOW);
    delay(timegap);
  }
}

bool motorResetPosition(int MOTOR_IN1, int MOTOR_IN2, int POT) {
  float position;
  float delta_position = 1.0;

  while(abs(delta_position) > 0.05) {
    position = getPosition(POT);
    delta_position = position - 0.5;
    if (delta_position > 0) {
      driveMotor(0, 85, 0, position, MOTOR_IN1, MOTOR_IN2);
    }
    if (delta_position < 0) {
      driveMotor(1, 85, 0, position, MOTOR_IN1, MOTOR_IN2);
    }
  }
  driveMotor(2, 0, 0, position, MOTOR_IN1, MOTOR_IN2);
  return 0;
}
