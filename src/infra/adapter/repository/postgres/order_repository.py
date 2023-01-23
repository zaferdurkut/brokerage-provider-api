from typing import Optional, List
from uuid import UUID

from opentracing_instrumentation import get_current_span

from src.core.model.base_models.order_status import OrderStatusEnum
from src.core.model.base_models.order_type import OrderTypeEnum
from src.core.model.order.buy_order_input_model import BuyOrderInputModel
from src.core.model.order.cancel_order_input_model import CancelOrderInputModel
from src.core.model.order.get_order_output_model import GetOrderOutputModel
from src.core.model.order.order_result_output_model import (
    OrderRepositoryResultOutputModel,
)
from src.core.model.order.sell_order_input_model import SellOrderInputModel
from src.infra.adapter.repository.postgres.entity import OrderEntity
from src.infra.adapter.repository.postgres.repository_manager import RepositoryManager
from src.infra.config.logging_config import get_logger
from src.infra.config.open_tracing_config import tracer
from src.infra.exception.not_found_exception import NotFoundException

logger = get_logger()


class OrderRepository:
    def buy_order(
        self, buy_order_input_model: BuyOrderInputModel
    ) -> OrderRepositoryResultOutputModel:
        with tracer.start_active_span(
            "OrderRepository-buy_order",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "buy_order_input_model",
                buy_order_input_model,
            )

            order_result_model = OrderRepositoryResultOutputModel(
                status=OrderStatusEnum.WAITING
            )
            with RepositoryManager() as repository_manager:
                try:
                    order_entity = OrderEntity(
                        stock_symbol=buy_order_input_model.stock_symbol,
                        user_id=buy_order_input_model.user_id,
                        price=buy_order_input_model.price,
                        amount=buy_order_input_model.amount,
                        type=OrderTypeEnum.BUY,
                        status=OrderStatusEnum.WAITING,
                    )

                    order_entity.error_code = order_result_model.error_code
                    order_entity.status = order_result_model.status
                    repository_manager.add(order_entity)
                    repository_manager.commit()
                except Exception as exc:
                    logger.error(str(exc))
                    order_result_model.error_code = 2008

                return order_result_model

    def sell_order(
        self, sell_order_input_model: SellOrderInputModel
    ) -> OrderRepositoryResultOutputModel:
        with tracer.start_active_span(
            "OrderRepository-sell_order",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "sell_order_input_model",
                sell_order_input_model,
            )

            order_result_model = OrderRepositoryResultOutputModel(
                status=OrderStatusEnum.WAITING
            )
            with RepositoryManager() as repository_manager:
                try:
                    order_entity = OrderEntity(
                        stock_symbol=sell_order_input_model.stock_symbol,
                        user_id=sell_order_input_model.user_id,
                        price=sell_order_input_model.price,
                        amount=sell_order_input_model.amount,
                        type=OrderTypeEnum.SELL,
                        status=OrderStatusEnum.WAITING,
                    )

                    order_entity.error_code = order_result_model.error_code
                    order_entity.status = order_result_model.status
                    repository_manager.add(order_entity)
                    repository_manager.commit()
                except Exception as exc:
                    logger.error(str(exc))
                    order_result_model.error_code = 2009

                return order_result_model

    def cancel_order(
        self, cancel_order_input_model: CancelOrderInputModel
    ) -> OrderRepositoryResultOutputModel:
        with tracer.start_active_span(
            "OrderRepository-cancel_order",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "cancel_order_input_model",
                cancel_order_input_model,
            )

            order_result_model = OrderRepositoryResultOutputModel(
                status=OrderStatusEnum.CANCELLED
            )
            with RepositoryManager() as repository_manager:
                try:
                    order_entity = (
                        repository_manager.query(OrderEntity)
                        .filter(OrderEntity.id == cancel_order_input_model.order_id)
                        .filter(OrderEntity.deleted.is_(False))
                        .first()
                    )

                    if order_entity is None:
                        raise NotFoundException(error_code=2011)
                    order_result_model.status = order_entity.status

                    if order_entity.status == OrderStatusEnum.WAITING:
                        order_result_model.status = OrderStatusEnum.CANCELLED
                    elif order_entity.status == OrderStatusEnum.COMPLETED:
                        order_result_model.error_code = 2012
                    elif order_entity.status == OrderStatusEnum.FAILED:
                        order_result_model.error_code = 2013
                    elif order_entity.status == OrderStatusEnum.CANCELLED:
                        order_result_model.error_code = 2014

                    if order_result_model.error_code is None:
                        order_entity.error_code = order_result_model.error_code
                        order_entity.status = order_result_model.status
                        repository_manager.merge(order_entity)
                        repository_manager.commit()

                except NotFoundException as exc:
                    logger.error(str(exc))
                    order_result_model.error_code = 2011

                except Exception as exc:
                    logger.error(str(exc))
                    order_result_model.error_code = 2010

                return order_result_model

    def get_orders(self, user_id: Optional[UUID]) -> List[GetOrderOutputModel]:
        with tracer.start_active_span(
            "OrderRepository-get_orders",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "user_id",
                user_id,
            )
            with RepositoryManager() as repository_manager:
                filters = []
                if user_id is not None:
                    filters.append(OrderEntity.user_id == user_id)

                order_entities = (
                    repository_manager.query(OrderEntity)
                    .filter(*filters)
                    .filter(OrderEntity.deleted.is_(False))
                    .order_by(OrderEntity.created_at.desc())
                    .all()
                )

                result = [
                    GetOrderOutputModel(**order_entity.__dict__)
                    for order_entity in order_entities
                ]

                return result

    def get_order(self, order_id: UUID) -> GetOrderOutputModel:
        with tracer.start_active_span(
            "OrderRepository-get_order",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "order_id",
                order_id,
            )
            with RepositoryManager() as repository_manager:
                order_entity = (
                    repository_manager.query(OrderEntity)
                    .filter(OrderEntity.id == order_id)
                    .filter(OrderEntity.deleted.is_(False))
                    .first()
                )

                if order_entity is None:
                    raise NotFoundException(error_code=2011)

                return GetOrderOutputModel(**order_entity.__dict__)
