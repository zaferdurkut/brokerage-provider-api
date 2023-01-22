from typing import Protocol

from src.core.model.order.order_event_model import OrderEventModel


class OrderEventPublishPort(Protocol):
    def create_order_event(self, order_event_model: OrderEventModel):
        ...
