import csv

class CSVFile:
    def __init__(self, filename, fields):
        #Open the CSV file and write the header row to the CSV file
        self.csv_write=open(filename, 'w', newline='')
        self.writer = csv.DictWriter(self.csv_write, fieldnames=fields)
        self.writer.writeheader()  

    def writePoint(self, point):
        # write a single data point
        if len(point["acceleration"]) == 3:
            self.writer.writerow({'time': point["timestamp"],'temperature':point['temperature'],'pressure':point['pressure'],'acceleration_x':point['acceleration'][0], 'acceleration_y':point['acceleration'][1], 'acceleration_z':point['acceleration'][2]})

    def writeAcc(self, time, acc):
        self.writer.writerow({'time': time, 'acc_x': acc[0], 'acc_y': acc[1], 'acc_z': acc[2]})
        
    def close(self):
        self.csv_write.close()