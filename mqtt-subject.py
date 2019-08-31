# Inspired by: https://github.com/jbarbadillo/reactivemqtt/blob/master/reactivemqtt/object_receiver.py
#
# Contributors:
#    Ahmad Akilan

from rx.subject import Subject
from os import environ
import paho.mqtt.client as mqtt

class MqttSubject(Subject):
    def __init__(self, topic, name=''):
        super().__init__()
        self.topic = topic
        self.client = mqtt.Client(name)
        self.client.on_connect = lambda client, userdat, flags, rc: client.subscribe(self.topic, qos=1)
        self.client.message_callback_add(topic, lambda client, userdata, msg: self.on_next(msg.payload.decode("utf-8")))
        self.client.connect(environ.get("MQTT_SERVICE","localhost"))
        self.client.loop_start()

    # Ideally the subject is used eiether for sending or receiving.
    # This send method is just for sample simplicity.
    def send(self, msg):
        print("sending msg: {}".format(msg))
        self.client.publish(self.topic, msg, qos=0, retain=False)

    def dispose(self):
        print("stopping mqtt")
        self.client.loop_stop()
        self.client.disconnect()

# name the topic "echo" cause that it is what this sample doing
s = MqttSubject(topic="echo")
s.subscribe(on_next=lambda msg: print("received msg: {}".format(msg)))


print("type a message to send:")
s.send(msg=input())

# some blocking code to delay disposal and exit
print("press any key to exit")
input()

s.dispose()

