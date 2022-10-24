

import math
from math import radians, cos, sin, asin, sqrt, atan, degrees
lat1 = 21.496377
lat2 = 21.498717600944747
long1 =39.245740
long2 =39.24846547044492
alt1=50
alt2=20



def angleFromCoordinate(lat1, long1, lat2, long2):
    dLon = (long2 - long1)

    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)

    brng = math.atan2(y, x)

    brng = math.degrees(brng)
    #brng = (brng + 360) % 360
    #brng = 360 - brng # count degrees clockwise - remove to make counter-clockwise
    
    return brng 
 
# x=angleFromCoordinate(21.49734, 39.24562,21.49631, 39.24586)
# print('the angle is :',x)


def distance(lat1, lat2, lon1, lon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2.0)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    d=c * r *1000
    return d
     
def angleElavation (d,alt2,alt1):
    virtis=alt2 - alt1
    angle=degrees(atan(virtis/d))
    return angle

def dirction(horizantalD,verticalD) :
   drictionH= (horizantalD/360.0) * 12500.0;
   #print("the steps of Horizantal angle is :",drictionH)
   drictionV= (-verticalD/90.0) * 3500.0;
   #print("the vertical steps are :",drictionV)  
   return drictionH,drictionV
   

d=distance(lat1, lat2, long1, long2)
horizantalAngle=angleFromCoordinate(lat1, long1, lat2, long2)
ElevationAngle=angleElavation (d,alt2,alt1) 
steps =dirction(horizantalAngle,ElevationAngle)
print("Hi you are start ")
print("the horizantal angle is ",horizantalAngle)
print("the distance is :",d)
print("the vertical angle is ",ElevationAngle)
print("the stpes of motors are :",steps)

