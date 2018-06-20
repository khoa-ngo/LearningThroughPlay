void driveMotor(int action, int speed, float position, int MOTOR_IN1, int MOTOR_IN2) {
  //action [0 or 1]
  //speed [0-inf]
  float lower_limit = 0.15;  // position limits, trigger done if not within range
  float upper_limit = 0.85;
  float speed_offset = 1.45;
  if (action == 0 && position > lower_limit) {
    digitalWrite(MOTOR_IN2, LOW);
    analogWrite(MOTOR_IN1, speed);
  }
  else if (action == 1 && position < upper_limit) {
    digitalWrite(MOTOR_IN1, LOW);
    analogWrite(MOTOR_IN2, speed * speed_offset);
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
