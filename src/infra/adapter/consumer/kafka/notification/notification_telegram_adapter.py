from uuid import UUID

import requests

from src.core.model.base_models.order_type import OrderTypeEnum
from src.core.model.notification.notification_event_model import NotificationEventModel
from src.core.model.user.get_user_output_model import GetUserOrderOutputModel
from src.infra.config.app_config import (
    NOTIFICATION_TELEGRAM_CHAT_ID,
    NOTIFICATION_TELEGRAM_BOT_TOKEN,
)
from src.infra.config.logging_config import get_logger
from src.infra.exception.infra_exception import InfraException
from src.infra.util.constants import SEND_TELEGRAM_MESSAGE_API_URL

logger = get_logger()


class NotificationTelegramAdapter:
    def __init__(self):
        self.chat_id = NOTIFICATION_TELEGRAM_CHAT_ID

    def send_success_notification(
        self, notification_event_model: NotificationEventModel
    ):
        order_details: GetUserOrderOutputModel = self._get_order_details(
            notification_event_model=notification_event_model,
            order_id=notification_event_model.order_id,
        )
        if order_details.type != OrderTypeEnum.CANCEL:
            message = f"Dear {notification_event_model.user.name}, \n Your {order_details.type.value} order has been successfully created with id {notification_event_model.order_id}"
        else:
            message = f"Dear {notification_event_model.user.name}, \n Your {order_details.type.value} order has been successfully cancelled with id {notification_event_model.order_id}"

        return self._send_to_telegram(message)

    def send_error_notification(self, notification_event_model: NotificationEventModel):
        if notification_event_model.error.is_system_error is False:
            order_details = self._get_order_details(
                notification_event_model=notification_event_model,
                order_id=notification_event_model.order_id,
            )
            if order_details.type != OrderTypeEnum.CANCEL:
                message = f"Dear {notification_event_model.user.name}, \n An error was encountered while creating Your {order_details.type.value} order with id {notification_event_model.order_id}. Error reason: {notification_event_model.error.error_message}"
            else:
                message = f"Dear {notification_event_model.user.name}, \n Your {order_details.type.value} order has not been cancelled with id {notification_event_model.order_id} Error reason: {notification_event_model.error.error_message}"
            return self._send_to_telegram(message)

    def _get_order_details(
        self, notification_event_model: NotificationEventModel, order_id: UUID
    ) -> GetUserOrderOutputModel:
        for order_item in notification_event_model.user.orders:
            if order_id == order_item.id:
                return order_item

    def _send_to_telegram(self, message):

        try:
            requests.post(
                SEND_TELEGRAM_MESSAGE_API_URL.format(
                    API_TOKEN=NOTIFICATION_TELEGRAM_BOT_TOKEN
                ),
                json={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "Markdown",
                },
            )
        except Exception as exc:
            logger.error(exc)
            raise InfraException(2016)
