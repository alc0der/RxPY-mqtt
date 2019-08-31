# RxPY-mqtt

A sample project on how to create an RxPY subject around MQTT.

## Running the Code (ping pong sample)

```bash
app=rx-mqtt-ping-pong.py docker-compose up
```

## Running the Code (echo example)

This sample requires stdin, so it requires extra steps.
```bash
# initiating mqtt-broker
docker-compose up -d mqtt-broker
# run the echo app
app=mqtt-subject.py docker-compose run rxpy-mqtt
```