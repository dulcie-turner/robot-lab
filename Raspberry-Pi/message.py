# Import the JSON library
import json

# Define a class called 'topic_msg'
class topic_msg:
    def __init__(self):
        self.temperatures=[]
        self.accelerations = []
        self.pressures = []
        self.number = 0

    # Method to decode a JSON message and update the 'topic_msg' object
    def decode(self,inputs=None):  
        # If 'inputs' is provided as bytes, decode it to a string     
        inputs=inputs.decode()

        # Parse the JSON message from the string
        json_message=json.loads(inputs)
        
        # final item in list is logger number
        self.number = json_message[-1]
        sensor_data = json_message[0:-1] 

        # Update the 'temperature' attribute with the value from the JSON message
        self.temperatures=[i['t'] for i in sensor_data]
        self.pressures=[i['p'] for i in sensor_data]
        self.accelerations=[i['a'] for i in sensor_data]
