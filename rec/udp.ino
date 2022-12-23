/* This code is to use with Adafruit BMP280           (Metric)
 * It measures both temperature and pressure and it displays them on the Serial monitor with the altitude
 * It's a modified version of the Adafruit example code
 * Refer to www.surtrtech.com or SurtrTech Youtube channel
 */

#include <Adafruit_BMP280.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

Adafruit_BMP280 bmp; // I2C Interface

String gpsString;
const char * ssid = "KAU_Tracker";
const char * pwd = "1234567890";

const char * udpAddress = "192.168.4.2";
const int udpPort = 8000;

WiFiUDP udp;

char result[8];

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, pwd);
  Serial.println("");
  Serial.println(F("BMP280 test"));

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  //This initializes udp and transfer buffer
  udp.begin(udpPort);

  if (!bmp.begin(0x76)) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    while (1);
  }

  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void loop() {
//    Serial.print(F("Temperature = "));
//    Serial.print(bmp.readTemperature());
//    Serial.println(" *C");
//
//    Serial.print(F("Pressure = "));
//    Serial.print(bmp.readPressure()/100); //displaying the Pressure in hPa, you can change the unit
//    Serial.println(" hPa");

    Serial.print(F("Approx altitude = "));
    Serial.print(bmp.readAltitude(1013.5)); //The "1019.66" is the pressure(hPa) at sea level in day in your region
    Serial.println(" m");                    //If you don't know it, modify it until you get your current altitude

    Serial.println();
    float high=bmp.readAltitude(1013.5);
    
    Serial.println(dtostrf(high, 6, 2, result));
  
    //send hello world to server
    udp.beginPacket(udpAddress, udpPort);
    udp.write(dtostrf(high, 6, 2, result));
    udp.endPacket(); 
    delay(100);
}
