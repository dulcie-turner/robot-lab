"""
WHAT THIS DOES:
    Get a data feed for the relevant sensors
    Using the relevant algorithm, validate the sensors
"""

from data_compare import *
from time import sleep

# sensors to test and their order
sensors = ["temperature", "pressure", "acceleration"]

loggers_to_ignore = []

def do_logger_test(plc):
    # test each sensor in a logger
    results = []
    for sensor in sensors:
        if sensor == "acceleration":
            # request shaking
            plc.set_signal("shakeRequest")
            print("Waiting for PLC to start shaking")
            
            # wait until PLC has started shaking
            while plc.get_signal() != "shaking":
                sleep(0.01)
                
            # run test
            print("PLC shaking has started")
            plc.set_signal("busy")
            results.append(do_sensor_test(sensor, plc))
            
        else:
            # run pressure / temperature test
            results.append(do_sensor_test(sensor))
        print(results[-1])
        
    if all([r.passed for r in results]):
        # if all sensors working, ignore logger
        loggers_to_ignore.append(results[0].logger) # (ASSUMES ALL TESTED SENSORS ARE FROM THE SAME LOGGER)
    else:
        # if some sensors are working but not all, can't ignore it since it will be retested 
        # (note: if the test constantly returns a partial failure, this will test the logger infinitely)
        
        # if no sensors working, can't ignore it since the logger is unidentified
        # (note: assumption is that the logger will not send any data later)
        pass  

    return results

def do_sensor_test(test_sensor, plc=None):
    """
        (RETESTING LOGIC):
            If all sensors work, the logger continues
            If some sensors work, the faulty ones are replaced until all sensors work
            If no sensors work, the logger is binned
    """
    
    # get all the data for testing
    sample_set = SampleSet(test_sensor)
    sample_set.fetchSamples(loggers_to_ignore, plc)
    
    # if it found multiple potential test loggers, fail test
    if sample_set.conflicting_loggers:
        return TestResult(None, sample_set.sensor, "couldn't_identify_logger")
    
    # if either test or reference loggers had a timeout, or no gyro readings
    if sample_set.timed_out or sample_set.nTestSamples == 0:
        print(f"Timed out - reference logger had {sample_set.nRefSamples} samples, and found {sample_set.nTestSamples} test samples")
        
        # identify which logger timed out and return result
        if sample_set.nTestSamples <= sample_set.required_samples:
            return TestResult(None, sample_set.sensor, "no_test_logger")
        else:
            return TestResult(None, sample_set.sensor, "no_ref_logger")
    
    # test temperature / pressure and return result
    if test_sensor == "temperature" or test_sensor == "pressure":
        if sample_set.testTempPressure():
            return TestResult(sample_set.test_logger, sample_set.sensor, None)
        else:
            return TestResult(sample_set.test_logger, sample_set.sensor, "out_of_threshold")
        
    # test gyro and return result
    if test_sensor == "acceleration":
        gyroResult = sample_set.testGyro()

        if all(gyroResult["detected"]):
            return TestResult(sample_set.test_logger, sample_set.sensor, None)
        else:
            print(f"Test failed with results: {gyroResult['detected']}")
            return TestResult(sample_set.test_logger, sample_set.sensor, "out_of_threshold")
        
class TestResult():
    # store a test result
    def __init__(self, logger, sensor, error):
        self.logger = logger
        self.sensor = sensor
        self.error = error
        if self.error:
            self.passed = False
        else:
            self.passed = True
            
    def __str__(self):
        # print the test result
        return f"Tested {self.sensor} for logger {self.logger} with error {self.error}"
    
if __name__ == "__main__":
    # this only executes if you run this code on its own
    # (used for testing)
    do_logger_test()
    do_logger_test()
    do_logger_test()