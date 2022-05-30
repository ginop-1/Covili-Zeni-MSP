import paho.mqtt.client as mqtt
from serial import Serial
from time import sleep
from threading import Thread
import logging


class SerialReader(mqtt.Client):
    def __init__(
        self, id: str, topic: str, broker: str, serial_port: str
    ) -> None:
        self.topic = topic
        self.broker = broker
        self.serial = Serial(serial_port, 9600)
        super().__init__(id)

    def on_connect(self, client, userdata, flags, rc):
        logging.info(mqtt.connack_string(rc))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        logging.info(f"subscribed {self.topic} with QoS: {granted_qos[0]}\n")

    def on_message(self, client, userdata, msg):
        logging.info(msg.payload.decode("utf-8"))

    def main_loop(self):
        while True:
            sleep(120)  # wait 2 minutes
            logging.info("Sending message...")
            self.serial.write("S".encode("ascii"))
            while self.serial.inWaiting() <= 0:
                sleep(0.5)
            temp = self.serial.read(self.serial.inWaiting()).decode("ascii")
            logging.log(logging.INFO, f"Received: {temp}")
            self.publish(self.topic, temp)

    def run(self):
        self.connect(self.broker)
        # create a thread for sending messages
        self.send_thread = Thread(target=self.main_loop)
        self.send_thread.start()

        try:
            self.loop_forever()
        except KeyboardInterrupt:
            logging.info("Exiting...")
        finally:
            self.serial.close()
            self.loop_stop()
            self.disconnect()


if __name__ == "__main__":
    serial_reader = SerialReader(
        "SERIAL_LISTENER", "4F/temperature/group5", "mqtt.ssh.edu.it"
    )
    serial_reader.run()
