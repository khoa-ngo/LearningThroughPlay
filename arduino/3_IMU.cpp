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

