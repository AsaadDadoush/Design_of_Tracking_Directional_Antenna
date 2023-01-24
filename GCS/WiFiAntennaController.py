from asyncore import loop
import socket
import asyncio
import os
import webbrowser
import serial
from TestAngle_Live import HorizantalAngle, distance, angleElavation, dirction
import numpy as np
from statistics import mean

# Turn off the wlan0 interface
# This may be necessary to avoid interference with other wireless devices
# cmd_wlan0 = 'sudo ifconfig wlan0 down'
# os.system(cmd_wlan0)

# Define the URL to open
url = "http://192.168.4.1"

# Open the URL in a web browser
# try:
#     webbrowser.open(url)
# except Exception as e:
#     # Print an error message if the URL could not be opened
#     print(f"Error opening URL: {e}")

# Initialize variables for the GPS coordinates and other variables
latitude = " "  # Latitude in degrees
longitude = " "  # Longitude in degrees
altitude = ""  # Altitude in meters
# 21.496306448242912, 39.2458077426255
# Initialize the GPS coordinates for the ground control station (GCS)
GCS_LATITUDE = 21.4964005  # Latitude in degrees of the GCS location
GCS_LONGITUDE = 39.2457465  # Longitude in degrees of the GCS location
GCS_ALTITUDE = 32.06     # Altitude in meters of the GCS location

# Initialize variables for the angles and steps of the antenna
OangleH = 0  # Horizontal angle in degrees
OangleV = 0  # Vertical angle in degrees
stepsH = 0  # Horizontal steps
stepsV = 0  # Vertical steps

# Initialize a flag to indicate whether the antenna should recapture the WiFi signal
recapture_flag = False


# Initialize the mobile and esp8266 addresses
mobile_address = ('192.168.4.4', 8008)
esp8266_address = ('192.168.4.4', 8000)

# Create sockets for the mobile and esp8266 connections
# The socket will use the Internet (AF_INET) address family and the
# User Datagram Protocol (UDP) socket type
sock_mobile = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_alt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the sockets to the respective addresses
sock_mobile.bind(mobile_address)
sock_alt.bind(esp8266_address)

# Set a timeout for the sockets to prevent blocking
sock_mobile.settimeout(1)
sock_alt.settimeout(1)

# Initialize lists for storing coordinates, altitudes, and directions
cordinates = []
altitudes = []
directionqx = []
PrevCordinates = []

# Uncomment the following line to open a serial connection
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()


async def mobile_udp():
    global latitude, longitude, recapture_flag

    # Run this loop indefinitely
    while True:
        # Sleep for a small amount of time to avoid using too many resources
        await asyncio.sleep(1)

        # Send the string "ping" to the specified address and port
        # sock_mobile.sendto(b'ping', ('192.168.100.3', 8008))

        # Set a timeout of 1 second for receiving data from the client
        # sock_mobile.settimeout(1)

        try:
            # Receive data from the client, with a buffer size of 1024 bytes
            data, client_address = sock_mobile.recvfrom(1024)
            # print(data)

        except socket.timeout:
            # If no data is received within the timeout period, print a message and set the recapture flag
            print("No connection from Mobile Phone")
            recapture_flag = True
            # Uncomment these lines to call the Prediction(), Track(), and Recapture() functions
            if (len(PrevCordinates) != 0):
                prediction()
                track()

        else:
            # If data is received within the timeout period, reset the recapture flag
            recapture_flag = False

            # Decode the received data from bytes to a string
            udp_string = data.decode('utf8')

            # Split the string on the comma character and retrieve the second element (the checksum)
            # checksum = udp_string.split(',')[1]

            # print("TEST connection established")

            # If the checksum is "1", process the received latitude and longitude values
            # if "1" in checksum:
            latitude = float(udp_string.split(',')[0])
            longitude = float(udp_string.split(',')[1])
            # print(latitude, longitude)

            # If the altitude value is not empty, append the latitude, longitude, and altitude values to the cordinates and PrevCordinates lists
            if altitude:
                cordinates.append(latitude)
                cordinates.append(longitude)
                cordinates.append(altitude)

                temp = []
                temp.append(latitude)
                temp.append(longitude)
                temp.append(altitude)
                # print(temp)

                PrevCordinates.append(temp)
                # print(PrevCordinates)

                # Uncomment this line to call the Track() function
                track()


async def esp8266_udp():
    global altitude

    # Run this loop indefinitely
    while True:
        # Sleep for a small amount of time to avoid using too many resources
        await asyncio.sleep(0.2)

        try:
            # Receive data from the client, with a buffer size of 1024 bytes
            data, addr = sock_alt.recvfrom(1024)

        except socket.timeout:
            # If no data is received within the timeout period, print a message
            print("No connection from ESP8266")

        else:
            # If data is received, decode it from bytes to a string
            alt_udp_string = data.decode('utf8')

            # Split the string on the comma character and retrieve the first element (the altitude value)
            altitude = float(alt_udp_string.split(',')[0])
            # Print the altitude value in meters
            # print("altitude in m: ", altitude)


async def recapture():
    while True:
        await asyncio.sleep(0.4)
        if (recapture_flag == True):
            test = [20, 25]
            directionqx.append(test)
            print("Recapture mode")


def serial_uno():
    # Create an empty string to store the received data
    receive_string_new = ""

    # Run this loop indefinitely
    global stepsH, stepsV

    # Sleep for a small amount of time to avoid using too many resources

    # If the directionqx list is not empty
    if len(directionqx) != 0:
        # Print the first element of the directionqx list (a tuple of two integers)
        # print("Steps_Serial: ", directionqx[0])

        # Assign the first and second elements of the tuple to the stepsH and stepsV variables, respectively
        stepsH = directionqx[0][0]
        stepsV = directionqx[0][1]

        # Convert the stepsH and stepsV values to strings
        angle_value_list = [str(stepsH), str(stepsV)]

        # Join the strings with a comma separator
        send_string = ','.join(angle_value_list)

        # Add a newline character to the end of the string
        send_string += "\n"

        # Send the string to the Arduino. Make sure you encode it before sending.
        ser.write(send_string.encode('utf-8'))

        # Receive data from the Arduino and decode it from bytes to a string
        receive_string = ser.readline().decode('utf-8', 'replace').rstrip()

        # Print the data received from Arduino to the terminal
        # print("------------------------------------------------")
        # print("PC H:  ", stepsH, " PC V:  ", stepsV)
        print("Mega Steps: ", receive_string)
        print("Pi Steps", send_string)
        print("------------------------------------------------")
        print(" ")

        # If the received string is not empty and is different from the previous received string
        if len(receive_string) != 0 and receive_string_new != receive_string:
            # Print the directionqx list
            print(directionqx)
            # Remove the first element of the directionqx list
            del directionqx[0]
            # Update the receive_string_new variable with the received string
            receive_string_new = receive_string
            # Print the updated directionqx list
            # print(directionqx)


def track():
    # Declare OangleH and OangleV as global variables
    global OangleH, OangleV

    # If the length of cordinates is greater than 3 or equal to 3
    if len(cordinates) > 3 or len(cordinates) == 3:
        # Assign the first three elements of cordinates to lat2, long2, and alt2
        lat2, long2, alt2 = cordinates[:3]
        # PrevCordinates.append(cordinates)

        # Print the current coordinates
        # print("The current coordinates are:", cordinates)

        # Calculate the distance between the GCS coordinates and the current coordinates
        d = distance(GCS_LATITUDE, float(lat2), GCS_LONGITUDE, float(long2))

        # Calculate the horizontal angle between the GCS coordinates and the current coordinates
        horizantal_angle = HorizantalAngle(
            GCS_LATITUDE, GCS_LONGITUDE, float(lat2), float(long2))

        # Calculate the elevation angle between the GCS coordinates and the current coordinates
        elevation_angle = angleElavation(d, float(alt2), GCS_ALTITUDE)

        # Calculate the difference between the current horizontal angle and the previous horizontal angle
        NangleH = horizantal_angle - OangleH

        # Calculate the difference between the current elevation angle and the previous elevation angle
        NangleV = elevation_angle - OangleV

        # Calculate the direction based on the differences in the horizontal and vertical angles
        directionq = dirction(NangleH, NangleV)

        # If the direction is not (0, 0)
        if directionq[0] != 0 or directionq[1] != 0:
            # If the distance is greater than or equal to 2
            if d >= 10:
                # Append the direction to directionqx
                directionqx.append(directionq)
                serial_uno()
                print("latitude: ", latitude)
                print("longitude: ", longitude)
                print("altitude: ", altitude)
                print("The distance is", d)
                print(directionqx)
                print()
            else:
                print("close range mode: ",d)

                # Print the horizontal and vertical angles and the number of steps in the direction
                # print("The horizontal angle is", horizantal_angle)
                # print("The vertical angle is", elevation_angle)
                # print("The number of steps is:", directionq)

                # Print the distance
        # print("The distance is", d)

        # Update the previous horizontal and vertical angles
        OangleH = horizantal_angle
        OangleV = elevation_angle

        # Remove the first three elements from cordinates
        del cordinates[:3]
        # print("TEST")
        # If the length of PrevCordinates is equal to 30
        if len(PrevCordinates) == 20:
            # print(PrevCordinates)
            # Remove the first three elements from PrevCordinates
            del PrevCordinates[:3]

        # else:
        #     # Print "out"
        #     print("out")


def prediction():
    if (recapture_flag == True):
        print("Prediction mode")

        # Calculate the mean change in latitude, longitude, and altitude
        # by finding the differences between consecutive coordinates
        # in each respective dimension and taking the mean of those differences
        lat_change = mean(np.diff([lat for lat, _, _ in PrevCordinates]))
        long_change = mean(np.diff([long for _, long, _ in PrevCordinates]))
        alti_change = mean(np.diff([alti for _, _, alti in PrevCordinates]))

        # Get the last coordinate in the list
        lat, long, alti = PrevCordinates[-1]

        # Calculate the predicted coordinate by adding the mean change
        # in each dimension to the last coordinate
        predicted_coord = [lat + lat_change,
                           long + long_change, alti + alti_change]

        # Print the predicted coordinate

        # print("Predicted cordinates :", predicted_coord)  # Output
        cordinates.append(predicted_coord[0])
        cordinates.append(predicted_coord[1])
        cordinates.append(predicted_coord[2])
        # print(cordinates)
        PrevCordinates.append(predicted_coord)


# Get the event loop
loop = asyncio.get_event_loop()

# Try to run the event loop with the tasks
try:
    # Start the Mobile_UDP task asynchronously
    asyncio.ensure_future(mobile_udp())
    asyncio.ensure_future(esp8266_udp())
    # asyncio.ensure_future(recapture())

    # Run the event loop indefinitely
    loop.run_forever()

# Except for a keyboard interrupt
except KeyboardInterrupt:
    # Do nothing
    pass

# Finally, close the event loop
finally:
    # Print a message
    print("Closing Loop")

    # Close the event loop
    loop.close()
