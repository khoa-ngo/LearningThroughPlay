#include "Adafruit_TLC5947.h"

#define NUM_TLC5974 1
#define DIN 4
#define CLK 5
#define LAT 6
#define LED1 5

Adafruit_TLC5947 TLC = Adafruit_TLC5947(NUM_TLC5974, CLK, DIN, LAT);

int led_gap = 500; // time gap between the start of R, G, and B lights
int r = -200; // initial red value
int g = r - led_gap; // initial g value with time delay
int b = g - led_gap; // initial b value with time delay

int led_dir_r = 1;
int led_dir_g = 1;
int led_dir_b = 1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  TLC.begin();
}

void loop() {
  TLC.setLED(LED1, crop(r,0,4095), crop(g,0,4095), crop(b,0,4095));
  TLC.write();

  setLEDcolor(r, g, b, led_dir_r, led_dir_g, led_dir_b);
}

int crop(int value, int min_value, int max_value) {
  return min(max_value, max(value, min_value));
}

void ledDir(int value, int led_speed, int &led_dir){
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

  ledDir(r, led_speed, led_dir_r);
  ledDir(g, led_speed, led_dir_g);
  ledDir(b, led_speed, led_dir_b);
}

