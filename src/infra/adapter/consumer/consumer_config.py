import logging

import kafka

from kafka.errors import NoBrokersAvailable

from src.infra.config.app_config import (
    KAFKA_ORDER_TOPIC,
    KAFKA_CONSUMER_GROUP,
    KAFKA_SERVERS,
    KAFKA_NOTIFICATION_TOPIC,
)
from src.infra.exception.infra_exception import InfraException


def initialize_order_consumer_topic():
    try:
        return kafka.KafkaConsumer(
            KAFKA_ORDER_TOPIC,
            group_id=KAFKA_CONSUMER_GROUP,
            bootstrap_servers=KAFKA_SERVERS,
        )
    except NoBrokersAvailable as exc:
        logging.critical(str(exc))
        raise InfraException(error_code=2000)


def initialize_notification_consumer_topic():
    try:
        return kafka.KafkaConsumer(
            KAFKA_NOTIFICATION_TOPIC,
            group_id=KAFKA_CONSUMER_GROUP,
            bootstrap_servers=KAFKA_SERVERS,
        )
    except NoBrokersAvailable as exc:
        logging.critical(str(exc))
        raise InfraException(error_code=2000)
