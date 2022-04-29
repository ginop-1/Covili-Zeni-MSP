import paho.mqtt.client as mqtt


class MQTTListener(mqtt.Client):
    def __init__(self, id: str, topic: str, broker: str) -> None:
        self.topic = topic
        self.broker = broker
        super().__init__(id)

    def log(self, msg: str):
        print(f"{self.__class__.__name__}: {msg}")

    def on_connect(self, client, userdata, flags, rc):
        self.log(mqtt.connack_string(rc))
        client.subscribe(self.topic)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.log(f"subscribed {self.topic} with QoS: {granted_qos[0]}\n")

    def on_message(self, client, userdata, msg):
        self.log(msg.payload.decode("utf-8"))

    def run(self):
        self.connect(self.broker)
        try:
            self.loop_forever()
        except KeyboardInterrupt:
            self.log("\nExiting...")
        finally:
            self.disconnect()


if __name__ == "__main__":
    mqtt_listener = MQTTListener(
        "MQTT_LISTENER", "4F/temperature/group5", "mqtt.ssh.edu.it"
    )
    mqtt_listener.run()
