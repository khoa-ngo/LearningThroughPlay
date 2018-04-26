#define MOTOR_IN1 2
#define MOTOR_IN2 3

int duration = 10;
int slidespeed = 15;

void setup() {
  pinMode(MOTOR_IN1, OUTPUT);
  pinMode(MOTOR_IN2, OUTPUT);
}

void loop() {
  digitalWrite(MOTOR_IN1, LOW);
  for (int i=0; i<duration; i++) {
    analogWrite(MOTOR_IN2, slidespeed);
    delay(10);
  }
  digitalWrite(MOTOR_IN2, LOW);
  for (int i=0; i<duration; i++) {
    analogWrite(MOTOR_IN1, slidespeed);
    delay(10);
  }
}

