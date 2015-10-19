#include <Servo.h>

Servo panServo;
Servo triggerServo;

int currentServo = 90;
int pos = 70;
int timedelay = 8;
int maxF = 138;
int minF = 60;
int inputPen = 7;

void setup()
{
  Serial.begin(9600);
  panServo.attach(9);
  triggerServo.attach(8);
  pinMode(2, OUTPUT);
  pinMode(3, INPUT);
  moveServo(90);
}

void loop() 
{
  if(digitalRead(inputPen) == HIGH){
    digitalWrite(2, HIGH);
    fire();
    digitalWrite(2, LOW);
    delay(100);
  }
}

void moveServo(int value){
  if(currentServo < value){
    while(currentServo < value){
      panServo.write(currentServo);
      delay(8);
      currentServo++;
    }
  } else {
    while(currentServo > value){
      panServo.write(currentServo);
      delay(8);
      currentServo--;
    }
  }
}

void fire()
{
  delay(2000);
  for(pos = minF; pos <= maxF; pos += 1) // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    triggerServo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(timedelay);                       // waits 15ms for the servo to reach the position 
  } 
  for(pos = maxF; pos>=minF; pos-=1)     // goes from 180 degrees to 0 degrees 
  {                                
    triggerServo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(timedelay/2);                       // waits 15ms for the servo to reach the position 
  } 
}

