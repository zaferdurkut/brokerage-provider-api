import json

from src.core.model.base_models.order_type import OrderTypeEnum
from src.core.model.notification.notification_event_model import (
    NotificationEventModel,
    NotificationErrorEventModel,
)
from src.core.model.order.buy_order_input_model import BuyOrderInputModel
from src.core.model.order.cancel_order_input_model import CancelOrderInputModel
from src.core.model.order.order_result_output_model import (
    OrderRepositoryResultOutputModel,
)
from src.core.model.order.sell_order_input_model import SellOrderInputModel
from src.core.model.user.get_user_output_model import GetUserOutputModel
from src.infra.adapter.consumer.kafka.consumer_config import initialize_order_consumer
from src.infra.adapter.producer.kafka.notification.notification_producer import (
    NotificationEventProducer,
)
from src.infra.adapter.repository.postgres.order_repository import OrderRepository
from src.infra.adapter.repository.postgres.user_repository import UserRepository
from src.infra.config.logging_config import get_logger
from src.infra.util.errors import SYSYEM_ERROR_CODES, errors

logger = get_logger()


class OrderConsumer:
    def __init__(self):
        self.order_consumer = initialize_order_consumer()
        self.order_repository = OrderRepository()
        self.user_repository = UserRepository()
        self.notification_event_producer = NotificationEventProducer()

    def run(self):
        logger.warning("OrderConsumer service was started")
        for message in self.order_consumer:
            data = self._value_deserializer(message.value)
            if data.get("type", None) == OrderTypeEnum.BUY:
                self._process_buy_order(data=data)
            elif data.get("type", None) == OrderTypeEnum.SELL:
                self._process_sell_order(data=data)
            elif data.get("type", None) == OrderTypeEnum.CANCEL:
                self._process_cancel_order(data=data)

    def _process_buy_order(self, data):
        try:
            buy_order_input_model = BuyOrderInputModel(**data)
            order_result_model: OrderRepositoryResultOutputModel = (
                self.order_repository.buy_order(
                    buy_order_input_model=buy_order_input_model
                )
            )
            user_output_model: GetUserOutputModel = self.user_repository.get_user(
                user_id=buy_order_input_model.user_id
            )
            notification_event_model: NotificationEventModel = (
                self._populate_notification_event_model(
                    order_result_model=order_result_model,
                    user_output_model=user_output_model,
                )
            )
            self.notification_event_producer.create_notification_event(
                notification_event_model=notification_event_model
            )

        except Exception as exc:
            logger.error(exc)

    def _process_sell_order(self, data):
        try:
            sell_order_input_model = SellOrderInputModel(**data)
            order_result_model: OrderRepositoryResultOutputModel = (
                self.order_repository.sell_order(
                    sell_order_input_model=sell_order_input_model
                )
            )
            user_output_model: GetUserOutputModel = self.user_repository.get_user(
                user_id=sell_order_input_model.user_id
            )
            notification_event_model: NotificationEventModel = (
                self._populate_notification_event_model(
                    order_result_model=order_result_model,
                    user_output_model=user_output_model,
                )
            )
            self.notification_event_producer.create_notification_event(
                notification_event_model=notification_event_model
            )

        except Exception as exc:
            logger.error(exc)

    def _process_cancel_order(self, data):
        try:
            cancel_order_input_model = CancelOrderInputModel(**data)
            order_result_model: OrderRepositoryResultOutputModel = (
                self.order_repository.cancel_order(
                    cancel_order_input_model=cancel_order_input_model
                )
            )
            if order_result_model.user_id is not None:
                user_output_model: GetUserOutputModel = self.user_repository.get_user(
                    user_id=order_result_model.user_id
                )
            else:
                user_output_model = None

            notification_event_model: NotificationEventModel = (
                self._populate_notification_event_model(
                    order_result_model=order_result_model,
                    user_output_model=user_output_model,
                )
            )
            self.notification_event_producer.create_notification_event(
                notification_event_model=notification_event_model
            )

        except Exception as exc:
            logger.error(exc)

    def _value_deserializer(self, message_value) -> dict:
        return json.loads(message_value.decode("utf-8"))

    def _populate_notification_event_model(
        self,
        order_result_model: OrderRepositoryResultOutputModel,
        user_output_model: GetUserOutputModel,
    ) -> NotificationEventModel:

        if order_result_model.error_code is None:
            notification_event_model: NotificationEventModel = NotificationEventModel(
                user=user_output_model,
                order_id=order_result_model.order_id,
                status=order_result_model.status,
                error=None,
            )
        else:
            if order_result_model.error_code in SYSYEM_ERROR_CODES:
                notification_event_model: NotificationEventModel = (
                    NotificationEventModel(
                        user=user_output_model,
                        order_id=None,
                        status=order_result_model.status,
                        error=NotificationErrorEventModel(
                            error_code=order_result_model.error_code,
                            error_message=errors.get(
                                order_result_model.error_code, None
                            ),
                            is_system_error=True,
                        ),
                    )
                )
            else:
                notification_event_model: NotificationEventModel = (
                    NotificationEventModel(
                        user=user_output_model,
                        order_id=order_result_model.order_id,
                        status=order_result_model.status,
                        error=NotificationErrorEventModel(
                            error_code=order_result_model.error_code,
                            error_message=errors.get(
                                order_result_model.error_code, None
                            ),
                            is_system_error=False,
                        ),
                    )
                )
        return notification_event_model


OrderConsumer().run()
