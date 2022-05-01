from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

import logging
import json
import paho.mqtt.client as mqtt


class MQTTListener(mqtt.Client):
    def __init__(self, id: str, topic: str, broker: str) -> None:
        self.topic = topic
        self.broker = broker

        config = json.load(open("config.json", "r"))["Influx"]
        self.influx_client = InfluxDBClient(
            url=config["url"], token=config["token"], org=config["org"]
        )
        self.default_bucket = config["bucket"]

        super().__init__(id)

    def on_connect(self, client, userdata, flags, rc):
        logging.info(mqtt.connack_string(rc))
        client.subscribe(self.topic)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        logging.info(f"subscribed {self.topic} with QoS: {granted_qos[0]}")

    def on_message(self, client, userdata, msg):
        try:
            temp = float(msg.payload.decode("utf-8"))
        except ValueError:
            logging.info("invalid message")
            return

        logging.info(f"received temperature: {temp}. Writing to DB...")
        self.influx_client.write_api(write_options=SYNCHRONOUS).write(
            self.default_bucket,
            self.influx_client.org,
            [
                {
                    "measurement": "temperatures",
                    "tags": {
                        "device": "MSP430",
                        "group": 5,
                    },
                    "fields": {
                        "temp": temp,
                    },
                }
            ],
        )

    def run(self):
        self.connect(self.broker)
        try:
            self.loop_forever()
        except KeyboardInterrupt:
            logging.info("\nExiting...")
        finally:
            self.loop_stop()
            self.disconnect()


if __name__ == "__main__":
    config = json.load(open("config.json", "r"))["MQTT"]
    mqtt_listener = MQTTListener("LISTENER", config["topic"], config["broker"])
    mqtt_listener.run()
