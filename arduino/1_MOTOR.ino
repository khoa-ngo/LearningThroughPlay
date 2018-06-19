void driveMotor(int action, int speed, float position, int MOTOR_IN1, int MOTOR_IN2) {
  //action [0 or 1]
  //speed [0-inf]
  float speed_offset = 1.45;
  if (action == 2) {  // action 2 shuts down motor
    digitalWrite(MOTOR_IN1, LOW);
    digitalWrite(MOTOR_IN2, LOW);
  }
  else if (positionWithinRange(position)) {
    if (action == 0) {
      digitalWrite(MOTOR_IN2, LOW);
      analogWrite(MOTOR_IN1, speed);
    }
    if (action == 1) {
      digitalWrite(MOTOR_IN1, LOW);
      analogWrite(MOTOR_IN2, speed * speed_offset);
    }
  }
  else {
    digitalWrite(MOTOR_IN1, LOW);
    digitalWrite(MOTOR_IN2, LOW);
  }
}

void stopMotor(float position, int MOTOR_IN1, int MOTOR_IN2) {
  driveMotor(2, 0, position, MOTOR_IN1, MOTOR_IN2);
}

bool motorResetPosition(int MOTOR_IN1, int MOTOR_IN2, int POT) {
  float position;
  float delta_position = 1.0;
  while(abs(delta_position) > 0.05) {
    position = getPosition(POT);
    delta_position = position - 0.5;
    if (delta_position > 0) {
      driveMotor(0, 85, position, MOTOR_IN1, MOTOR_IN2);
    }
    if (delta_position < 0) {
      driveMotor(1, 85, position, MOTOR_IN1, MOTOR_IN2);
    }
  }
  stopMotor(position, MOTOR_IN1, MOTOR_IN2);
  return false;
}
