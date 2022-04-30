import paho.mqtt.client as mqtt
from serial import Serial
from time import sleep
from threading import Thread


class SerialReader(mqtt.Client):
    def __init__(self, id: str, topic: str, broker: str) -> None:
        self.topic = topic
        self.broker = broker
        super().__init__(id)

    def log(self, msg: str):
        print(f"{self.__class__.__name__}: {msg}")

    def on_connect(self, client, userdata, flags, rc):
        self.log(mqtt.connack_string(rc))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.log(f"subscribed {self.topic} with QoS: {granted_qos[0]}\n")

    def on_message(self, client, userdata, msg):
        self.log(msg.payload.decode("utf-8"))

    def connect_serial(self):
        self.serial = Serial("/dev/ttyACM1", 9600)

    def main_loop(self):
        while True:
            sleep(120)  # wait 2 minutes
            self.log("Sending message...")
            self.serial.write("S".encode("ascii"))
            while self.serial.inWaiting() <= 0:
                sleep(0.5)
            # serial output is in format: "t1,t2..." ex: "28.5,26.7,25.9..."
            temp = (
                self.serial.read(self.serial.inWaiting())
                .decode("ascii")
                .split(",")
            )
            temp = temp[-2]  # get the last measurement

            if len(temp) >= 5:
                print("no")

            self.serial.write("A".encode("ascii"))

            # self.serial.write(b"B")
            try:
                self.publish(self.topic, temp)
            except UnboundLocalError:
                pass

    def run(self):
        self.connect_serial()
        self.connect(self.broker)
        # create a thread for sending messages
        self.send_thread = Thread(target=self.main_loop)
        self.send_thread.start()

        try:
            self.loop_forever()
        except KeyboardInterrupt:
            self.log("\nExiting...")
        finally:
            self.serial.close()
            self.disconnect()


if __name__ == "__main__":
    serial_reader = SerialReader(
        "SERIAL_LISTENER", "4F/temperature/group5", "mqtt.ssh.edu.it"
    )
    serial_reader.run()
