#Import necessary libraries and modules
import csv
import requests
from communication import *
from message import *
from datetime import datetime


# Initialize a communication instance
com=Communication() 
topic0=topic_msg()

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
writer = csv.DictWriter(csvfile_w, fieldnames=['number','data'])
writer.writeheader()  

#Write data to the CSV file
#HTTP POST request to write data to InfluxDB
count=0        
while count<5000:
        if com.update_topic==True:
                com.update_topic= False
                topic0.decode(com.msg_topic)
                timestamp = int(datetime.utcnow().timestamp())
                measurement = "temperature"
                data=topic0.temperature
                writer.writerow({'number':count,'data':data})
                data_point = f"{measurement} value={data} {timestamp}"
                response = requests.post(write_url, params=dict(db=db_name, precision="s"), data=data_point)
                                  
                if response.status_code == 204:
                        print("Data written successfully.",'number',count,measurement,'=',data)
                else:
                        print("Fail to write data")
                count=count+1

#Close the CSV file 
csvfile_w.close()


