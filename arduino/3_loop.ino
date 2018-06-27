void loop() {
  // read command through serial comm
  if (Serial.available()) {  // check serial buffer for command
    String received = Serial.readStringUntil('\n');
    action = received.toInt();

    // perform action as soon as possible after receiving it
    if (action == 1 or action == 0) {
      if (restarted){
        servoActivePosition();
        restarted = false;
      }
      // action
      if (action == 1) {
        drive_speed += drive_force;
      }
      if (action == 0) {
        drive_speed -= drive_force;
      }
      // drive
      if (drive_speed > 0) {
        drive_direction = 1;
      }
      if (drive_speed < 0) {
        drive_direction = 0;
      }
      else if (drive_speed == 0) {
        drive_direction = 2;
      }
      driveMotor(drive_direction, abs(drive_speed), position, MOTOR_IN1, MOTOR_IN2);
      // delay(5);
    }

    // observations
    angle = getAngle() - initial_angle;
    position = getPosition(POT);
    done = isDone(angle, position); // check if done
    // derived observations
    velocity = (position - position_previous) * 10.0;
    angular_velocity = 10.0 * (angle - angle_previous);
    // store to last observations
    position_previous = position;
    angle_previous = angle;

    // send data to python
    if (done) {
      stopMotor(position, MOTOR_IN1, MOTOR_IN2);
      drive_speed = 0;
      updateObservation(observation, position, velocity, angle, angular_velocity); // update null observations
      reward = 0; // assign reward
      sendSerial(action, observation, reward, done); // send out done null message
      delay(200);
      servo1.attach(SERVO1);
      servo2.attach(SERVO2);
      servoResetPosition(); // reset servo
      // reset pot position
      delay(200);
      done = motorResetPosition(MOTOR_IN1, MOTOR_IN2, POT);
      delay(1000);
      initial_angle = getAngle();
      restarted = true;
      angle_previous = 0.0;  // get initial angle after reset
      position_previous = getPosition(POT);  // get initial position after reset
    }
    else {
      updateObservation(observation, position, velocity, angle, angular_velocity);
      reward = 1;  // receives reward if they hadn't fall
      sendSerial(action, observation, reward, done);
    }
  }
  // debug output
  #ifdef DEBUG
  Serial.print("dt: ");
  Serial.print(time_delta);
  Serial.print(" obs: ");
  Serial.print(position, 3);
  Serial.print(" ");
  Serial.print(velocity, 3);
  Serial.print(" ");
  Serial.print(angle, 3);
  Serial.print(" ");
  Serial.print(angular_velocity, 4);
  Serial.print(" action: ");
  Serial.print(action);
  Serial.print(" done: ");
  Serial.println(done);
  #endif
}