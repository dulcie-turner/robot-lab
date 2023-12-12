#Import necessary libraries and modules
from csv_write import *
from data_fetcher import *
from database_write import *

db = Database()
csv = CSVFile()

#Write data to the CSV file
#HTTP POST request to write data to InfluxDB
count=0        
while count<1000:
    if data_point_present():
        point = get_data_point()

        # write to the csv file
        csv.write(point, count)
                
        # write to the database
        db.write_point("Temperature", point["temperature"], point["timestamp"], point["logger"])
        db.write_point("Pressure", point["pressure"], point["timestamp"], point["logger"])
                        
        if point['acceleration'] != []:
            db.write_point("Acceleration_x", point["acceleration"][0], point["timestamp"], point["logger"])
            db.write_point("Acceleration_y", point["acceleration"][1], point["timestamp"], point["logger"])
            db.write_point("Acceleration_z", point["acceleration"][2], point["timestamp"], point["logger"])
                
        count=count+1

csv.close()


