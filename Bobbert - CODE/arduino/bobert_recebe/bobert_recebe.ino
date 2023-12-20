#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
//#include <LiquidCrystal_I2C.h>

//LiquidCrystal_I2C lcd(0x27, 20, 4);
Adafruit_PWMServoDriver myServo = Adafruit_PWMServoDriver(0x40);
byte servo[16] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};

// conf. do servo VS-SO92J
#define SERVOMIN 230
#define SERVOMAX 520

const byte LED = LED_BUILTIN;

void setup() {
  pinMode(LED, OUTPUT);
  
  myServo.begin();
  myServo.setPWMFreq(60);
  delay(10);

  Serial.begin(115200);
  delay(500);

  // olhos
  mover_servo(14, 180);
  mover_servo(15, 180);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('#');
    input.trim(); // Remove leading/trailing whitespaces

    // Check if the input starts with "angles = ["
    if (input.endsWith(",")) {
    //if (input.startsWith("") && input.endsWith(",'")) {
      // Remove "angles = [" and "]" from the input string
      input = input.substring(0, input.length() - 1);

      // Split the input into individual angle values
      String anglesArray[8]; // Assuming you have 8 angles
      int angleIndex = 0;
      int startIndex = 0;

      // Parse the input string and extract angle values
      for (int i = 0; i < input.length(); i++) {
        if (input.charAt(i) == ',') {
          anglesArray[angleIndex] = input.substring(startIndex, i);
          startIndex = i + 1;
          // Serial.print(startIndex);
          // Serial.print("  -  ");
          angleIndex++;
        }
      }
      //Serial.println(" - OK");

      // Handle the last angle value
      anglesArray[angleIndex] = input.substring(startIndex);
      byte set_angulo_servo;

      // BDA BDB BEA  BEB  PDA  PDB  PEA  PEB
      //  0   1   2    3    4    5    6    7

// braço direito --------------------------------------------------
  // ombro
      set_angulo_servo = constrain(anglesArray[0].toInt(), 10, 160);
      set_angulo_servo = map(set_angulo_servo, 20, 170, 160, 10);
      mover_servo(0,set_angulo_servo);

  // cotovelo
      // set_angulo_servo = constrain(anglesArray[1].toInt(), 15, 110);
      // mover_servo(1,set_angulo_servo);

// braço esquerdo --------------------------------------------------
  // ombro
      set_angulo_servo = constrain(anglesArray[2].toInt(), 10, 160);
      set_angulo_servo = map(set_angulo_servo, 20, 170, 160, 10);
      mover_servo(2,set_angulo_servo);
  // cotovelo
      // set_angulo_servo = constrain(anglesArray[3].toInt(), 70, 160);
      // mover_servo(3,set_angulo_servo);


// perna direito --------------------------------------------------
  // quadril
      set_angulo_servo = constrain(anglesArray[5].toInt(), 70, 160);
      set_angulo_servo = map(set_angulo_servo, 90, 160, 160, 70);
      mover_servo(4,set_angulo_servo);
  // // joelho
  //     set_angulo_servo = constrain(anglesArray[6].toInt(), 70, 160);
  //     mover_servo(5,set_angulo_servo);

// perna esquerda --------------------------------------------------
  // quadril
      set_angulo_servo = constrain(anglesArray[4].toInt(), 70, 160);
      set_angulo_servo = map(set_angulo_servo, 70, 160, 0, 90);
      mover_servo(6,set_angulo_servo);
  // // joelho
  //     set_angulo_servo = constrain(anglesArray[4].toInt(), 70, 160);
  //     mover_servo(7,set_angulo_servo);

// cabeça --------------------------------------------------
      // set_angulo_servo = constrain(anglesArray[8].toInt(), 20, 180);
      // mover_servo(8,set_angulo_servo);

    }
  }
}


void mover_servo(byte index, float angle){
  // ϴ = (angle/(180/(SERVOMAX-SERVOMIN)))+SERVOMIN
  int pulse = (angle/0.5625)+220;
  myServo.setPWM(index, 0, pulse);
}


