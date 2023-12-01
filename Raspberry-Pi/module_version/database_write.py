import requests
from datetime import datetime

class Database:
    #Define the InfluxDB database name and the server URL, and query /write endpoints
    db_name = 'mydb'
    influx_url = "http://localhost:8086"
    create_url = f"{influx_url}/query"
    write_url = f"{influx_url}/write"

    def __init__(self):
        #Send an HTTP POST request to create the database
        create_query = f"CREATE DATABASE {self.db_name}"
        response = requests.post(self.create_url, params=dict(q=create_query))

        if response.status_code == 200:
                print(f"Database '{self.db_name}' created successfully.")
        else:
                print(f"Failed to create database '{self.db_name}'.")
                exit(1)

    def write_point(self, measurement, value, logger, timestamp=None, tags=None):
        # send an HTTP POST request to the influxDB with "data_point"
        if timestamp == None:
            timestamp = int(datetime.utcnow().timestamp())
        
        if tags:
            tag_string = ",".join([f"{i}={tags[i]}" for i in tags])
            data_point = f"{measurement},logger={logger},{tag_string} value={value} {timestamp}"
        else:
            data_point = f"{measurement},logger={logger} value={value} {timestamp}"
        response = requests.post(self.write_url, params=dict(db=self.db_name, precision="s"), data=data_point)

        if response.status_code == 204:
            print(f"Data written successfully: {measurement} reading for logger {logger} with a value of {value} and time of {timestamp}")
            return True
        else:
            print(f"Failed to write data: {measurement} reading for logger {logger} with a value of {value}")
            print(f"Code {response.status_code} with text {response.text}")
            
            return False
