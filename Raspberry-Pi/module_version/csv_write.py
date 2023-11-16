import csv

class CSVFile:
    def __init__(self):
        #Open the CSV file and write the header row to the CSV file
        self.csv_write=open('logger.csv', 'w', newline='')
        self.writer = csv.DictWriter(self.csv_write, fieldnames=['number','temperature','pressure','acceleration'])
        self.writer.writeheader()  

    def write(self, point, count):
        self.writer.writerow({'number':count,'temperature':point['temperature'],'pressure':point['pressure'],'acceleration':point['acceleration']})

    def close(self):
        self.csv_write.close()