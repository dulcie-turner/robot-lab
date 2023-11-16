#Import necessary libraries and modules
from csv_write import *
from data_fetcher import *
from database_write import *
from data_comparison import *
from plc import *

from time import sleep

db = Database()
csv = CSVFile()
plc = PLC()

""" WHAT DOES THIS DO?

Repeatedly loops
    It sends all data it has to the database

    If it gets a signal from the PLC to do a test (and it isn't busy)
        It tests the relevant sensor
        It sends the result to the PLC
        It uploads the result to the database

"""
plc.set_signal("ready")

while True:
    if data_point_present():
        # get data point
        point = get_data_point()
    
        # write to the database
        db.write_point("Temperature", point["temperature"], point["timestamp"], point["logger"])
        db.write_point("Pressure", point["pressure"], point["timestamp"], point["logger"])    
        if point['acceleration'] != []:
            db.write_point("Acceleration_x", point["acceleration"][0], point["timestamp"], point["logger"])
            db.write_point("Acceleration_y", point["acceleration"][1], point["timestamp"], point["logger"])
            db.write_point("Acceleration_z", point["acceleration"][2], point["timestamp"], point["logger"])

    plcMessage = plc.get_test_sensor()

    # if a sensor needs testing
    if plcMessage != None:
        plc.set_signal("busy")

        result = test_logger(plcMessage)

        plc.set_signal(result)
        sleep(2)
        plc.set_signal("ready")

                
    sleep(0.1)