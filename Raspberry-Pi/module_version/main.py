#Import necessary libraries and modules
from csv_write import *
from data_fetcher import *
from database_write import *
from sensor_test import *
from plc import *

from time import sleep

db = Database()
csv = CSVFile("logger.csv", ['time','temperature','pressure','acceleration_x', 'acceleration_y', 'acceleration_z'])
plc = PLC()

showingTestResult = False
runningTest = False

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
        if packet_present():
            # get a packet of data points

            points = get_data_points()
            
            
            if points:    
                written_timestamps = []
                for point in points:
                    # write to the database
                    if int(point["timestamp"] / 1000) not in written_timestamps:
                        db.write_reading(point)
                        # (only write one reading per second, since it cannot handle millisec timestamps)
                        written_timestamps.append(int(point["timestamp"] / 1000))
                
                    # csv data collection
                    # if point["logger"] == 12:    
                    #    csv.writePoint(point)
                        
        # if a sensor needs testing
        plcMessage = plc.get_signal()
        if plcMessage == "test" and (not runningTest):
            runningTest = True
            plc.set_signal("busy") 
            
            # test each sensor and upload results to database
            results = do_logger_test(plc)
            for r in results:
                db.write_point("result", r.passed, r.logger, tags={"error": r.error, "sensor": r.sensor})

            # send test results to PLC, until they signal that they are finished
            plc.set_signal("result", [r.passed for r in results])
            showingTestResult = True
          
        if plcMessage == "resultReceived" and runningTest:
            print("Results received")
            plc.set_signal("ready")
            showingTestResult = False
            runningTest = False
            
        sleep(0.005)
        
except KeyboardInterrupt:
    csv.close()        
