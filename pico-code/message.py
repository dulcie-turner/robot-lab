# Import the JSON library
import json

# Define a class called 'topic_msg'
class topic_msg:
    def __init__(self):
        # Initialize the 'temperature' attribute to 0
        self.temperature=0

    # Method to encode the 'topic_msg' object as a JSON message
    def encode(self):
        # Create a dictionary with the 'temperature' attribute
        message={'temperature':self.temperature}
        # Convert the dictionary to a JSON-formatted string
        json_message=json.dumps(message)
        return json_message

    # Method to decode a JSON message and update the 'topic_msg' object
    def decode(self,inputs=None):  
        # If 'inputs' is provided as bytes, decode it to a string     
        inputs=inputs.decode()

        # Parse the JSON message from the string
        json_message=json.loads(inputs)

        # Update the 'temperature' attribute with the value from the JSON message
        self.temperature=json_message['temperature']

