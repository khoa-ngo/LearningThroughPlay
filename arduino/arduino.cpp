#include <Wire.h>
#include "arduino.h"

int32_t gYZero;
int32_t angle; // millidegrees
int bucketized_angle;
int32_t angleRate; // degrees/s
int bucketized_angleRate;
int32_t qbrain_index[6][6] = \
  {{11, 12, 13, 14, 15, 16}, \
  {21, 22, 23, 24, 25, 26}, \
  {31, 32, 33, 34, 35, 36}, \
  {41, 42, 43, 44, 45, 46}, \
  {51, 52, 53, 54, 55, 56}, \
  {61, 62, 63, 64, 65, 66}};
int32_t speed = 50;
int32_t qbrain[6][6] = \
  {{-300, -150, -100, -100, -50, 60}, \
  {-250, -100, -70, -30, -20, 60}, \
  {-170, -100, -40, -20, 30, 120}, \
  {-130, -80, 0, 20, 120, 180}, \
  {-90, -70, 50, 70, 130, 180}, \
  {-50, 50, 100, 120, 150, 300}};
int32_t action = 0;
int32_t distanceLeft;
int32_t speedLeft;
int32_t driveLeft;
int32_t distanceRight;
int32_t speedRight;
int32_t driveRight;
int16_t motorSpeed;
int i;
bool isBalancingStatus;
bool balanceUpdateDelayedStatus;

bool isBalancing()
{
  return isBalancingStatus;
}

bool balanceUpdateDelayed()
{
  return balanceUpdateDelayedStatus;
}

void balanceSetup()
{
  // Initialize IMU.
  Wire.begin();
  if (!imu.init())
  {
    while(true)
    {
      Serial.println("Failed to detect and initialize IMU!");
      delay(200);
    }
  }
  imu.enableDefault();
  imu.writeReg(LSM6::CTRL2_G, 0b01011000); // 208 Hz, 1000 deg/s

  // Wait for IMU readings to stabilize.
  delay(1000);

  // Calibrate the gyro.
  int32_t total = 0;
  for (int i = 0; i < CALIBRATION_ITERATIONS; i++)
  {
    imu.read();
    total += imu.g.y;
    delay(1);
  }

  gYZero = total / CALIBRATION_ITERATIONS;
}

void bucketize(int32_t angle, int32_t angleRate) {
  if (angle < -10000) bucketized_angle = 0;
  if (angle > -10000 && angle < -5000) bucketized_angle = 1;
  if (angle > -5000 && angle < 0) bucketized_angle = 2;
  if (angle > 0 && angle < 5000) bucketized_angle = 3;
  if (angle > 5000 && angle < 10000) bucketized_angle = 4;
  if (angle > 10000) bucketized_angle = 5;

  if (angleRate < -100) bucketized_angleRate = 0;
  if (angleRate > -50 && angleRate < -20) bucketized_angleRate = 1;
  if (angleRate > -20 && angleRate < 0) bucketized_angleRate = 2;
  if (angleRate > 0 && angleRate < 20) bucketized_angleRate = 3;
  if (angleRate > 20 && angleRate < 50) bucketized_angleRate = 4;
  if (angleRate > 100) bucketized_angleRate = 5;
  // Serial.print(bucketized_angle);
  // Serial.print('\t');
  // Serial.print(bucketized_angleRate);
  // Serial.print('\t');
}



int32_t truncate(int32_t value) {
  float new_value;
  new_value = value / 10000.0f;
  new_value = (new_value > (floor(new_value)+0.5f)) ? ceil(new_value) : floor(new_value);
  return int32_t(new_value*10000);
}
// This function contains the core algorithm for balancing a
// Balboa 32U4 robot.
void balance()
{
  // Adjust toward angle=0 with timescale ~10s, to compensate for
  // gyro drift.  More advanced AHRS systems use the
  // accelerometer as a reference for finding the zero angle, but
  // this is a simpler technique: for a balancing robot, as long
  // as it is balancing, we know that the angle must be zero on
  // average, or we would fall over.
  angle = angle * 999 / 1000;
  // Serial.print(angle);
  // Serial.print('\t');

  // This variable measures how close we are to our basic
  // balancing goal - being on a trajectory that would cause us
  // to rise up to the vertical position with zero speed left at
  // the top.  This is similar to the fallingAngleOffset used
  // for LED feedback and a calibration procedure discussed at
  // the end of Balancer.ino.
  //
  // It is in units of millidegrees, like the angle variable, and
  // you can think of it as an angular estimate of how far off we
  // are from being balanced.
  // int32_t risingAngleOffset = angleRate * ANGLE_RATE_RATIO + angle;
  int32_t balanceOutput = (angleRate * ANGLE_RATE_RATIO + angle)*ANGLE_RESPONSE;
  // balanceOutput = truncate(balanceOutput);
  // balanceOutput = constrain(balanceOutput, -300000, 300000);
  // Serial.print(truncate(balanceOutput));
  // Serial.print('\t');

  // Experimental AI
  bucketize(angle, angleRate);

  // Combine risingAngleOffset with the distance and speed
  // variables, using the calibration constants defined in
  // Balance.h, to get our motor response.  Rather than becoming
  // the new motor speed setting, the response is an amount that
  // is added to the motor speeds, since a *change* in speed is
  // what causes the robot to tilt one way or the other.
  // balanceOutput = qbrain[bucketized_angle][bucketized_angleRate] * 1000;
  motorSpeed += ( balanceOutput
    + DISTANCE_RESPONSE * (distanceLeft + distanceRight)
    + SPEED_RESPONSE * (speedLeft + speedRight)
    ) / 100 / GEAR_RATIO;

  Serial.print(angle);
  Serial.print('\t');
  Serial.print(angleRate);
  Serial.print('\t');
  Serial.println(motorSpeed);

  // motorSpeed += (
  //   + qbrain[bucketized_angle][bucketized_angleRate]*1000
  //   + DISTANCE_RESPONSE * (distanceLeft + distanceRight)
  //   + SPEED_RESPONSE * (speedLeft + speedRight)
  //   ) / 100 / GEAR_RATIO;
  
  if (motorSpeed > MOTOR_SPEED_LIMIT)
  {
    motorSpeed = MOTOR_SPEED_LIMIT;
  }
  if (motorSpeed < -MOTOR_SPEED_LIMIT)
  {
    motorSpeed = -MOTOR_SPEED_LIMIT;
  }

  // Adjust for differences in the left and right distances; this
  // will prevent the robot from rotating as it rocks back and
  // forth due to differences in the motors, and it allows the
  // robot to perform controlled turns.
  int16_t distanceDiff = distanceLeft - distanceRight;

  motors.setSpeeds(
    motorSpeed + distanceDiff * DISTANCE_DIFF_RESPONSE / 100,
    motorSpeed - distanceDiff * DISTANCE_DIFF_RESPONSE / 100);
}

void lyingDown()
{
  // Reset things so it doesn't go crazy.
  motorSpeed = 0;
  distanceLeft = 0;
  distanceRight = 0;
  motors.setSpeeds(0, 0);

  if (angleRate > -2 && angleRate < 2)
  {
    // It's really calm, so we know the angles.
    if (imu.a.z > 0)
    {
      angle = 110000;
    }
    else
    {
      angle = -110000;
    }
    distanceLeft = 0;
    distanceRight = 0;
  }
}

void integrateGyro()
{
  // Convert from full-scale 1000 deg/s to deg/s.
  angleRate = (imu.g.y - gYZero) / 29;

  angle += angleRate * UPDATE_TIME_MS;
}

void integrateEncoders()
{
  static int16_t lastCountsLeft;
  int16_t countsLeft = encoders.getCountsLeft();
  speedLeft = (countsLeft - lastCountsLeft);
  distanceLeft += countsLeft - lastCountsLeft;
  lastCountsLeft = countsLeft;

  static int16_t lastCountsRight;
  int16_t countsRight = encoders.getCountsRight();
  speedRight = (countsRight - lastCountsRight);
  distanceRight += countsRight - lastCountsRight;
  lastCountsRight = countsRight;
}

void balanceDrive(int16_t leftSpeed, int16_t rightSpeed)
{
  driveLeft = leftSpeed;
  driveRight = rightSpeed;
}

void balanceDoDriveTicks()
{
  distanceLeft -= driveLeft;
  distanceRight -= driveRight;
  speedLeft -= driveLeft;
  speedRight -= driveRight;
}

void balanceResetEncoders()
{
  distanceLeft = 0;
  distanceRight = 0;
}

void balanceUpdateSensors()
{
  imu.read();
  integrateGyro();
  integrateEncoders();
}

void balanceUpdate() {
  static uint16_t lastMillis;
  uint16_t ms = millis();

  // Perform the balance updates at 100 Hz.
  if ((uint16_t)(ms - lastMillis) < UPDATE_TIME_MS) { return; }
  balanceUpdateDelayedStatus = ms - lastMillis > UPDATE_TIME_MS + 1;
  // Serial.print(ms-lastMillis);
  // Serial.print('\t');
  // Serial.println(ms-lastMillis-5);
  lastMillis = ms;

  balanceUpdateSensors();
  balanceDoDriveTicks();

  if (imu.a.x < 0)
  {
    lyingDown();
    isBalancingStatus = false;
  }
  else
  {
    balance();
    isBalancingStatus = true;
  }
}
