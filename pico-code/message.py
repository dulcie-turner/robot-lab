# Import the JSON library
import json

# Define a class called 'topic_msg'
class topic_msg:
    def __init__(self):
        # Initialize the 'temperature' attribute to 0
        self.temp=0
        self.press=0
        self.acc=[]

    # Method to encode the 'topic_msg' object as a JSON message
    def encode(self):
        # Create a dictionary with the 'temperature' attribute
        message={'t':round(self.temp,2), 'p':round(self.press,2), 'a': [round(a, 3) for a in self.acc]}
        return message

    # Method to decode a JSON message and update the 'topic_msg' object
    def decode(self,inputs=None):  
        # If 'inputs' is provided as bytes, decode it to a string     
        inputs=inputs.decode()

        # Parse the JSON message from the string
        json_message=json.loads(inputs)

        # Update the 'temperature' attribute with the value from the JSON message
        self.temp=json_message['t']
        self.press=json_message['p']
        self.acc=json_message['a']


