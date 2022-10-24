String a;
String rssi_ser =" ";
String latitude_ser = " ";
String longitude_ser = " ";
String altitude_ser = " ";

int rssi=0;
float latitude =0.0000000;
float longitude=0.0000000;
float altitude = 0.0000000;

void setup() {

Serial.begin(115200); // opens serial port, sets data rate to 9600 bps
Serial.setTimeout(25);
}

void loop() {

while(Serial.available()) {

a= Serial.readString();// read the incoming data as string
rssi_ser= a.substring(0,3); rssi = rssi_ser.toInt();
latitude_ser= a.substring(6,15); latitude = latitude_ser.toFloat();
longitude_ser= a.substring(18,26); longitude = longitude_ser.toFloat();
altitude_ser = a.substring(28,32); altitude = altitude_ser.toFloat();
//Serial.print("RSSI:      ");Serial.println(rssi_ser);
//Serial.print("Latitude:  ");Serial.println(latitude_ser);
//Serial.print("Longitude: ");Serial.println(longitude_ser);

//rssi = rssi_ser.toInt();
//latitude = latitude_ser.toFloat();
//longitude = longitude_ser.toFloat();

Serial.print("RSSI:      ");Serial.println(rssi);
Serial.print("Latitude:  ");Serial.println(latitude,6);
Serial.print("Longitude: ");Serial.println(longitude,6);
Serial.print("Altitude: ");Serial.println(altitude,2);




}

}
