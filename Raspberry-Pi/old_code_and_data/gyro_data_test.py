import csv

def read_csv_data(file_path):
    # Initialize lists to hold column data
    time = []
    temperature = []
    pressure = []
    acceleration_x = []
    acceleration_y = []
    acceleration_z = []

    # Open the CSV file
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        # Iterate over each row and extract column data
        for row in csv_reader:
            time.append(row['time'])
            temperature.append(row['temperature'])
            pressure.append(row['pressure'])
            acceleration_x.append(row['acceleration_x'])
            acceleration_y.append(row['acceleration_y'])
            acceleration_z.append(row['acceleration_z'])

    return time, temperature, pressure, acceleration_x, acceleration_y, acceleration_z

def find_threshold(data, factor=3):
    threshold = 0
    for i in range(50):
        if float(data[i]) > threshold:
            threshold = float(data[i])
    
    # Subtract the threshold from all data points
    for j in range(len(data)):
        data[j] = float(data[j]) - threshold
    
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
            if abs(float(data[i])) > threshold:
                group.append(float(data[i]))
                start = i
        elif len(group) >= min_group_size:
            break
        else:
            group.append(float(data[i]))

    if end == 0:
        end = i

    return group, start, end

def acceleration_sensor_test(acceleration_x, acceleration_y, acceleration_z):
    # Find the thresholds for x and y acceleration
    threshold_x = find_threshold(acceleration_x)
    threshold_y = find_threshold(acceleration_y)
    min_group_size = 100

    x_detection, x_acceleration, y_detection, y_acceleration = False, 0, False, 0

    # Find groups of data in x and y acceleration
    x_group, x_start, x_end = find_group(acceleration_x, threshold_x, min_group_size)
    y_group, y_start, y_end = find_group(acceleration_y, threshold_y, min_group_size)

    x_group_2, x_start_2, x_end_2 = find_group(acceleration_x[x_end:], threshold_x, min_group_size)
    y_group_2, y_start_2, y_end_2 = find_group(acceleration_y[y_end:], threshold_y, min_group_size)

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

    return x_detection, x_acceleration, y_detection, y_acceleration, z_detection, z_acceleration


time, temperature, pressure, acceleration_x, acceleration_y, acceleration_z = read_csv_data('logger 98.csv')

# Call the sensor analysis function
x_detection, x_acceleration, y_detection, y_acceleration, z_detection, z_acceleration = acceleration_sensor_test(
    acceleration_x, acceleration_y, acceleration_z
)

print("X Detection:", x_detection)
print("X Acceleration:", x_acceleration)
print("Y Detection:", y_detection)
print("Y Acceleration:", y_acceleration)
print("Z Detection:", z_detection)
print("Z Acceleration:", z_acceleration)
