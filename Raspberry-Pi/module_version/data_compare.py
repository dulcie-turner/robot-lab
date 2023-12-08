from data_fetcher import *
from time import sleep
from statistics import mean
from csv_write import *

# percentage thresholds
thresholds = {
    "temperature": 20,
    "pressure": 0.2
}

# store and test the samples
class SampleSet():
    # define testing constants
    reference_logger = 12 # with sensor 4s in it!
    required_samples = 80
    program_delay = 0.005
    timeout_duration = 20 / program_delay
    
    def __init__(self, sensor):
        self.sensor = sensor
        
        self.samples = []
        self.test_logger = None
        self.nTestSamples = 0
        self.nRefSamples = 0
        
        self.timeout = 0
        self.timed_out = False
        
        self.conflicting_loggers = False
        
    def fetchSamples(self, loggers_to_ignore, plc=None):
        # get all the samples needed for a test
        print(f"Getting {self.sensor} samples, to compare to logger {self.reference_logger}")
        
        if self.sensor == "acceleration":
            acc_csv = CSVFile("acc.csv", ["time", "acc_x", "acc_y", "acc_z"])
            while plc.get_signal() == "shaking":
                if packet_present():
                    points = get_data_points()
                    
                    if points:
                        # if this isn't a logger to ignore
                        if not points[0]["logger"] in loggers_to_ignore:
                            # save each point in the packet
                            for point in points:
                                self.saveSample(point, acc_csv)
                                
                sleep(self.program_delay)
                
            acc_csv.close()
        else:
            # repeat until you've got enough of both data points, or there has been a timeout
            while (self.nTestSamples <= self.required_samples or self.nRefSamples <= self.required_samples) and self.timeout < self.timeout_duration:
                if packet_present():
                    points = get_data_points()
                    
                    if points:
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
                
    def saveSample(self, reading, csv=None):
        # save each sample in the appropriate place in the samples list
        # if self.sensor == "acceleration":
        #    print(reading[self.sensor])
            
        # if not a blank or invalid reading
        if (reading[self.sensor] != 0) and not (self.sensor == "acceleration" and len(reading[self.sensor]) != 3):
            # (since the timestamps are in milliseconds, assume no reading has the same timestamp)
            
            if reading["logger"] == self.reference_logger:
                # if it is from the ref logger, save it
                if self.sensor != "acceleration": # gyro does not use a live reference
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
                    
                    if self.sensor == "acceleration":
                        csv.writeAcc(reading["timestamp"], reading[self.sensor])
                else:
                    # if the data isn't coming from the test logger
                    # this means there are multiple loggers that could potentially be the test logger
                    # error!
                    self.conflicting_loggers = True
                    
    def testTempPressure(self):
        # if the average reading is within the threshold
        if self.getAverageDifference() <= thresholds[self.sensor]:
            print(f"Sensor met threshold of {thresholds[self.sensor]}%\n")
            return True
        else:
            # if it is not within the threshold
            print(f"Sensor failed threshold of {thresholds[self.sensor]}%\n")
            return False
        
    def testGyro(self):
        acceleration = [i.test for i in self.samples if i.test != None]
        
        acceleration_x = [i[0] for i in acceleration]
        acceleration_y = [i[1] for i in acceleration]
        acceleration_z = [i[2] for i in acceleration]
        
        # Find the thresholds for x and y acceleration
        threshold_x = find_threshold(acceleration_x)
        threshold_y = find_threshold(acceleration_y)
        min_group_size = 100

        x_detection, x_acceleration, y_detection, y_acceleration = False, 0, False, 0

        # Find groups of data in x and y acceleration
        x_group, x_start, x_end = find_group(acceleration_x, threshold_x, min_group_size)
        y_group, y_start, y_end = find_group(acceleration_y, threshold_y, min_group_size)

        if x_start < y_start:
            y_start, y_end = x_start, x_end
            y_group, y_start, y_end = find_group(acceleration_y[x_start:], 0, min_group_size)
            y_start, y_end = y_start+x_start-1, y_end+x_start-1
        else:
            x_start, x_end = y_start, y_end
            x_group, x_start, x_end = find_group(acceleration_x[y_start:], 0, min_group_size)
            x_start, x_end = x_start+y_start-1, x_end+y_start-1

        x_group_2, x_start_2, x_end_2 = find_group(acceleration_x[x_end:], threshold_x, min_group_size)
        y_group_2, y_start_2, y_end_2 = find_group(acceleration_y[y_end:], threshold_y, min_group_size)
        x_start_2, x_end_2 = x_start_2+x_end, x_end_2+x_end
        y_start_2, y_end_2 = y_start_2+y_end, y_end_2+y_end

        if x_start_2 < y_start_2:
            y_start_2, y_end_2 = x_start_2, x_end_2
            y_group_2, y_start_2, y_end_2 = find_group(acceleration_y[y_start_2:], 0, min_group_size)
            y_start_2, y_end_2 = y_start_2+x_start_2-1, y_end+x_start_2-1
        else:
            x_start_2, x_end_2 = y_start_2, y_end_2
            x_group_2, x_start_2, x_end_2 = find_group(acceleration_x[y_start_2:], 0, min_group_size)
            x_start_2, x_end_2 = x_start_2+y_start_2-1, x_end+y_start_2-1
    
        if x_group != [] and x_group_2!= []:
            x_group = x_group_2
            # Analyze x acceleration data
            if x_group:
                x_group.sort()
                if abs(x_group[2]) > threshold_x or x_group[-2] > threshold_x:
                    if x_group[-1] > threshold_x * 1.5 and x_group[-1] < 5 * x_group[-2]:
                        x_detection = True
                        x_acceleration = round(x_group[-1], 3)
                    if abs(x_group[0]) > threshold_x * 1.5 and abs(x_group[-1]) < 5 * abs(x_group[-2]):
                        x_detection = True
                        x_acceleration = round(max(x_group[-1], abs(x_group[0])), 3)

        if y_group != [] and y_group_2!= []:
            # Analyze y acceleration data
            if y_group:
                y_group.sort()
                if abs(y_group[2]) > threshold_y or y_group[-2] > threshold_y:
                    if y_group[-1] > threshold_y * 1.5 and y_group[-1] < 5 * y_group[-2]:
                        y_detection = True
                        y_acceleration = round(y_group[-1], 3)
                    if abs(y_group[0]) > threshold_y * 1.5 and abs(y_group[-1]) < 5 * abs(y_group[-2]):
                        y_detection = True
                        y_acceleration = round(max(y_group[-1], abs(y_group[0])), 3)

        # Calculate z acceleration
        z_detection, z_acceleration = calculate_z_acceleration(acceleration_z)

        return {
            "detected": [x_detection, y_detection, z_detection],
            "acceleration": [x_acceleration, y_acceleration, z_acceleration]
        }
                    
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
    
# GYRO TESTING HELPER FUNCTIONS
    
def find_threshold(data, factor=2):
    up = 0
    down = 100
    for i in range(50):
        if abs(float(data[i])) > abs(up):
            up = float(data[i])
    for i in range(50):
        if abs(float(data[i])) < abs(down):
            down = float(data[i])
    
    threshold = (abs(up) - abs(down))/2

    # Subtract the threshold from all data points
    for j in range(len(data)):
        data[j] = float(data[j]) - ((up+down)/2)
    
    # Calculate the threshold multiplied by a factor
    threshold = round(threshold * factor, 3)
    return threshold
    

def calculate_z_acceleration(acceleration_z):
    # Calculate the average acceleration_z in the first 100 data points
    acceleration_z = [float(val) for val in acceleration_z]
    z_acceleration = round(sum(acceleration_z[:100]) / len(acceleration_z[:100]), 3)
    
    # Check if z_acceleration falls within a specific range
    z_detection = 9 < z_acceleration < 10
    return z_detection, z_acceleration

def find_group(data, threshold, min_group_size):
    group = []
    start = 0
    end = 0

    for i in range(len(data)):
        if start == 0:
            if abs(float(data[i])) > abs(threshold):
                group.append(float(data[i]))
                start = i
        elif len(group) >= min_group_size:
            break
        else:
            group.append(float(data[i]))
    if len(data) < min_group_size:
        for j in range(min_group_size-len(data)):
            group.append(0)
    if end == 0:
        end = i

    return group, start, end
            