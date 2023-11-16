# Fetches the latest data point

"""
SAMPLE DATA STRUCTURE:
    point = {
        "logger": 2,
        "temperature": 25,
        "pressure": 1000,
        "acceleration": [9.8, 0, 0],
        "timestamp": 99999
    }
"""
from communication import *
from message import *
from datetime import datetime

# Initialize a communication instance
com=Communication() 
topic0=topic_msg()

def data_point_present():
    # is there a new data point present?
    return com.update_topic

def get_data_point():
    com.update_topic= False
    topic0.decode(com.msg_topic)
    timestamp = int(datetime.utcnow().timestamp())

    return {
        "logger": topic0.number,
        "temperature": topic0.temperature,
        "pressure": topic0.pressure,
        "acceleration": topic0.acceleration,
        "timestamp": timestamp
    }
