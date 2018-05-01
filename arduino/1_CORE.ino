int crop(int value, int min_value, int max_value) {
  return min(max_value, max(value, min_value));
}

void updateObservation(float (& ob)[4], float position, float velocity, float angle, float angular_velocity) {
  // Function takes in action and update observation
//  float act = 1.0;
  ob[0] = position;
  ob[1] = velocity;
  ob[2] = angle;
  ob[3] = angular_velocity;
}

void sendSerial(float (& ob)[4], int reward, bool done) {
  for (int i=0; i<=3; i++){
    // observations
    Serial.print(ob[i], 4);
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

      // end of message, should be something like
      // [ob1, ob2, ob3, ob4, reward, done]
      Serial.println();
    }
  }
}
