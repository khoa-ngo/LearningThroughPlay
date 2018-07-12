#include <Wire.h>
#include "Adafruit_VCNL4010.h"

#define STEPPER_STEP 5
#define STEPPER_DIR 6
#define STEPPER_SLEEP 7
#define DELAY 300

Adafruit_VCNL4010 vcnl;
vcnl4010_freq VCNL4010_250;

void setup() {
  Serial.begin(9600);
  pinMode(STEPPER_STEP, OUTPUT);
  pinMode(STEPPER_DIR, OUTPUT);
  pinMode(STEPPER_SLEEP, OUTPUT);
  digitalWrite(STEPPER_SLEEP, HIGH);

  if (!vcnl.begin()){
  	Serial.println("Sensor not found: ");
  	while(1);
  }
  Serial.println("Found VCNL4010");
  vcnl.setFrequency(VCNL4010_250);
}

void loop() {
  Serial.print(getPosition());
}

void driveMotor(int speed) {
  if (speed != 0){
  	for (int i = 0; i <= speed; i++){
  	  digitalWrite(STEPPER_STEP, HIGH);
  	  delayMicroseconds(DELAY);
  	  digitalWrite(STEPPER_STEP, LOW);
  	}
  }
}

int getPosition() {
  return vcnl.readAmbient();
}