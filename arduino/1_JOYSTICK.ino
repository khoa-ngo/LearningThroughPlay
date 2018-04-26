int readJoystick(int JOYSTICKX){
  float deadband = 0.2;
  float upperband = 0.5 + deadband/2.0;
  float lowerband = 0.5 - deadband/2.0;
  
  float val = analogRead(JOYSTICKX)*(1.0/1023.0);
  if (val > upperband){
    return 1;
  }
  if (val < lowerband){
    return 0;
  }
  else{
    return -1;
  }
}

