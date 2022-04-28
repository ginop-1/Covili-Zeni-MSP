from msp_reader import DBManager
from random import randint

if __name__ == "__main__":
    client = DBManager.InfluxClient()
    client.write_record(randint(0, 100))
