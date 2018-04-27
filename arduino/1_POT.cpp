float readPosition(int POT) {
  float val = 1 - analogRead(POT)*(1.0/1023.0);
  return val;
}

bool positionAtLow(float x) {
  //x ranges from 0.0-1.0
  float lowerlimit = 0.1;
  if (x < lowerlimit) {
    return 1;
  }
  else {
    return 0;
  }
}

bool positionAtHigh(float x) {
  //x ranges from 0.0-1.0
  float higherlimit = 0.9;
  if (x > higherlimit) {
    return 1;
  }
  else {
    return 0;
  }
}
