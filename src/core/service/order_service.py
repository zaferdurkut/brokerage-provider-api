from typing import List, Optional
from uuid import UUID

from opentracing_instrumentation import get_current_span

from src.core.model.base_models.order_type import OrderTypeEnum
from src.core.model.order.buy_order_input_model import BuyOrderInputModel
from src.core.model.order.cancel_order_input_model import CancelOrderInputModel
from src.core.model.order.get_order_output_model import GetOrderOutputModel
from src.core.model.order.order_event_model import OrderEventModel
from src.core.model.order.sell_order_input_model import SellOrderInputModel
from src.core.port.order_event_publish_port import OrderEventPublishPort
from src.core.port.order_repository_port import OrderRepositoryPort
from src.core.port.stock_repository_port import StockRepositoryPort
from src.core.port.user_repository_port import UserRepositoryPort
from src.infra.config.open_tracing_config import tracer


class OrderService:
    def __init__(
        self,
        order_event_publish_port: OrderEventPublishPort,
        order_repository_port: OrderRepositoryPort,
        user_repository_port: UserRepositoryPort,
        stock_repository_port: StockRepositoryPort,
    ):
        self.order_event_publish_port = order_event_publish_port
        self.order_repository_port = order_repository_port
        self.user_repository_port = user_repository_port
        self.stock_repository_port = stock_repository_port

    def buy_order(self, buy_order_input_model: BuyOrderInputModel):
        with tracer.start_active_span(
            "OrderService-buy_order",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "buy_order_input_model",
                buy_order_input_model,
            )
            # TODO: Caching of user and stock
            # TODO: Can move to Order Service
            self.user_repository_port.check_user(user_id=buy_order_input_model.user_id)
            self.stock_repository_port.check_stock(
                stock_symbol=buy_order_input_model.stock_symbol
            )

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
            # TODO: Caching of user and stock
            # TODO: Can move to Order Service
            self.user_repository_port.check_user(user_id=sell_order_input_model.user_id)
            self.stock_repository_port.check_stock(
                stock_symbol=sell_order_input_model.stock_symbol
            )

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

            self.order_event_publish_port.create_order_event(
                order_event_model=OrderEventModel(
                    **cancel_order_input_model.dict(), type=OrderTypeEnum.CANCEL
                )
            )

    def get_orders(self, user_id: Optional[UUID]) -> List[GetOrderOutputModel]:
        with tracer.start_active_span(
            "OrderService-get_orders",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "user_id",
                user_id,
            )
            return self.order_repository_port.get_orders(user_id=user_id)

    def get_order(self, order_id: UUID) -> GetOrderOutputModel:
        with tracer.start_active_span(
            "OrderService-get_order",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "order_id",
                order_id,
            )
            return self.order_repository_port.get_order(order_id=order_id)
