#include "Adafruit_TLC5947.h" // led controller
#include "Servo.h" // servo
#include "Wire.h" // imu
#include "Adafruit_Sensor.h" // imu
#include "Adafruit_BNO055.h" // imu
#include "utility/imumaths.h" // imu

//#define DEBUG
//digital pins assignments:
#define DIN 4 //LED controller pin: DIN
#define CLK 5 //LED controller pin: CLK
#define LAT 6 //LED controller pin: LAT
#define SERVO1 9 //servo #1
#define SERVO2 10 //servo #2
#define MOTOR_IN1 3 //motor controller pin: IN1
#define MOTOR_IN2 11 //motor controller pin: IN2
//analog pins assignments:
#define JOYSTICKX 2 //joystick signal, x direction
#define POT 3 // potentiometer sense

//other assignments:
#define LED1 5 //LED Controller LED Location

// initialize LED:
Adafruit_TLC5947 TLC = Adafruit_TLC5947(0, CLK, DIN, LAT);
int led_gap = 500; //time delay between the start of red, green, and blue LEDs
int r = -200; // initial red value
int g = r - led_gap; //initial green value with time delay
int b = g - led_gap; //initial blue value with time delay
int led_dir_r = 1;
int led_dir_g = 1;
int led_dir_b = 1;

//Servo:
Servo servo1;
Servo servo2;

//IMU:
Adafruit_BNO055 bno = Adafruit_BNO055(55);  // start ddafruit instance
float angle = 0.0; // pendulum arm angle measurement
float angle_previous = 0.0;
float angular_velocity; // calculated angular velocity

//slide potentiometer:
float position; // slide pot current position
float velocity; // calculated velocity
float position_previous; // past position measurement, used to calculate velocity
unsigned long time_end; // first timestamp
unsigned long time_begin = millis(); //update previous timestamp for velocity calculations
unsigned long time_delta;

//Machine Learning:
float observation[4];
int reward = 0;
bool done = false;
int action = 2;

//Other:
bool msg_received = false;
bool joystick_control = false;
bool restarted = true;
int drive_speed = 85;

void setup() {
  Serial.begin(57600);
  String string = "hello";
  Serial.println(string);

  //LED
  // TLC.begin(); //LED Controller
  // TLC.setLED(LED1, 4095, 4095, 4095);  // 0-4095

  //Servo
  servo1.attach(SERVO1); //Servo
  servo2.attach(SERVO2); //Servo
  servoResetPosition();

  //Motor
  pinMode(MOTOR_IN1, OUTPUT); //Motor
  pinMode(MOTOR_IN2, OUTPUT); //Motor
  motorResetPosition(MOTOR_IN1, MOTOR_IN2, POT);

  //IMU
  if(!bno.begin()) {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
  }
  delay(200);
  bno.setExtCrystalUse(true);

  // update initial position
  position_previous = getPosition(POT);
}
