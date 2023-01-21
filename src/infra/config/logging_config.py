import logging

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

logger = logging.getLogger()


def get_logger():
    return logger
