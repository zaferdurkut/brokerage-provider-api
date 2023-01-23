from opentracing_instrumentation import get_current_span

from src.core.model.base_models.order_type import OrderTypeEnum
from src.core.model.order.buy_order_input_model import BuyOrderInputModel
from src.core.model.order.cancel_order_input_model import CancelOrderInputModel
from src.core.model.order.order_event_model import OrderEventModel
from src.core.model.order.sell_order_input_model import SellOrderInputModel
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
            # TODO: Add user control from database or redis
            # TODO: Add stock control from database or redis
            self.order_event_publish_port.create_order_event(
                order_event_model=OrderEventModel(
                    **buy_order_input_model.dict(), type=OrderTypeEnum.BUY
                )
            )

    def sell_order(self, sell_order_input_model: SellOrderInputModel):
        with tracer.start_active_span(
            "OrderService-sell_order",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "sell_order_input_model",
                sell_order_input_model,
            )
            # TODO: Add user control from database or redis
            # TODO: Add stock control from database or redis
            self.order_event_publish_port.create_order_event(
                order_event_model=OrderEventModel(
                    **sell_order_input_model.dict(), type=OrderTypeEnum.SELL
                )
            )

    def cancel_order(self, cancel_order_input_model: CancelOrderInputModel):
        with tracer.start_active_span(
            "OrderService-cancel_order",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "cancel_order_input_model",
                cancel_order_input_model,
            )
            # TODO: Add order control from database or redis
            # TODO: Add stock control from database or redis
            self.order_event_publish_port.create_order_event(
                order_event_model=OrderEventModel(
                    **cancel_order_input_model.dict(), type=OrderTypeEnum.CANCEL
                )
            )
