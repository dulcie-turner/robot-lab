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

reference_logger = 12
reference_interval = 5 # n readings at 1 second per reading
timeout_duration = 15 # seconds before timeout
program_delay = 0.1 # delay while checking for readings

# percentage thresholds
thresholds = {
    "temperature": 1.5,
    "pressure": 1
}

# store the signals to ignore for each logger
signals_to_ignore = [0] + [{"temperature": False, "pressure": False} for i in range(1, 13)]

# store the readings
class Reading():
    def __init__(self, timestamp, test=None, ref=None):
        self.timestamp = timestamp
        self.test = test
        self.ref = ref

def test_logger(test_sensor):
    """
        WHAT THIS DOES:
            Gets all the data for a specific sensor type (for the loggers that aren't being ignored)
            If there is data from a single logger, this is the logger to be tested
            If there is no data, the sensor / logger isn't working
            If there is data for multiple loggers, error!
    """
    test_samples = 0
    ref_samples = 0
    timeout = 0

    samples = []
    test_logger = None
    
    print(f"Getting {reference_interval} {test_sensor} samples, to compare to logger {reference_logger}")
    
    # repeat until you've got enough of both data points, or there has been a timeout
    while (test_samples <= reference_interval or ref_samples <= reference_interval) and (timeout * program_delay) < timeout_duration:
        if data_point_present():
            point = get_data_point()
            
            # if this isn't a sensor to ignore, and the data point isn't blank
            if (not signals_to_ignore[point['logger']][test_sensor]) and point[test_sensor] != 0:
                # see if there is already data at that timestamp
                existing = next((x for x in samples if x.timestamp == point["timestamp"]), None)
            
                # if the data is coming from the reference logger
                if point["logger"] == reference_logger:
                    # create or update the reference data point
                    if existing:
                        existing.ref = point[test_sensor]
                    else:
                        samples.append(Reading(point["timestamp"],ref=point[test_sensor]))
                    ref_samples += 1
                
                else:
                    # if the test logger hasn't been set yet, make this it
                    if test_logger == None:
                        test_logger = point["logger"]
                        
                    # if the data is coming from the test logger
                    if point["logger"] == test_logger:
                        # create or update the test data point
                        if existing:
                            existing.test = point[test_sensor]
                        else:
                            samples.append(Reading(point["timestamp"],test=point[test_sensor]))
                        test_samples += 1
                        
                    else:
                        # if the data isn't coming from the test logger
                        # this means there are multiple loggers that could potentially be the test logger
                        # error!
                        raise Exception("Multiple untested sensors are sending data at once. Can't identify sensor to test")
                        
        timeout += 1
        sleep(program_delay)
        
    if (timeout * program_delay) >= timeout_duration:
        print(f"Timed out - reference logger had {ref_samples} samples, and found {test_samples} test samples")
        return False
       
    # find the average difference
    average_test_reading = mean([i.test for i in samples if i.test != None])
    average_ref_reading = mean([i.ref for i in samples if i.ref != None])
    percent_difference = 100 * (average_test_reading - average_ref_reading) / average_ref_reading
    
    print(f"Logger tested: {test_logger} , Test average: {average_test_reading:.2f} , Ref average: {average_ref_reading:.2f} , Percentage difference: {(percent_difference):.2f}%")
    
    if percent_difference <= thresholds[test_sensor]:
        print(f"Sensor met threshold of {thresholds[test_sensor]}%\n")

        # mark the sensor as successfully tested
        signals_to_ignore[test_logger][test_sensor] = True
        return True
    else:
        print(f"Sensor failed threshold of {thresholds[test_sensor]}%\n")
        return False

if __name__ == "__main__":
    # this only executes if you run this code on its own
    # (used for testing)
    
    test_logger("temperature")
    test_logger("pressure")