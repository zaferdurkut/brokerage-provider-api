import json

from opentracing_instrumentation import get_current_span

from src.core.model.notification.notification_event_model import NotificationEventModel
from src.infra.adapter.producer.producer_config import initialize_notification_producer
from src.infra.config.app_config import KAFKA_NOTIFICATION_TOPIC
from src.infra.config.logging_config import get_logger
from src.infra.config.open_tracing_config import tracer
from src.infra.exception.infra_exception import InfraException

logger = get_logger()


class NotificationEventProducer:
    def __init__(self):
        self.kafka_notification_producer = initialize_notification_producer()
        self.notification_topic = KAFKA_NOTIFICATION_TOPIC

    def create_notification_event(
        self, notification_event_model: NotificationEventModel
    ):
        with tracer.start_active_span(
            "NotificationEventProducer-create_notification_event",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "notification_event_model",
                notification_event_model,
            )
            self._send(
                topic=self.notification_topic,
                item=json.loads(notification_event_model.json()),
            )

    def _send(self, topic: str, item: dict):
        """Connect to Kafka and  push message to Topic"""
        self.kafka_notification_producer.send(topic=topic, value=item).add_callback(
            NotificationEventProducer.on_send_success
        ).add_errback(NotificationEventProducer.on_send_error)

    @staticmethod
    def on_send_success(record):
        logger.info(f"Topic: {str(record.topic)}, Partition: {record.partition}")

    @staticmethod
    def on_send_error(exc):
        logger.error(str(exc))
        raise InfraException(error_code=2015, error_detail=exc)
