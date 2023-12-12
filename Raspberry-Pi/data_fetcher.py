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

sampling_interval = 0.015

def packet_present():
    # is there a new data point present?
    return com.update_topic

def get_data_points():
    # get a packet of data and return a list of points
    
    com.update_topic= False
    
    try:
        topic0.decode(com.msg_topic)
        time_of_arrival = int(datetime.utcnow().timestamp() * 1000) # get timestamp of packet arrival in ms

        unsorted_dict = [{
            "logger": topic0.number,
            "temperature": topic0.temperatures[i],
            "pressure": topic0.pressures[i],
            "acceleration": topic0.accelerations[i],
            # each sample must have a unique timestamp, but the timestamps are not sent (due to the Pico's unreliable onboard clock)
            # so the sample times are back-calculated from the time of arrival (this is very approximate!)
            "timestamp": time_of_arrival - (i * sampling_interval)
        } for i in range(len(topic0.temperatures))]
        
        # sort by timestamp
        sorted_dict = sorted(unsorted_dict, key=lambda d: d["timestamp"])
        return sorted_dict
    
    except (json.decoder.JSONDecodeError, UnicodeDecodeError) as e:
         # sometimes packets are invalid and cause errors
         # (think this is packets being too large and not sending correctly)
        print(e)
        return None
