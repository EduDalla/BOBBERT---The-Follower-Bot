#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver myServo = Adafruit_PWMServoDriver(0x40);
byte servo[16] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};

// conf. do servo VS-SO92J
#define SERVOMIN 230
#define SERVOMAX 520

const byte LED = 13;

void setup() {
  pinMode(A0, INPUT);
  pinMode(LED, OUTPUT);

  Serial.begin(9600);
  
  myServo.begin();
  myServo.setPWMFreq(60);
  delay(10);

  delay(500);
}

void loop() {
  byte val = analogRead(A0)/5;
  mover_servo(0, val);
  delay(100);

  Serial.print("VALOR ATUAL: ");
  Serial.println(val);
}


void mover_servo(byte index, float angle){
  // ϴ = (angle/(180/(SERVOMAX-SERVOMIN)))+SERVOMIN
  int pulse = (angle/0.5625)+220;
  myServo.setPWM(index, 0, pulse);

}


