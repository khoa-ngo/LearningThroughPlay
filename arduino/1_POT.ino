float getPosition(int POT) {
  return 1 - analogRead(POT)*(1.0/1023.0);
}
