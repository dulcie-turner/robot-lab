#Import necessary libraries and modules
import requests
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

#Send an HTTP POST request to write data to InfluxDB
data = 0
while True:
    data=data+1
    timestamp = int(datetime.utcnow().timestamp())
    measurement = "temperature"

    data_point = f"{measurement} value={data} {timestamp}"
    response = requests.post(write_url, params=dict(db=db_name, precision="s"), data=data_point)
                          
    if response.status_code == 204:
        print("Data written successfully.")
    else:
        print(f"Failed to write data: {response.text}")
        exit(1)