void setLEDdir(int value, int led_speed, int &led_dir){
  if (value > 4095 + led_speed * 1){
    led_dir = -1;
  }
  if (value < - 50 * led_speed && led_dir == -1) {
    led_dir = 1;
  }
}

void setLEDcolor(int &r, int &g, int &b, int &led_dir_r, int &led_dir_g, int &led_dir_b){
  int led_speed = 25; // how quickly LED intensity rise and fall
  int led_acceleration = 3; // how quickly LED intensity rise at the start of the cycle
  
  r += (led_speed + (r/4095 - 1) * led_acceleration) * led_dir_r;
  g += (led_speed + (g/4095 - 1) * led_acceleration) * led_dir_g;
  b += (led_speed + (b/4095 - 1) * led_acceleration) * led_dir_b;

  setLEDdir(r, led_speed, led_dir_r);
  setLEDdir(g, led_speed, led_dir_g);
  setLEDdir(b, led_speed, led_dir_b);
}
