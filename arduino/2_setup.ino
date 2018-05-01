//Includes***
#include "Adafruit_TLC5947.h" //LED Controller
#include "Servo.h" //Servo
#include "Wire.h" //IMU
#include "Adafruit_Sensor.h" //IMU
#include "Adafruit_BNO055.h" //IMU
#include "utility/imumaths.h" //IMU

//Pin Assignments***
//Digital:
#define DIN 4 //LED Controller DIN
#define CLK 5 //LED Controller CLK
#define LAT 6 //LED Controller LAT
#define SERVO1 9 //Servo 1
#define SERVO2 10 //Servo 2
#define MOTOR_IN1 3 //Motor IN1
#define MOTOR_IN2 11 //Motor IN2
//Analog:
#define JOYSTICKX 2 //Joystick signal, x direction
#define POT 3 //Potentiometer Sense


//Other Assignments:
#define LED1 5 //LED Controller LED Location
#define FORWARD 0
#define REVERSE 1

//Initialization***
//LED:
Adafruit_TLC5947 TLC = Adafruit_TLC5947(1, CLK, DIN, LAT);
int led_gap = 500; //time delay between the start of Red, Green, and Blue LEDs
int r = -200; // initial Red value
int g = r - led_gap; //initial Green value with time delay
int b = g - led_gap; //initial Blue value with time delay
int led_dir_r = 1; //LED directions
int led_dir_g = 1;
int led_dir_b = 1;

//Servo:
Servo servo1;
Servo servo2;

//IMU:
Adafruit_BNO055 bno = Adafruit_BNO055(55);
float angle; // pendulum arm angle measurement
float angle_previous = 0;
float angular_velocity; // calculated angular velocity

//Pot Sense:
float position; // slide pot current position
float velocity; // calculated velocity
float position_previous = readPosition(POT); // past position measurement, used to calculate velocity
unsigned long time_now; // first timestamp
unsigned long time_previous = millis(); //update previous timestamp for velocity calculations
unsigned long time_delta;

//Machine Learning:
float ob[4];
int reward = 0;
int done = 1;
int act = 3;

//Other:
bool active = false;
bool debug = false;
bool msg_received = false;
bool manual_control = false;

void setup() {
  Serial.begin(19200);

  //LED
  TLC.begin(); //LED Controller

  //Servo
  servo1.attach(SERVO1); //Servo
  servo2.attach(SERVO2); //Servo
  servoResetPosition();

  //Motor
  pinMode(MOTOR_IN1, OUTPUT); //Motor
  pinMode(MOTOR_IN2, OUTPUT); //Motor
  motorResetPosition(MOTOR_IN1, MOTOR_IN2, POT);

  //IMU
  Serial.println("Initializing IMU"); Serial.println("");
  if(!bno.begin()) {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
  }
  delay(1000);
  bno.setExtCrystalUse(true);
}
