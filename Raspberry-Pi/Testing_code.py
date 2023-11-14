#Import necessary libraries and modules
import csv
from communication import *
from message import *
from datetime import datetime

# Creating an instance of topic_msg
msg = topic_msg()

# Setting the temperature
msg.temperature = 25

# Encoding the message
encoded_msg = msg.encode()  # This will be a JSON string like '{"temperature": 25}'

# Decoding the message
msg.decode('{"temperature": 30}')
print(msg.temperature)  # Output: 30


# Creating an instance of Communication
comm = Communication()

# Assume a message is received on 'service/topic'
# The on_message_topic callback is automatically triggered, updating comm.msg_topic and comm.update_topic

# Checking if a new message has been received
if comm.update_topic:
    print("New message:", comm.msg_topic)
    comm.update_topic = False  # Resetting the flag
