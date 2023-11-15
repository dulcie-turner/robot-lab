#Import necessary libraries and modules
import csv
import requests
from data_fetcher import *
from datetime import datetime


#Define the InfluxDB database name and the server URL, and query /write endpoints
db_name = 'mydb'
influx_url = "http://localhost:8086"
create_url = f"{influx_url}/query"
write_url = f"{influx_url}/write"

#Send an HTTP POST request to create the database
create_query = f"CREATE DATABASE {db_name}"
response = requests.post(create_url, params=dict(q=create_query))

if response.status_code == 200:
        print(f"Database '{db_name}' created successfully.")
else:
        print(f"Failed to create database '{db_name}'.")
        exit(1)

#Open the CSV file and write the header row to the CSV file
csvfile_w=open('logger.csv', 'w', newline='')
writer = csv.DictWriter(csvfile_w, fieldnames=['number','temperature','pressure','acceleration'])
writer.writeheader()  

#Write data to the CSV file
#HTTP POST request to write data to InfluxDB
count=0        
while count<1000:
        if data_point_present():
                point = get_data_point()

                
                # write to the csv file
                writer.writerow({'number':count,'temperature':point['temperature'],'pressure':point['pressure'],'acceleration':point['acceleration']})
                
                # send an HTTP POST request to the influxDB with "data_point"
                data_point = f"Temperature,logger={point['logger']} value={point['temperature']} {point['timestamp']}"
                response = requests.post(write_url, params=dict(db=db_name, precision="s"), data=data_point)
                        
                # send an HTTP POST request to the influxDB with "data_point" - pressure
                data_point = f"Pressure,logger={point['logger']} value={point['pressure']} {point['timestamp']}"
                response = requests.post(write_url, params=dict(db=db_name, precision="s"), data=data_point)
                
                if point['acceleration'] != []:
                        print(point['acceleration'])
                
                        # send an HTTP POST request to the influxDB with "data_point" - accelerationx
                        data_point = f"Acceleration_x,logger={point['logger']} value={point['acceleration'][0]} {point['timestamp']}"
                        response = requests.post(write_url, params=dict(db=db_name, precision="s"), data=data_point)
                        
                        # send an HTTP POST request to the influxDB with "data_point" - accelerationy
                        data_point = f"Acceleration_y,logger={point['logger']} value={point['acceleration'][1]} {point['timestamp']}"
                        response = requests.post(write_url, params=dict(db=db_name, precision="s"), data=data_point)
                        
                        # send an HTTP POST request to the influxDB with "data_point" - accelerationz
                        data_point = f"Acceleration_z,logger={point['logger']} value={point['acceleration'][2]} {point['timestamp']}"
                        response = requests.post(write_url, params=dict(db=db_name, precision="s"), data=data_point)

                                  
                if response.status_code == 204:
                        print("Data written successfully.",'number',count,'logger no',point['logger'], 'Temperature =',point['temperature'],'Pressure =',point['pressure'],'Acceleration =',point['acceleration'])
                else:
                        print("Fail to write data")
                
                count=count+1

#Close the CSV file 
csvfile_w.close()


