void loop() {
  // read command from python
  if (Serial.available()) {
    String received = Serial.readStringUntil('\n');
    act = received.toInt();
    msg_received = true;
  }
  else {
    msg_received = false;
  }

  // reserved for debugging
  if (debug) {
    done = 0;
    act = 2;
    msg_received = true;
  }

  // perform action as soon as possible after receiving it
  if (act != 2) {
    servoActivePosition();
    if (restarted){
      delay(100);
      restarted = false;
    }
    driveMotor(act, drive_speed, 15, position, MOTOR_IN1, MOTOR_IN2);
  }
  else {
    servo1.detach();
    servo2.detach();
  }
  
  // observation
  delay(10);
  angle = getAngle();
  position = getPosition(POT);
  // time_end = millis();  // clock ends

  done = isDone(angle, position); // check if done

  // calculated properties
  // time_delta = time_end - time_begin;
  velocity = (position - position_previous)/1.0;
  angular_velocity = 10.0 * (angle - angle_previous)/1.0;
  
  position_previous = position;
  angle_previous = angle;
  // time_begin = millis();  // clock starts

  // send data to python
  if (!done && msg_received) {
    reward = 1;  // receives reward if they hadn't fall
    updateObservation(ob, position, velocity, angle, angular_velocity);
    sendSerial(ob, reward, done);
  }

  if (done) {
    delay(200);
    driveMotor(2, 1, 0, position, MOTOR_IN1, MOTOR_IN2); // stop motor
    servo1.attach(SERVO1); // reset servo
    servo2.attach(SERVO2); // reset servo
    servoResetPosition(); // reset servo
    delay(1000); // delay between servo reset and position reset

    // send out done null message
    reward = 0; // assign reward
    if (msg_received){
      updateObservation(ob, 0.0, 0.0, 0.0, 0.0); // update null observations
      sendSerial(ob, reward, done); // send message
    }

    // reset pot position
    done = motorResetPosition(MOTOR_IN1, MOTOR_IN2, POT);
    delay(1000);
    restarted = true;
    act = 2;

    angle_previous = getAngle();  // get initial angle after reset
    position_previous = getPosition(POT);  // get initial position after reset
    // time_begin = millis();  // clock starts again
  }

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