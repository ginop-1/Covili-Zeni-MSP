from .MQTTListener import MQTTListener
from .SerialReader import SerialReader
from threading import Thread
import json


def run(config_file: str = "config.json"):
    # load config file
    with open(config_file, "r") as f:
        config = json.load(f)["MQTT"]

    mqtt_listener = MQTTListener("mqtt", config["topic"], config["broker"])
    serial_reader = SerialReader("serial", config["topic"], config["broker"])
    listener_thread = Thread(target=mqtt_listener.run)
    serial_thread = Thread(target=serial_reader.run)
    try:
        listener_thread.start()
        serial_thread.start()
    finally:
        listener_thread.join()
        serial_thread.join()
