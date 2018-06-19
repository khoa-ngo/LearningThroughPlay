float getPosition(int POT) {
  float val = 1 - analogRead(POT)*(1.0/1023.0);
  return val;
}

bool positionAtLow(float x) {
  //x ranges from 0.0-1.0
  float lowerlimit = 0.15;
  if (x < lowerlimit) {
    return 1;
  }
  else {
    return 0;
  }
}

bool positionAtHigh(float x) {
  //0.0< x <1.0
  float higherlimit = 0.85;
  if (x > higherlimit) {
    return 1;
  }
  else {
    return 0;
  }
}
