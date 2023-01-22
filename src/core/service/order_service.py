from opentracing_instrumentation import get_current_span

from src.core.model.base_models.order_type import OrderTypeEnum
from src.core.model.order.buy_order_input_model import BuyOrderInputModel
from src.core.model.order.order_event_model import OrderEventModel
from src.core.port.order_event_publish_port import OrderEventPublishPort
from src.infra.config.open_tracing_config import tracer


class OrderService:
    def __init__(
        self,
        order_event_publish_port: OrderEventPublishPort,
    ):
        self.order_event_publish_port = order_event_publish_port

    def buy_order(self, buy_order_input_model: BuyOrderInputModel):
        with tracer.start_active_span(
            "OrderService-buy_order",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "buy_order_input_model",
                buy_order_input_model,
            )
            self.order_event_publish_port.create_order_event(
                order_event_model=OrderEventModel(
                    **buy_order_input_model.dict(), type=OrderTypeEnum.BUY
                )
            )
