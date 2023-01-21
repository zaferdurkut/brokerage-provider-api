from typing import Any

from kafka.errors import KafkaError
from opentracing_instrumentation import get_current_span

from src.core.model.order.order_event_input_model import CreateOrderInputModel
from src.infra.adapter.producer.producer_config import initialize_order_producer
from src.infra.config.app_config import KAFKA_ORDER_TOPIC
from src.infra.config.logging_config import get_logger
from src.infra.config.open_tracing_config import tracer
from src.infra.exception.infra_exception import InfraException

logger = get_logger()


class OrderEventProducer:
    def __init__(self):
        self.kafka_order_producer = initialize_order_producer()
        self.order_topic = KAFKA_ORDER_TOPIC

    def create_order_event(self, order_event_input_model: CreateOrderInputModel):
        with tracer.start_active_span(
            "OrderEventProducer-search",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "order_event_input_model",
                order_event_input_model,
            )
            self._send(topic=self.order_topic, item=order_event_input_model.dict())

    def _send(self, topic: str, item: dict):
        """Connect to Kafka and  push message to Topic"""
        self.kafka_order_producer.send(topic=topic, value=item).add_callback(
            OrderEventProducer.on_send_success
        ).add_errback(OrderEventProducer.on_send_error)

    @staticmethod
    def on_send_success(record):
        logger.info(f"Topic: {str(record.topic)}, Partition: {record.partition}")

    @staticmethod
    def on_send_error(exc):
        logger.error(str(exc))
        raise InfraException(error_code=2002, error_detail=exc)
