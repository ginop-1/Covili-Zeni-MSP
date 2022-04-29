from .MQTTListener import MQTTListener
from .SerialReader import SerialReader
from threading import Thread
import json


class Runner:
    @staticmethod
    def run(config_file: str = "config.json"):
        # load config file
        with open(config_file, "r") as f:
            config = json.load(f)["MQTT"]

        mqtt_listener = MQTTListener("mqtt", config["topic"], config["broker"])
        serial_reader = SerialReader(
            "serial", config["topic"], config["broker"]
        )
        listener_thread = Thread(target=mqtt_listener.run)
        listener_thread.start()
        serial_thread = Thread(target=serial_reader.run)
        serial_thread.start()
