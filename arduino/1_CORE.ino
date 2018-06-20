int crop(int value, int min_value, int max_value) {
  return min(max_value, max(value, min_value));
}

void updateObservation(float (& observation)[4], float position, float velocity, float angle, float angular_velocity) {
  // takes in action and update observation
  observation[0] = position;
  observation[1] = velocity;
  observation[2] = angle;
  observation[3] = angular_velocity;
}

void sendSerial(float (& observation)[4], int reward, bool done) {
  for (int i=0; i<=3; i++){
    Serial.print(observation[i], 2);
    Serial.print(',');
    if (i==3) {
      Serial.print(reward);
      Serial.print(',');
      if (done){
        Serial.print('1');
      }
      else {
        Serial.print('0');
      }
      Serial.print(',');
      Serial.println();
    }
  }
}

bool positionWithinRange(float position) {
  float lower_limit = 0.15;  // position limits, trigger done if not within range
  float upper_limit = 0.85;
  if (position < upper_limit && position > lower_limit) {
    return true;
  }
  else {
    return false;
  }
}

bool angleWithinRange(float angle) {
  float lower_limit = -0.75;  // angular limits, trigger done if not within range
  float upper_limit = 0.75;
  if (angle < upper_limit && angle > lower_limit) {
    return true;
  }
  else {
    return false;
  }
}

bool isDone(float angle, float position) {
  if (positionWithinRange(position) && angleWithinRange(angle)){
    return false;
  }
  else {
    return true;
  }
}
