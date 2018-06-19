float getPosition(int POT) {
  return 1 - analogRead(POT)*(1.0/1023.0);
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
