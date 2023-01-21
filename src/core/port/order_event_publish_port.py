from typing import Protocol, Any

from src.core.model.order.order_event_input_model import CreateOrderInputModel


class OrderEventPublishPort(Protocol):
    def create_order_event(self, order_event_input_model: CreateOrderInputModel):
        ...
