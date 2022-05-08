from .MQTTListener import MQTTListener
from .SerialReader import SerialReader

import serial.tools.list_ports
from threading import Thread
import json


def run(config_file: str = "config.json"):
    # load config file
    with open(config_file, "r") as f:
        config = json.load(f)["MQTT"]

    ports = serial.tools.list_ports.comports()

    print("Available ports:")
    [print(f"{ix}. {port.device} {port.description}") for ix, port in enumerate(ports)]
    
    port = ports[int(input("Choose port (use index): "))].device


    mqtt_listener = MQTTListener("mqtt", config["topic"], config["broker"])
    serial_reader = SerialReader("serial", config["topic"], config["broker"], port)
    listener_thread = Thread(target=mqtt_listener.run)
    serial_thread = Thread(target=serial_reader.run)
    try:
        listener_thread.start()
        serial_thread.start()
    finally:
        listener_thread.join()
        serial_thread.join()
