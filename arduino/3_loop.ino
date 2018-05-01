void loop() {
  // Read action from Python
  if (Serial.available()) {
    String received = Serial.readStringUntil('\n'); 
    act = received.toInt();
    msg_received = true;
    }
    else {
    msg_received = false;
    }

  // Check for done state First
  if (getAngle() > 0.8 || getAngle() < -0.8 || 
      readPosition(POT) > 0.8 || readPosition(POT) < 0.2 ) {
    done = 1;
  }
  // Then Perform Action
  if (done) {
    // Stop Motor
    driveMotor(3, 0, 0, position, MOTOR_IN1, MOTOR_IN2);

    // Reset Servo
    servo1.attach(SERVO1);
    servo2.attach(SERVO2);
    servoResetPosition();
    delay(500);

    // Send out 'done' message
    updateObservation(ob, 0.0, 0.0, 0.0, 0.0);
    reward = 0;
    sendSerial(ob, reward, done);

    // Reset Pot Position
    done = motorResetPosition(MOTOR_IN1, MOTOR_IN2, POT);
    delay(1000);
  }
  else if (act != 3) {
    reward = 1;
    servo1.attach(SERVO1);
    servo2.attach(SERVO2);
    servoActivePosition();
    driveMotor(act, 85, 0, position, MOTOR_IN1, MOTOR_IN2);
  }
  else {
    servo1.detach();
    servo2.detach();
  }
  
  if (msg_received){
    // Observations
    angle = getAngle();
    position = readPosition(POT);

    // Calculated Observations
    time_now = millis();  //finish time
    time_delta = time_now - time_previous;
    velocity = 1000.0 * (position - position_previous)/((float)time_now-(float)time_previous);
    angular_velocity = 1000.0 * (angle - angle_previous)/((float)time_now-(float)time_previous);
    position_previous = position;
    angle_previous = angle;
    time_previous = time_now;  //start time

    updateObservation(ob, position, velocity, angle, angular_velocity);
    sendSerial(ob, reward, done);
  }

  // servo1.detach();
  // servo2.detach();

  //Debug
  if (debug){
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
    Serial.print(" act: ");
    Serial.print(act);
    Serial.print(" done: ");
    Serial.println(done);
  }
}