
from array import array
from asyncore import loop
from pathlib import Path
import socket
import csv
import asyncio
from time import sleep
import os
import time


altitude = 50     
longitude = 39.245814456835774
latitude = 21.499358320077228

# data to write
header_row = ['office_name', 'num_employees']
os.remove("countries.csv")

async def Read_UDP():
    while True:
        await asyncio.sleep(0.1)
        with open(r'countries.csv', 'a', newline='') as csvfile:
            fieldnames = ['latitude','longitude','altitude']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'latitude':latitude, 'longitude':longitude,'altitude':altitude})


async def Read_sDP():
    while True:
        await asyncio.sleep(10)
        with open(r'countries.csv', 'a', newline='') as csvfile:
            fieldnames = ['latitude','longitude','altitude']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'latitude':"HERE", 'longitude':"Delay",'altitude':"mine"})

            

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(Read_UDP())
    asyncio.ensure_future(Read_sDP())
    loop.run_forever()

except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()	