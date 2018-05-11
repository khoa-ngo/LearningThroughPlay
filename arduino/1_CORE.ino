int crop(int value, int min_value, int max_value) {
  return min(max_value, max(value, min_value));
}

void updateObservation(float (& ob)[4], float position, float velocity, float angle, float angular_velocity) {
  // takes in action and update observation
  ob[0] = position;
  ob[1] = velocity;
  ob[2] = angle;
  ob[3] = angular_velocity;
}

void sendSerial(float (& ob)[4], int reward, bool done) {
  for (int i=0; i<=3; i++){
    // observations
    Serial.print(ob[i], 3);
    Serial.print(',');
    if (i==3) {
      // reward
      Serial.print(reward);
      Serial.print(',');

      // done
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

bool isDone(float angle, float position) {
  if (angle < -0.75 || angle > 0.75 || 
    position < 0.1 || position > 0.9) {
    return true;
  }
  else {
    return false;
  }
}
