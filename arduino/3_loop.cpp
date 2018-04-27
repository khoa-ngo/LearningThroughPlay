void loop() {
  if (Serial.available()) {
    String received = Serial.readStringUntil('\n'); // read action from Python
    act = received.toInt();
    msg_received = true;
  }
  else {
    msg_received = false;
  }

  // LED
  TLC.setLED(LED1, crop(r,0,4095), crop(g,0,4095), crop(b,0,4095));
  TLC.write();
  setLEDcolor(r, g, b, led_dir_r, led_dir_g, led_dir_b);
  
  //Joystick
  if (manual_control){
    act = readJoystick(JOYSTICKX);
  }
  
  if (act != -1) {
    active = true;
  }

  //Done Detection
  if (angle > 0.85 || angle < -0.85) {
    driveMotor(-1, 1, 0, position, MOTOR_IN1, MOTOR_IN2);
    done = true;
    active = false;
    delay(500);
  }
  if (done) {
    servo1.attach(SERVO1);
    servo2.attach(SERVO2);
    servoResetPosition();
    delay(400);
    // servoActivePosition();  # manual active mode for debug
    updateObservation(ob, 0.0, 0.0, 0.0, 0.0);
    sendSerial(ob, done);
    done = motorResetPosition(MOTOR_IN1, MOTOR_IN2, POT);
    delay(400);
  }
  else if (active) {
    servo1.attach(SERVO1);
    servo2.attach(SERVO2);
    servoActivePosition();
    driveMotor(act, 100, 0, position, MOTOR_IN1, MOTOR_IN2);
  }
  else {
    servo1.detach();
    servo2.detach();
  }
  
  if (msg_received && !done || manual_control) {
    //Sensor: Slide Pot & IMU
    angle = getAngle();
    position = readPosition(POT);

    //Sensor: Calculated Values
    time_now = millis();  //finish time
    time_delta = time_now - time_previous;
    velocity = 1000.0 * (position - position_previous)/((float)time_now-(float)time_previous);
    angular_velocity = 1000.0 * (angle - angle_previous)/((float)time_now-(float)time_previous);
    position_previous = position;
    angle_previous = angle;
    time_previous = time_now;  //start time

    //Send data to Python
    updateObservation(ob, position, velocity, angle, angular_velocity);
    sendSerial(ob, done);
  }

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
