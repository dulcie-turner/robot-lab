from plc import *
from time import sleep, time

plc = PLC()

toSend = [
    [1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1]
]

index = 0
count = 0

while True:
    print(plc.get_raw())

    if count % (10) == 0:
        plc.set_raw(toSend[index % len(toSend)])
        index += 1
        
    count += 1
    sleep(0.2)
    
    