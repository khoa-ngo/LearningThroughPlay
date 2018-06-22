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
      driveMotor(action, drive_speed, position, MOTOR_IN1, MOTOR_IN2);
    }

    // observations
    angle = getAngle();
    position = getPosition(POT);
    done = isDone(angle, position); // check if done
    // derived observations
    velocity = (position - position_previous)*10.0;
    angular_velocity = 10.0* (angle - angle_previous);
    // store to last observations
    position_previous = position;
    angle_previous = angle;

    // send data to python
    if (done) {
      stopMotor(position, MOTOR_IN1, MOTOR_IN2);
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
      delay(700);
      restarted = true;
      angle_previous = getAngle();  // get initial angle after reset
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