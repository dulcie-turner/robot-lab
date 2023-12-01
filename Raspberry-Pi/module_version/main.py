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

sensors = ["temperature", "pressure"]

""" WHAT DOES THIS DO?

Repeatedly loops
    It sends all data it has to the database

    If it gets a signal from the PLC to do a test
        It sends a busy signal
        It tests all three sensors
        It sends the result to the PLC (plus a result ready signal)
        It uploads the result to the database
    Else
        It sends a ready signal

"""
plc.set_signal("ready")

try:
    while True:
        if data_point_present():
            # get data point
            point = get_data_point()
        
            # write to the database
            db.write_point("Temperature", point["temperature"], point["logger"], point["timestamp"])
            db.write_point("Pressure", point["pressure"], point["logger"], point["timestamp"])    
            if point['acceleration'] != []:
                db.write_point("Acceleration_x", point["acceleration"][0], point["logger"], point["timestamp"])
                db.write_point("Acceleration_y", point["acceleration"][1], point["logger"], point["timestamp"])
                db.write_point("Acceleration_z", point["acceleration"][2], point["logger"], point["timestamp"])
                
            # data collection
            # if point["logger"] == 12:    
            #    csv.write(point)

            print("----")


        plcMessage = plc.get_signal()

        # if a sensor needs testing
        if plcMessage == "test":
            plc.set_signal("busy")
            
            # test each sensor and upload results to database
            results = []
            for sensor in sensors:
                print(f"Testing {sensor}")
                results.append(test_logger(sensor))
                db.write_point("result", results[-1].passed, results[-1].logger, tags={"error": results[-1].error, "sensor": results[-1].sensor})

            # briefly send test results to PLC
            plc.set_signal("result", [i.passed for i in results])
            sleep(2)
            plc.set_signal("ready")
          
        sleep(0.05)
        
except KeyboardInterrupt:
    csv.close()        
