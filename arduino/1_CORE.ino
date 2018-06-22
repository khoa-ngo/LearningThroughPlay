int crop(int value, int min_value, int max_value) {
  return min(max_value, max(value, min_value));
}

void updateObservation(float (& observation)[4], float position, float velocity, float angle, float angular_velocity) {
  // takes in action and update observation
  observation[0] = (position - 0.5) * 1.0;
  observation[1] = velocity * 6.26;
  observation[2] = angle * 0.73;
  observation[3] = angular_velocity * 2.93;
}

void sendSerial(int action, float (& observation)[4], int reward, bool done) {
  for (int i=0; i<=3; i++){
    Serial.print(observation[i], 3);
    Serial.print(',');
    if (i==3) {
      Serial.print(reward);
      Serial.print(',');
      if (done) {
        Serial.print('1');
      }
      else {
        Serial.print('0');
      }
      Serial.print(',');
      Serial.print(action);
      Serial.print('\n');
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
  float lower_limit = -0.275;  // angular limits, trigger done if not within range
  float upper_limit = 0.275;
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
