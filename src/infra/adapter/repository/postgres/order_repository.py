from typing import Optional, List
from uuid import UUID

from opentracing_instrumentation import get_current_span
from sqlalchemy import func

from src.core.model.base_models.order_status import OrderStatusEnum
from src.core.model.base_models.order_type import OrderTypeEnum
from src.core.model.order.buy_order_input_model import BuyOrderInputModel
from src.core.model.order.cancel_order_input_model import CancelOrderInputModel
from src.core.model.order.get_order_output_model import GetOrderOutputModel
from src.core.model.order.order_result_output_model import (
    OrderRepositoryResultOutputModel,
)
from src.core.model.order.sell_order_input_model import SellOrderInputModel
from src.infra.adapter.repository.postgres.entity import OrderEntity, UserStockEntity
from src.infra.adapter.repository.postgres.entity.stock_entity import StockEntity
from src.infra.adapter.repository.postgres.entity.user_entity import UserEntity
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

                    user_entity = self._get_user(user_id=buy_order_input_model.user_id)

                    total_waiting_amount = self._get_total_waiting_amount(
                        user_id=buy_order_input_model.user_id,
                        stock_symbol=buy_order_input_model.stock_symbol,
                        order_type=OrderTypeEnum.BUY,
                    )

                    if (
                        order_entity.amount + total_waiting_amount
                    ) * order_entity.price > user_entity.balance:
                        order_result_model.status = OrderStatusEnum.FAILED
                        order_result_model.error_code = 2006

                    order_entity.error_code = order_result_model.error_code
                    order_entity.status = order_result_model.status
                    repository_manager.add(order_entity)
                    repository_manager.commit()
                    order_result_model.order_id = order_entity.id
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

                    user_entity = self._get_user(user_id=sell_order_input_model.user_id)

                    user_stock_amount = self._get_user_stock_amount(
                        user_id=user_entity.id,
                        stock_symbol=sell_order_input_model.stock_symbol,
                    )

                    total_waiting_amount = self._get_total_waiting_amount(
                        user_id=sell_order_input_model.user_id,
                        stock_symbol=sell_order_input_model.stock_symbol,
                        order_type=OrderTypeEnum.SELL,
                    )

                    if order_entity.amount + total_waiting_amount > user_stock_amount:
                        order_result_model.status = OrderStatusEnum.FAILED
                        order_result_model.error_code = 2007

                    order_entity.error_code = order_result_model.error_code
                    order_entity.status = order_result_model.status
                    repository_manager.add(order_entity)
                    repository_manager.commit()
                    order_result_model.order_id = order_entity.id
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

                    order_result_model.user_id = order_entity.user_id
                    order_result_model.order_id = order_entity.id

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

    def _get_user(self, user_id: UUID) -> UserEntity:
        with RepositoryManager() as repository_manager:
            user_entity = (
                repository_manager.query(UserEntity)
                .filter(UserEntity.id == user_id)
                .filter(UserEntity.deleted.is_(False))
                .first()
            )

            return user_entity

    def _get_user_stock_amount(self, user_id: UUID, stock_symbol: str) -> float:
        with RepositoryManager() as repository_manager:
            user_stock_entity = (
                repository_manager.query(UserStockEntity)
                .filter(UserStockEntity.user_id == user_id)
                .filter(UserStockEntity.stock_symbol == stock_symbol)
                .filter(UserStockEntity.deleted.is_(False))
                .first()
            )

            if user_stock_entity is None:
                return 0

            return user_stock_entity.amount

    def _get_total_waiting_amount(
        self, user_id: UUID, stock_symbol: str, order_type: OrderTypeEnum
    ):
        with RepositoryManager() as repository_manager:
            waiting_order_entities = (
                repository_manager.query(
                    func.sum(OrderEntity.amount).label("total_waiting_amount")
                )
                .filter(OrderEntity.user_id == user_id)
                .filter(OrderEntity.stock_symbol == stock_symbol)
                .filter(OrderEntity.status == OrderStatusEnum.WAITING)
                .filter(OrderEntity.type == order_type)
                .filter(OrderEntity.deleted.is_(False))
                .first()
            )

            total_waiting_amount = waiting_order_entities.total_waiting_amount

            if total_waiting_amount is None:
                total_waiting_amount = 0

            return total_waiting_amount
