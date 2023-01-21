import kafka
from kafka.errors import NoBrokersAvailable

from src.infra.config.app_config import (
    KAFKA_ORDER_TOPIC,
    KAFKA_SERVERS,
    KAFKA_NOTIFICATION_TOPIC,
)
from src.infra.config.logging_config import get_logger
from src.infra.exception.infra_exception import InfraException

logger = get_logger()


def initialize_order_consumer():
    try:
        return kafka.KafkaConsumer(
            KAFKA_ORDER_TOPIC,
            bootstrap_servers=KAFKA_SERVERS,
        )
    except NoBrokersAvailable as exc:
        logger.critical(str(exc))
        raise InfraException(error_code=2000)
    except Exception as exc:
        logger.critical(str(exc))
        raise InfraException(error_code=2001)


def initialize_notification_consumer():
    try:
        return kafka.KafkaConsumer(
            KAFKA_NOTIFICATION_TOPIC,
            bootstrap_servers=KAFKA_SERVERS,
        )
    except NoBrokersAvailable as exc:
        logger.critical(str(exc))
        raise InfraException(error_code=2000)
    except Exception as exc:
        logger.critical(str(exc))
        raise InfraException(error_code=2001)
