# Import necessary libraries for sensor data
import board
import busio
from adafruit_dps310.basic import DPS310
import adafruit_mcp9808
import adafruit_adxl34x

# Initialize I2C communication for sensors
i2c = busio.I2C(scl=board.GP27,sda=board.GP26)

# Initialize the sensors
dps310 = DPS310(i2c)
mcp = adafruit_mcp9808.MCP9808(i2c)
adxl343 = adafruit_adxl34x.ADXL343(i2c)

# Import additional libraries for communication
import wifi
import time
from communication import *
from message import *

# Connect to Wi-Fi network
wifi.radio.connect('UniOfCam-IoT', 'frrXvRk4')
print("Wifi connected")
# Initialize a communication instance
com=Communication() 


while True:
    # print("dps310 Temperature = %.2f C" % dps310.temperature)
    print("dps310 Pressure = %.2f hPa" % dps310.pressure)   
    print("mcp9808 Temperature = %.2f C" % mcp.temperature) 
    print("adxl343 accelerometer %f %f %f" % adxl343.acceleration)

    # Prepare data for communication
    topic=topic_msg()
    topic.temperature=dps310.temperature    
    topic1=topic.encode()   
    # Publish data 
    com.publish(topic1)
    # Sleep for 1 second before the next iteration
    time.sleep(1)