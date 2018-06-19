void loop() {
  // read command through serial comm
  if (Serial.available()) {  // check serial buffer for command
    String received = Serial.readStringUntil('\n');
    action = received.toInt();
    msg_received = true;
  }
  else {
    msg_received = false;
  }
  // reserved for debugging
  #ifdef DEBUG
  done = false;
  action = 2;
  msg_received = true;
  #endif
  // joystick control
  if (joystick_control) {
    ;
  }
  // perform action as soon as possible after receiving it
  if (action != 2) {
    if (restarted){
      servoActivePosition();
      restarted = false;
    }
    driveMotor(action, drive_speed, position, MOTOR_IN1, MOTOR_IN2);
  }
  else {
    servo1.detach();
    servo2.detach();
  }
  // observation
  delay(10);
  angle = getAngle();
  position = getPosition(POT);
  #ifdef DEBUG
  time_end = millis();  // clock ends
  #endif
  done = isDone(angle, position); // check if done
  // calculated properties
  #ifdef DEBUG
  time_delta = time_end - time_begin;
  #endif
  velocity = (position - position_previous)/1.0;
  angular_velocity = 10.0 * (angle - angle_previous)/1.0;
  position_previous = position;
  angle_previous = angle;
  #ifdef DEBUG
  time_begin = millis();  // clock starts
  #endif
  // send data to python
  if (!done && msg_received) {
    updateObservation(observation, position, velocity, angle, angular_velocity);
    reward = 1;  // receives reward if they hadn't fall
    sendSerial(observation, reward, done);
  }
  if (done) {
    delay(200);
    stopMotor(position, MOTOR_IN1, MOTOR_IN2);
    servo1.attach(SERVO1);
    servo2.attach(SERVO2);
    servoResetPosition(); // reset servo
    delay(500); // delay between servo reset and position reset
    // send out done null message
    if (msg_received){
      updateObservation(observation, 0.00, 0.00, 0.00, 0.00); // update null observations
      reward = 0; // assign reward
      sendSerial(observation, reward, done); // send message
    }
    // reset pot position
    done = motorResetPosition(MOTOR_IN1, MOTOR_IN2, POT);
    delay(500);
    restarted = true;
    angle_previous = getAngle();  // get initial angle after reset
    position_previous = getPosition(POT);  // get initial position after reset
    #ifdef DEBUG
    time_begin = millis();  // clock starts again
    #endif
    action = 2;
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