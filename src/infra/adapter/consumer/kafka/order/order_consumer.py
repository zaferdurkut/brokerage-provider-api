import json

from src.core.model.base_models.order_type import OrderTypeEnum
from src.core.model.order.buy_order_input_model import BuyOrderInputModel
from src.core.model.order.cancel_order_input_model import CancelOrderInputModel
from src.core.model.order.order_result_output_model import (
    OrderRepositoryResultOutputModel,
)
from src.core.model.order.sell_order_input_model import SellOrderInputModel
from src.infra.adapter.consumer.kafka.consumer_config import initialize_order_consumer
from src.infra.adapter.repository.postgres.order_repository import OrderRepository
from src.infra.config.logging_config import get_logger

logger = get_logger()


class OrderConsumer:
    def __init__(self):
        self.order_consumer = initialize_order_consumer()
        self.order_repository = OrderRepository()

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
            order_result_model: OrderRepositoryResultOutputModel = (
                self.order_repository.buy_order(
                    buy_order_input_model=BuyOrderInputModel(**data)
                )
            )
            print(order_result_model)
        except Exception as exc:
            logger.error(exc)

    def _process_sell_order(self, data):
        try:
            order_result_model: OrderRepositoryResultOutputModel = (
                self.order_repository.sell_order(
                    sell_order_input_model=SellOrderInputModel(**data)
                )
            )
            print(order_result_model)
        except Exception as exc:
            logger.error(exc)

    def _process_cancel_order(self, data):
        try:
            order_result_model: OrderRepositoryResultOutputModel = (
                self.order_repository.cancel_order(
                    cancel_order_input_model=CancelOrderInputModel(**data)
                )
            )
            print(order_result_model)
        except Exception as exc:
            logger.error(exc)

    def _value_deserializer(self, message_value) -> dict:
        return json.loads(message_value.decode("utf-8"))


OrderConsumer().run()
