# Import necessary libraries for sensor data
import board
import busio
from adafruit_dps310.basic import DPS310
import adafruit_mcp9808
import adafruit_adxl34x

# Start with sensors, i2c and communication not set up
dps310 = mcp = adxl343 = None
i2c = None
com = None

# Functions to attempt to connect to sensors
def connectPressure():
    try:
        dps310 = DPS310(i2c)
        return dps310
    except:
        print("Pressure not connected")

def connectTemp():
    try:
        mcp = adafruit_mcp9808.MCP9808(i2c)
        return mcp
    except:
        print("Temperature not connected")

def connectAccel():
    try:
        adxl343 = adafruit_adxl34x.ADXL343(i2c)
        return adxl343
    except:
        print("Acceleration not connected")

# Import additional libraries for communication
import wifi
import time
from communication import *
from message import *
from logger import *

logger = getLoggers()

topics = []
wifiConnected = False
while not wifiConnected:
    try:
        # Try to connect to Wi-Fi network
        wifi.radio.connect('UniOfCam-IoT', logger.password)
        wifiConnected = True
        print("Wifi connected")
    except Exception as e:
        print(f"Unable to connect to WiFi: {e}")

readingInterval = 0.015 # this is an approx value
packetSize = 0.3 / readingInterval  # also approximate (should be equal to 5 seconds ish)

lastTime = time.monotonic()

while True:
    # Try to connect to i2c
    if i2c == None:
        try:
            i2c = busio.I2C(scl=board.GP27,sda=board.GP26)
        except RuntimeError:
            print("No sensors")
            i2c = None
    
    else:
        # Try to connect to Mosquitto
        if com == None:
            try:
                com = Communication()
            except:
                print("Could not connect to Mosquitto")
                com = None
        else:
            # Prepare data for communication
            topic=topic_msg()
            
            # If the pressure sensor is connected, try to take a reading
            if dps310 != None:
                try:
                    # print("dps310 Pressure = %.2f hPa" % dps310.pressure)
                    topic.press=dps310.pressure
                except:
                    print("Couldn't get pressure")
                    dps310 = None
            else:
                dps310 = connectPressure()

            # If the temperature sensor is connected, try to take a reading
            if mcp != None:
                try:
                    # print("mcp9808 Temperature = %.2f C" % mcp.temperature)
                    topic.temp=mcp.temperature
                except:
                    print("Couldn't get temperature")
                    mcp = None
            else:
                mcp = connectTemp()

            # If the accelerometer sensor is connected, try to take a reading
            if adxl343 != None:
                try:
                    # print("adxl343 accelerometer %f %f %f" % adxl343.acceleration)
                    relative_acc = adxl343.acceleration # (relative to the accelerometer)
                    topic.acc = [relative_acc[2], relative_acc[1], relative_acc[0]] # reorder axes
                except:
                    print("Couldn't get acceleration")
                    adxl343 = None
            else:
                adxl343 = connectAccel()
            
            encoded_topic=topic.encode()   
            topics.append(encoded_topic)
            
            if len(topics) > packetSize:
                # Try to publish data
                try:
                    topics.append(logger.number)
                    com.publish(f'service/topic/{logger.number}', topics)
                    topics = []
                    
                    # print(f"sent w {time.monotonic() - lastTime}s del")
                    lastTime = time.monotonic()
                except Exception as e:
                    topics = []
                    com = None

    # Sleep before the next iteration"""
    time.sleep(readingInterval)
