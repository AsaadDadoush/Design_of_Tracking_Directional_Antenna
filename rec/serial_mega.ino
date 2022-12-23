#include <Stepper.h>
#include <stdio.h>

const int stepsPerRevolution = 200; 
const int IN_D0 = 12; // digital input IR horizantal
const int IN_D1 = 2; // digital input  IR vertical
bool value_D0; // IR 1
bool value_D1; // IR 2


Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11); // vertical
Stepper myStepper2(stepsPerRevolution, 4, 5, 6, 7); // horizontal

void setup() {

Serial.begin(9600);
myStepper.setSpeed(90);
myStepper2.setSpeed(170);
pinMode (IN_D0, INPUT);
pinMode (IN_D1, INPUT);
Serial.setTimeout(25);
value_D0 = digitalRead(IN_D0);
value_D1 = digitalRead(IN_D1);
delay(1000);


Serial.flush();
//while(value_D0 !=1 || value_D1 !=1){
//      if(value_D0 !=1){
//        value_D0 = digitalRead(IN_D0);// reads the digital input from the IR distance sensor
//        myStepper2.step(20);
////        Serial.println("the value of D  Horizantal is: ");
////        Serial.println(value_D0);
//        delay(10);
//      }
//      
//     if(value_D1 !=1){
//        value_D1 = digitalRead(IN_D1);// reads the digital input from the IR distance sensor
//        myStepper.step(20);
////        Serial.println("the value of D vetical is: ");
////        Serial.println(value_D1);
//        delay(10);
//     }
// }

    delay(2000);


}


int StepsH=0;   
int StepsV=0;

int StepsH_new = 0;
int StepsV_new = 0;

bool motor_flag = false; 
bool read_flag = true;
bool flag_read = true;

void loop() {

 
   Read();
   motor();
   delay(100);

}
   

void signal_motor(){

  
  Serial.println("T");
  Serial.println(" ");
  Serial.println(" ");
    
  }
  
  

void Read(){
  
  if(flag_read == 1){
  if(Serial.available() > 0){
    StepsH = Serial.parseInt();
 
    StepsV = Serial.parseInt();
  
    Serial.print(StepsH);Serial.println(StepsV);
    delay(10);
    if (StepsH_new != StepsH || StepsV_new != StepsV){
     flag_read = false;
    }
   }
 }
}

void motor(){

   if (StepsH_new != StepsH || StepsV_new != StepsV && flag_read == 0){
       myStepper.step(StepsV);
       delay(50);
       myStepper2.step(StepsH);
       delay(50);
       StepsH_new = StepsH;
       StepsV_new = StepsV;
       flag_read = true;
       
   }

   StepsH = 0;
   StepsV = 0;

  

}
