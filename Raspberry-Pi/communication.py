# Import necessary libraries
import paho.mqtt.client as mqtt 

# Define a Communication class
class Communication:
    def __init__(self):
        # Create an MQTT client with the specified broker and port
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect('10.247.53.162',1883, keepalive=60)
        # Set the on_connect callback function
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.loop_start()

        #Subscribe to the MQTT topic
        self.mqtt_client.message_callback_add('service/topic', self.on_message_topic)
        self.mqtt_client.subscribe('service/#')
        self.msg_topic=''
        self.update_topic= False

     # Callback function called when the MQTT client successfully connects
    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
        else:
            print("Connection failed")


    #Handle incoming MQTT message on the defined topic 
    def on_message_topic(self, client, userdata, message):
        self.msg_topic = message.payload
        self.update_topic = True

