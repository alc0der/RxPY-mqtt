# Code idea taken from: https://github.com/jbarbadillo/reactivemqtt/blob/master/reactivemqtt/object_receiver.py
# MqttDocs: https://pypi.org/project/paho-mqtt
# Contributors:
#    Ahmad Akilan - initial library

from rx.subject import Subject
from os import environ
import paho.mqtt.client as mqtt
from time import sleep

class MqttSubject(Subject):
    def __init__(self, name, opponent_name):
        super().__init__()
        self.name = name
        self.opponent_name = opponent_name
        self.client = mqtt.Client(name)
        self.client.on_connect = lambda client, userdat, flags, rc: client.subscribe(self.name, qos=1)
        self.client.message_callback_add(self.name, lambda client, userdata, msg: self.send(self.__receive_reply__(msg.payload.decode("utf-8"))))
        self.client.connect(environ.get("MQTT_SERVICE", "localhost"))
        self.client.loop_start()

    def __receive_reply__(self, msg):
        sleep(1)
        print("player {} received {}".format(self.name, msg))
        if(msg=="PING"):
            return "PONG"
        elif(msg=="PONG"):
            return "PING"

    def send(self, msg):
        print("player {} sending {}".format(self.name, msg))
        self.client.publish(self.opponent_name, msg, qos=0, retain=False)

    def dispose(self):
        print("stopping {}".format(self.name))
        self.client.loop_stop()
        self.client.disconnect()

p1 = MqttSubject("player1", "player2")
p2 = MqttSubject("player2", "player1")

p1.send(msg='PING')

rx1 = p1.subscribe(on_next=lambda msg: print("p1 received: {}".format(msg)))
rx2 = p2.subscribe(on_next=lambda msg: print("p2 received: {}".format(msg)))

sleep(10)

p1.dispose()
p2.dispose()