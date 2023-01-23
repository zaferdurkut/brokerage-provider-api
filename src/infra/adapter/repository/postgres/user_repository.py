from uuid import UUID

from opentracing_instrumentation import get_current_span

from src.core.model.base_models.user_type import UserTypeEnum
from src.core.model.user.create_user_input_model import CreateUserInputModel
from src.core.model.user.create_user_output_model import CreateUserOutputModel
from src.core.model.user.get_user_output_model import (
    GetUserOutputModel,
    GetUserOrderOutputModel,
    GetUserStockOutputModel,
)
from src.infra.adapter.repository.postgres.entity import UserStockEntity
from src.infra.adapter.repository.postgres.entity.stock_entity import StockEntity
from src.infra.adapter.repository.postgres.entity.user_entity import UserEntity
from src.infra.adapter.repository.postgres.repository_manager import RepositoryManager
from src.infra.config.open_tracing_config import tracer
from src.infra.exception.not_found_exception import NotFoundException
from src.infra.util.constants import DEFAULT_USER_STOCK_AMOUNT


class UserRepository:
    def create_user(
        self, create_user_input_model: CreateUserInputModel
    ) -> CreateUserOutputModel:
        with tracer.start_active_span(
            "UserRepository-create_user",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "create_user_input_model",
                create_user_input_model,
            )
            with RepositoryManager() as repository_manager:
                user_entity = UserEntity(
                    name=create_user_input_model.name,
                    surname=create_user_input_model.surname,
                    email=create_user_input_model.email,
                    balance=create_user_input_model.balance,
                    type=UserTypeEnum.NORMAL,
                )
                repository_manager.add(user_entity)
                repository_manager.commit()

                ## TODO: Mock data for user stock initializing - Start
                stock_entities = (
                    repository_manager.query(StockEntity)
                    .filter(StockEntity.deleted.is_(False))
                    .all()
                )
                for stock_entity in stock_entities:
                    user_stock_entity = UserStockEntity(
                        user_id=user_entity.id,
                        stock_symbol=stock_entity.symbol,
                        amount=DEFAULT_USER_STOCK_AMOUNT,
                        price=stock_entity.first_price * DEFAULT_USER_STOCK_AMOUNT,
                    )
                    repository_manager.add(user_stock_entity)
                    repository_manager.commit()

                ## TODO: Mock data for user stock initializing - End
                return CreateUserOutputModel(id=user_entity.id)

    def get_user(self, user_id: UUID) -> GetUserOutputModel:
        with tracer.start_active_span(
            "UserRepository-create_user",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "user_id",
                user_id,
            )
            with RepositoryManager() as repository_manager:
                user_entity = (
                    repository_manager.query(UserEntity)
                    .filter(UserEntity.id == user_id)
                    .filter(UserEntity.deleted.is_(False))
                    .first()
                )
                if user_entity is None:
                    raise NotFoundException(error_code=2003)

                orders = [
                    GetUserOrderOutputModel(**order_item.__dict__)
                    for order_item in user_entity.user_orders
                ]
                orders = sorted(orders, key=lambda x: x.created_at, reverse=True)

                return GetUserOutputModel(
                    **user_entity.__dict__,
                    orders=orders,
                    stocks=[
                        GetUserStockOutputModel(
                            **stock_item.__dict__, total_price=stock_item.price
                        )
                        for stock_item in user_entity.user_stocks
                    ],
                )

    def check_user(self, user_id: UUID):
        with tracer.start_active_span(
            "UserRepository-check_user",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "user_id",
                user_id,
            )
            with RepositoryManager() as repository_manager:
                user_entity = (
                    repository_manager.query(UserEntity)
                    .filter(UserEntity.id == user_id)
                    .filter(UserEntity.deleted.is_(False))
                    .first()
                )
                if user_entity is None:
                    raise NotFoundException(error_code=2003)
