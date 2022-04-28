from influxdb_client import InfluxDBClient
import json
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxClient(InfluxDBClient):
    """Main DB manager class

    ...

    Attributes
    ----------
    config : dict
        Loaded config.json
    Other attributes are inherited from InfluxDBClient

    Methods
    -------
    write_record(temperature: float)
        Writes a record to the DB
    Other methods are inherited from InfluxDBClient

    """

    def __init__(self, config_file: str = "config.json", **kwargs):
        with open(config_file, "r") as f:
            self.config = json.load(f)

        super().__init__(
            url=self.config["url"],
            token=self.config["token"],
            org=self.config["org"],
            **kwargs
        )

    def write_record(self, temperature: float):
        """Writes a record to the DB

        Parameters
        ----------
        temperature : float
            Temperature to write to the DB

        Returns
        -------
        None
        """

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
