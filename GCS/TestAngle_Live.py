

import math

from math import radians, cos, sin, asin, sqrt, atan, degrees
def HorizantalAngle(lat1, long1, lat2, long2):
    dLon = (long2 - long1)

    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)

    angle = math.atan2(y, x)

    angle = math.degrees(angle)
    #brng = (brng + 360) % 360
    #brng = 360 - brng # count degrees clockwise - remove to make counter-clockwise
    
    return angle
 

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
   
    
def dirction(horizantalD,verticalD) : # calclate the steps of motors
        drictionH= (horizantalD/360.0) * 12500.0 ;  # notice yasterday U R changed
        #print("the steps of Horizantal angle is :",drictionH)
        drictionV= (-verticalD/90.0) * 3500.0 ;
        #print("the vertical steps are :",drictionV
        return round(drictionH),round(drictionV)




    
    
    


