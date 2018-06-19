float getAngle() {
  sensors_event_t event;
  bno.getEvent(&event);
  
  angle = event.orientation.x;
  if (angle > 300) {
    angle = (angle - 360)/30;
  }
  else {
    angle = angle/30;
  }
  return angle;
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