#include "esp_camera.h"
#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();
 
 

WiFi.begin(ssid, password);

while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
 Serial.println("");
  Serial.println("WiFi connected");

 

Serial.print("Camera Ready! Use 'http://");
Serial.print(WiFi.localIP());
Serial.println("' to connect");
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(10000);
}
