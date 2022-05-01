import logging
from msp_reader.runner import run

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(module)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    run()
