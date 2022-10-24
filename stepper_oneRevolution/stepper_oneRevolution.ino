
#include <Stepper.h>
#include <stdio.h>
#include <math.h>
#define d2r (M_PI / 180.0)
//#include "haversine.h"

//21.496412085177443, 39.24574732273937

double angel;
double driction;
double Elevation;
double lat1=21.496375671268357;
double long1=39.246058007460505;
double alt1=50;
double lat2=21.497518838568514;
double long2=39.24244921468016;
double alt2=49.9;
double horizantalD; // degerss between two GPS cordinates 
double verticalD;   // vfertical degree
double drictionH;
double drictionV;
//21.496491195751478, 39.25012739187595  parking alium
//21.496375671268357, 39.246058007460505
//21.497661805293824, 39.24630611095945
//21.497518838568514, 39.24244921468016
const int stepsPerRevolution = 200; 
const int IN_D0 = 12; // digital input IR horizantal
const int IN_D1 = 2; // digital input  IR vertical
bool value_D0; // IR 1
bool value_D1; // IR 2


Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11); // vertical
Stepper myStepper2(stepsPerRevolution, 4, 5, 6, 7); // horizontal


void setup() {
  Serial.begin(9600);
  myStepper.setSpeed(120);
  myStepper2.setSpeed(225);
  pinMode (IN_D0, INPUT);
  pinMode (IN_D1, INPUT);

//   while(value_D0 !=1 || value_D1 !=1){
//      if(value_D0 !=1){
//        value_D0 = digitalRead(IN_D0);// reads the digital input from the IR distance sensor
//        myStepper2.step(240);
//        Serial.println("the value of D  Horizantal is: ");
//        Serial.println(value_D0);
//        delay(10);
//      }
//      
//     if(value_D1 !=1){
//        value_D1 = digitalRead(IN_D1);// reads the digital input from the IR distance sensor
//        myStepper.step(-240);
//        Serial.println("the value of D vetical is: ");
//        Serial.println(value_D1);
//        delay(10);
//     }
//  }
  TrackGPS();
  ElevationAngle();
  dirction();
   
   myStepper2.step(drictionH);
   myStepper.step(drictionV);
  //myStepper.step(3000);
  Serial.print("Assad say :");
  Serial.println(drictionV);
 
}

void loop() {
  
//  myStepper.step(-200);
//     myStepper.step(3500);
//   delay(100);
//   myStepper.step(3500);
    // value_D1 = digitalRead(IN_D1);// reads the digital input from the IR distance sensor
    //myStepper2.step(240);
//     Serial.println("the value of D is: ");
//     Serial.println(value_D1);
//     delay(500);
  Serial.println("1");
//     

}

void dirction(){
   drictionH= (horizantalD/360.0) * 12500.0;
   Serial.println("the steps at Horizantal");
   Serial.println(drictionH);
   drictionV= (verticalD/90.0) * 3500.0;
   Serial.println("the steps at vertical");
   Serial.println(drictionV);
}

void TrackGPS(){
    double dLon = (long2 - long1);
    double y = sin(dLon) * cos(lat2);
    double x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dLon);

    double brng = atan2(y, x);

    brng = (brng*180)/M_PI;
    //brng = (brng + 360);
    //brng =  fmod(brng,360);
    //brng = 360 - brng; // count degrees clockwise - remove to make counter-clockwise
    horizantalD=brng;
   Serial.println("\nthe horizantal angle is :");
   Serial.println(horizantalD);
}
/*
void ElevationAngle(){
    double Distance_NS= abs((lat2-lat1)*1852);
    double Distance_EW= abs(((long2-long1)*1852)*(cos((lat2+lat1)/2)));
    double Distance_Horizontal=sqrt(Distance_NS*Distance_NS+Distance_EW*Distance_EW);
    double Distance_Vertical=alt2-alt1;
    Elevation = atan (Distance_Vertical / Distance_Horizontal);
    Elevation=(Elevation*180)/M_PI;

    Serial.println("\nthe vertical angle is ");   
    Serial.println(Elevation);
    verticalD=-Elevation;                                  
}
*/
 
void ElevationAngle()
{
   double dlong = (long2 - long1) * d2r;
   double dlat = (lat2 - lat1) * d2r;
   double a = pow(sin(dlat/2.0), 2) + cos(lat1*d2r) * cos(lat2*d2r) * pow(sin(dlong/2.0), 2);
   double c = 2 * asin(sqrt(a));
   double d = 6371*1e3 * c;
   Elevation=atan((alt2-alt1)/d);
   Elevation=(Elevation*180)/M_PI;
   Serial.print("\nthe distance in M is "); Serial.println(d);
   verticalD=-Elevation;

   Serial.print(" the elevation angle is  showed : "); Serial.println(Elevation);


}