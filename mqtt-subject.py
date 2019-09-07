# Inspired by: https://github.com/jbarbadillo/reactivemqtt/blob/master/reactivemqtt/object_receiver.py
#
# Contributors:
#    Ahmad Akilan

from rx.subject import Subject
from os import environ
import paho.mqtt.client as mqtt

class EchoSubject(Subject):
    def __init__(self, name=''):
        # Run the super class constructor
        super().__init__()
        # Make topic property
        self.topic = 'echo'
        # Make an MQTT client
        self.client = mqtt.Client('EchoClient')
        # Pass subscribe as a callback to on_connect
        self.client.on_connect = lambda client, userdat, flags, rc: client.subscribe(self.topic, qos=1)
        # Add the subject on_next as the callback of mqtt on_message and pass to it the payload
        self.client.message_callback_add(topic, lambda client, userdata, msg: self.on_next(msg.payload.decode("utf-8")))
        # Establish connection
        self.client.connect(environ.get("MQTT_SERVICE","localhost"))
        # Start the client
        self.client.loop_start()

    def send(self, msg):
        """
        Publishes message to the MQTT topic
        """
        print("sending msg: {}".format(msg))
        self.client.publish(self.topic, msg, qos=0, retain=False)

    def dispose(self):
        print("stopping mqtt")
        self.client.loop_stop()
        self.client.disconnect()

# Create echo client
s = EchoSubject()
# Subscribe print to the subject
s.subscribe(on_next=lambda msg: print("received msg: {}".format(msg)))


print("type a message to send:")
s.send(msg=input())

# some blocking code to delay disposal and exit
print("press any key to exit")
input()

s.dispose()

