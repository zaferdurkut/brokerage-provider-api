import json

from src.core.model.notification.notification_event_model import NotificationEventModel
from src.infra.adapter.consumer.kafka.consumer_config import (
    initialize_notification_consumer,
)
from src.infra.adapter.consumer.kafka.notification.notification_telegram_adapter import (
    NotificationTelegramAdapter,
)
from src.infra.config.logging_config import get_logger

logger = get_logger()


class NotificationConsumer:
    def __init__(self):
        self.notification_consumer = initialize_notification_consumer()
        self.notification_telegram_adapter = NotificationTelegramAdapter()

    def run(self):
        logger.warning("NotificationConsumer service was started")
        for message in self.notification_consumer:
            data = self._value_deserializer(message.value)
            notification_event_model = NotificationEventModel(**data)
            if notification_event_model.error is None:
                self.notification_telegram_adapter.send_success_notification(
                    notification_event_model=notification_event_model
                )
            else:
                self.notification_telegram_adapter.send_error_notification(
                    notification_event_model=notification_event_model
                )

    def _value_deserializer(self, message_value) -> dict:
        return json.loads(message_value.decode("utf-8"))


NotificationConsumer().run()
