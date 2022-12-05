from array import array
from asyncore import loop
import socket
import csv
import asyncio
from time import sleep
import os
# import serial
import time
from TestAngle_Live import HorizantalAngle, distance, angleElavation, dirction
# cmd_wlan0 = 'sudo ifconfig wlan0 down'
# cmd = 'iwconfig wlxaa0510003923 | grep -i quality > RSSI.csv'
# os.system(cmd_wlan0)
# os.system(cmd)
latitude = "E"
longitude = "E"
altitude = "E" 

UDP_IP = "192.168.43.181"
UDP_PORT = 8000

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))  
cordinates = []
directionqx=[]

# ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
# ser.flush()



async def Read_UDP():
    global GPS_UDP
    while True:
        await asyncio.sleep(0.001)
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        #print("received message: %s" % data)
        lat_UDP = data[18:26].decode()
        long_UDP = data[30:38].decode()
        altitude_UDP = data[41:46].decode()
        GPS_UDP = [lat_UDP, long_UDP, altitude_UDP]
        # print(GPS_UDP)


async def Open_CSV():
    global lat_csv
    global long_csv
    global altitude_csv
    while True:
        await asyncio.sleep(0.01)
        with open('GPS.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(GPS_UDP)

        with open('GPS.csv', 'r') as file:
            reader = csv.reader(file)
            for each_row in reader:
                if each_row:
                    lat_csv = each_row[0]
                    long_csv = each_row[1]
                    altitude_csv = each_row[2]
                    
                
            # print(long_csv)
            # print(lat_csv)
            # print(altitude_csv)


# async def Read_into():
#     #os.remove("countries.csv")
#     while True:
#         await asyncio.sleep(0.05)
#         with open(r'countries.csv', 'a', newline='') as csvfile:
#             fieldnames = ['latitude', 'longitude', 'altitude']
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             if (latitude != "E" and longitude != "E" and altitude != "E"):
#                 writer.writerow({'latitude': latitude, 'longitude': longitude, 'altitude': altitude})
#                 print("| Latitude:  ", latitude, "  |")
#                 print("| Longitude: ", longitude, "  |")
#                 print("| Altitude:  ", altitude, "      |")


async def Get_GPS():
    global latitude
    global longitude
    global altitude
    while True:
        await asyncio.sleep(0.05)
       # print(lat_csv[1:10])
        if lat_csv[0:1] == "2" and long_csv[0:1] == "3":
            latitude = lat_csv
            longitude = long_csv
            altitude = altitude_csv
            cordinates.append(latitude)
            cordinates.append(longitude)
            cordinates.append(altitude)

            # print(cordinates)
            # print("Latitude: ","", latitude)
            # print("Longitude: ", longitude)
            # print("Altitude: ","", altitude)


async def RSSI_Read():
    global RSSI
    while True:
        await asyncio.sleep(0)
        os.system(cmd)
        with open('RSSI.csv', 'r') as file:
            reader = csv.reader(file)
            for each_row in reader:
                if each_row:
                    RSSI_csv = each_row
                    RSSI_py = RSSI_csv[0].split()[-2]
                    RSSI = RSSI_py[6:9]
                    # print('RSSI: ',RSSI)


async def monitor():
    while True:
        await asyncio.sleep(1)
        print("="*26)
        print("| Latitude:  ", latitude, "  |")
        print("| Longitude: ", longitude, "  |")
        print("| Altitude:  ", altitude, "      |")
        # print("| RSSI:      ", RSSI, "       |")
        print("="*26)


async def Serial_UNO():
    latitude = 21.756545
    longitude = 39.234567
    altitude = 69.9
    while True:
        await asyncio.sleep(0)

        angle_value_list = [str(RSSI), str(","), str(latitude), str(
            ","), str(longitude), str(altitude), str("  ")]
        send_string = ','.join(angle_value_list)
        send_string += "\n"

        # Send the string. Make sure you encode it before you send it to the Arduino.
        ser.write(send_string.encode('utf-8'))

        # Receive data from the Arduino
        receive_string = ser.readline().decode('utf-8', 'replace').rstrip()

        # Print the data received from Arduino to the terminal
        print(receive_string)
async def Track():
    print("test")
    lat1 = 21.496377 #GCI location
    long1 =39.245740
    alt1=50
    OangleH = 0
    OangleV = 0
    while True:
        await asyncio.sleep(0.3)
        if(len(cordinates > 3)):
            lat2=cordinates[0]
            long2=cordinates[1]
            alt2=cordinates[2]

            d = distance(lat1, float(lat2), long1, float(long2))
            horizantalAngle = (HorizantalAngle(lat1, long1, float(lat2), float(long2)))
            ElevationAngle = (angleElavation(d, float(alt2), alt1))
            NangleH = horizantalAngle - OangleH
            NangleV = ElevationAngle - OangleV
            directionq = dirction(NangleH, NangleV)

            directionqx.append(directionq)

            print("Hi you are start  ")
            print("the horizantal angle is ", horizantalAngle)
            print("the vertical angle is ", ElevationAngle)
            print("the destance is ", d)
            print("the numbers of steps is :", directionq)
            #################################

            OangleH = horizantalAngle
            OangleV = ElevationAngle
            print("")
            
            del cordinates[0]
            del cordinates[2]
            del cordinates[1]
loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(Read_UDP())
    asyncio.ensure_future(Open_CSV())
    asyncio.ensure_future(Get_GPS())
    #asyncio.ensure_future(Read_into())
    asyncio.ensure_future(Track())
    # # asyncio.ensure_future(RSSI_Read())
    # asyncio.ensure_future(monitor())
    # # asyncio.ensure_future(Serial_UNO())
    loop.run_forever()

except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()
