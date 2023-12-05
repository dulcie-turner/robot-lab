"""
WHAT THIS DOES:
    Get a data feed for the relevant two sensors
    For a specified comparison interval, find the average difference
    Compare it to a threshold to decide whether to reject (returning True or False)

    (This only works for pressure and temperature currently)
"""

from data_fetcher import *
from time import sleep
from statistics import mean

# percentage thresholds
thresholds = {
    "temperature": 2,
    "pressure": 1
}
# sensors to test and their order
sensors = ["temperature", "pressure"]

loggers_to_ignore = []

    
def do_logger_test():
    # test each sensor in a logger
    results = []
    for sensor in sensors:
        results.append(do_sensor_test(sensor))   
    if all([r.passed for r in results]):
        # if all sensors working, ignore logger
        loggers_to_ignore.append(results[0].logger) # (ASSUMES ALL TESTED SENSORS ARE FROM THE SAME LOGGER)
    else:
        # if some sensors are working but not all, can't ignore it since it will be retested
        # if no sensors working, can't ignore it (since the logger is unidentified) but will have to assume it doesn't send any data later
        pass  
    return results

def do_sensor_test(test_sensor):
    """
        WHAT THIS DOES:
            Gets all the data for a specific sensor type (for the loggers that aren't being ignored)
            If there is data from a single logger, this is the logger to be tested
            If there is no data, the sensor / logger isn't working
            If there is data for multiple loggers, error!
            
        (RETESTING LOGIC):
            If all sensors work, the logger continues
            If some sensors work, the faulty ones are replaced until all sensors work
            If no sensors work, the logger is binned
    """
    
    # get all the data for testing
    sample_set = SampleSet(test_sensor)
    sample_set.fetchSamples()
    
    # if either test or reference loggers had a timeout
    if sample_set.timed_out:
        print(f"Timed out - reference logger had {sample_set.nRefSamples} samples, and found {sample_set.nTestSamples} test samples")
        # identify which logger timed out and return result
        if sample_set.nTestSamples <= sample_set.required_samples:
            return TestResult(None, sample_set.sensor, "no_test_logger")
        else:
            return TestResult(None, sample_set.sensor, "no_ref_logger")
    
    # if it found multiple potential test loggers
    if sample_set.conflicting_loggers:
        return TestResult(None, sample_set.sensor, "couldn't_identify_logger")
       
    # if the average reading is within the threshold
    if sample_set.getAverageDifference() <= thresholds[sample_set.sensor]:
        print(f"Sensor met threshold of {thresholds[sample_set.sensor]}%\n")
        return TestResult(sample_set.test_logger, sample_set.sensor, None)
    else:
        # if it is not within the threshold
        print(f"Sensor failed threshold of {thresholds[sample_set.sensor]}%\n")
        return TestResult(sample_set.test_logger, sample_set.sensor, "out_of_threshold")

# store and test the samples
class SampleSet():
    # define testing constants
    reference_logger = 12
    required_samples = 5
    program_delay = 0.005
    timeout_duration = 10 / program_delay
    
    def __init__(self, sensor):
        self.sensor = sensor
        
        self.samples = []
        self.test_logger = None
        self.nTestSamples = 0
        self.nRefSamples = 0
        
        self.timeout = 0
        self.timed_out = False
        
        self.conflicting_loggers = False
        
    def fetchSamples(self):
        # get all the samples needed for a test
        print(f"Getting {self.sensor} samples, to compare to logger {self.reference_logger}")
        
        # repeat until you've got enough of both data points, or there has been a timeout
        while (self.nTestSamples <= self.required_samples or self.nRefSamples <= self.required_samples) and self.timeout < self.timeout_duration:
            if packet_present():
                points = get_data_points()
                
                # if this isn't a logger to ignore
                if not points[0]["logger"] in loggers_to_ignore:
                    # save each point in the packet
                    for point in points:
                        self.saveSample(point)
                        
            self.timeout += 1
            sleep(self.program_delay)
        
        # did it time out?
        if self.timeout >= self.timeout_duration:
            self.timed_out = True
                
    def saveSample(self, reading):
        # save each sample in the appropriate place in the samples list
        
        # if not a blank reading
        if reading[self.sensor] != 0:
            # (since the timestamps are in milliseconds, assume no reading has the same timestamp)
            
            if reading["logger"] == self.reference_logger:
                # if it is from the ref logger, save it
                self.samples.append(Sample(reading["timestamp"],ref=reading[self.sensor]))
                self.nRefSamples += 1
            else:
                if self.test_logger == None:
                    # if the test logger hasn't been set yet, make this it
                    self.test_logger = reading["logger"]
                    
                if reading["logger"] == self.test_logger:
                    # if the data is coming from the test logger, save it
                    self.samples.append(Sample(reading["timestamp"], test=reading[self.sensor]))
                    self.nTestSamples += 1
                    
                else:
                    # if the data isn't coming from the test logger
                    # this means there are multiple loggers that could potentially be the test logger
                    # error!
                    self.conflicting_loggers = True
                    
    def getAverageDifference(self):
        # find the average difference (used for temperature and pressure)
        average_test_reading = mean([i.test for i in self.samples if i.test != None])
        average_ref_reading = mean([i.ref for i in self.samples if i.ref != None])
        percent_difference = 100 * (average_test_reading - average_ref_reading) / average_ref_reading
    
        print(f"Logger tested: {self.test_logger} , Test average: {average_test_reading:.2f} , Ref average: {average_ref_reading:.2f} , Percentage difference: {(percent_difference):.2f}%")
        return abs(percent_difference)
    
class Sample():
    # store a single reading
    def __init__(self, timestamp, test=None, ref=None):
        self.timestamp = timestamp
        self.test = test
        self.ref = ref

    def __str__(self):
        # print it nicely
        return f"{self.timestamp} : test {self.test}, ref {self.ref}"
            
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

if __name__ == "__main__":
    # this only executes if you run this code on its own
    # (used for testing)
    do_logger_test()
    do_logger_test()
    do_logger_test()
