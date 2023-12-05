import csv

class CSVFile:
    def __init__(self):
        #Open the CSV file and write the header row to the CSV file
        self.csv_write=open('logger.csv', 'w', newline='')
        self.writer = csv.DictWriter(self.csv_write, fieldnames=['time','temperature','pressure','acceleration_x', 'acceleration_y', 'acceleration_z'])
        self.writer.writeheader()  

    def write(self, point):
        if len(point["acceleration"]) == 3:
            self.writer.writerow({'time': point["timestamp"],'temperature':point['temperature'],'pressure':point['pressure'],'acceleration_x':point['acceleration'][0], 'acceleration_y':point['acceleration'][1], 'acceleration_z':point['acceleration'][2]})

    def close(self):
        self.csv_write.close()