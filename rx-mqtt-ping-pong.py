# Code idea taken from: https://github.com/jbarbadillo/reactivemqtt/blob/master/reactivemqtt/object_receiver.py
# MqttDocs: https://pypi.org/project/paho-mqtt
# Contributors:
#    Ahmad Akilan - initial library

from rx.subject import Subject
from os import environ
import paho.mqtt.client as mqtt
from time import sleep

class PingPongSubject(Subject):
    def __init__(self, name, opponent_name):
        # Run the super class constructor
        super().__init__()
        # Set player and opponent names, which will servce as topics
        self.name = name
        self.opponent_name = opponent_name
        # Set this player's topic. This is where he will receive
        self.client = mqtt.Client(name)
        # Pass subscribe as a callback to on_connect
        self.client.on_connect = lambda client, userdat, flags, rc: client.subscribe(self.name, qos=1)
        # Add callback receiver which will return PING or PONG and send the returned value to the opponent who will do the same
        self.client.message_callback_add(self.name, lambda client, userdata, msg: self.send(self.__receive_reply__(msg.payload.decode("utf-8"))))
        # Establish connection
        self.client.connect(environ.get("MQTT_SERVICE", "localhost"))
        # Start the client
        self.client.loop_start()

    def __receive_reply__(self, msg):
        sleep(1)
        print("player {} received {}".format(self.name, msg))
        if(msg=="PING"):
            return "PONG"
        elif(msg=="PONG"):
            return "PING"

    def send(self, msg):
        """
        Publishes message (PING or PONG) to the opponenet topic
        """
        print("player {} sending {}".format(self.name, msg))
        self.client.publish(self.opponent_name, msg, qos=0, retain=False)

    def dispose(self):
        print("stopping {}".format(self.name))
        self.client.loop_stop()
        self.client.disconnect()

# Set up players
p1 = PingPongSubject("player1", "player2")
p2 = PingPongSubject("player2", "player1")

# start the game
p1.send(msg='PING')

rx1 = p1.subscribe(on_next=lambda msg: print("p1 received: {}".format(msg)))
rx2 = p2.subscribe(on_next=lambda msg: print("p2 received: {}".format(msg)))

# Let them play for 10 seconds
sleep(10)

# times up
p1.dispose()
p2.dispose()