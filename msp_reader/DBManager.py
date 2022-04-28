from influxdb_client import InfluxDBClient
import json
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxClient(InfluxDBClient):
    def __init__(self, config_file : str = "config.json", **kwargs):
        with open(config_file, "r") as f:
            self.config = json.load(f)

        super().__init__(
            self.config["url"], self.config["token"], self.config["org"], **kwargs
        )

    def write_record(self, temperature: float):
        write_api = self.write_api(write_options=SYNCHRONOUS)

        write_api.write(
            self.config["bucket"],
            self.config["org"],
            [
                {
                    "measurement": "temperatures",
                    "tags": {
                        "device": "MSP430",
                        "group": 5,
                    },
                    "fields": {
                        "temp": temperature,
                    },
                }
            ],
        )
