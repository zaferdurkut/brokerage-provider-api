from opentracing_instrumentation import get_current_span

from src.core.model.stock.create_stock_input_model import CreateStockInputModel
from src.core.model.stock.ipo_stock_to_user_input_model import IPOStockToUserInputModel
from src.infra.adapter.repository.postgres.entity import UserStockEntity
from src.infra.adapter.repository.postgres.entity.stock_entity import StockEntity
from src.infra.adapter.repository.postgres.entity.user_entity import UserEntity
from src.infra.adapter.repository.postgres.repository_manager import RepositoryManager
from src.infra.config.open_tracing_config import tracer
from src.infra.exception.bad_request_exception import BadRequestException
from src.infra.exception.not_found_exception import NotFoundException


class StockRepository:
    def create_stock(self, create_stock_input_model: CreateStockInputModel):
        with tracer.start_active_span(
            "StockRepository-create_user",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "create_stock_input_model",
                create_stock_input_model,
            )
            with RepositoryManager() as repository_manager:
                stock_entity = (
                    repository_manager.query(StockEntity)
                    .filter(StockEntity.symbol == create_stock_input_model.symbol)
                    .filter(StockEntity.deleted.is_(False))
                    .first()
                )

                if stock_entity is not None:
                    raise BadRequestException(error_code=2004)

                user_entity = StockEntity(
                    amount=create_stock_input_model.amount,
                    name=create_stock_input_model.name,
                    symbol=create_stock_input_model.symbol,
                    first_price=create_stock_input_model.first_price,
                    currency=create_stock_input_model.currency,
                )
                repository_manager.add(user_entity)
                repository_manager.commit()

    def ipo_stock_to_user(
        self, ipo_stock_to_user_input_model: IPOStockToUserInputModel
    ):
        with tracer.start_active_span(
            "StockRepository-ipo_stock_to_user",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "ipo_stock_to_user_input_model",
                ipo_stock_to_user_input_model,
            )

            with RepositoryManager() as repository_manager:

                stock_entity = (
                    repository_manager.query(StockEntity)
                    .filter(
                        StockEntity.symbol == ipo_stock_to_user_input_model.stock_symbol
                    )
                    .filter(StockEntity.deleted.is_(False))
                    .first()
                )

                user_entity = (
                    repository_manager.query(UserEntity)
                    .filter(UserEntity.id == ipo_stock_to_user_input_model.user_id)
                    .filter(UserEntity.deleted.is_(False))
                    .first()
                )

                if user_entity is None:
                    raise NotFoundException(error_code=2003)

                if stock_entity is None:
                    raise NotFoundException(error_code=2005)

                total_price = (
                    ipo_stock_to_user_input_model.amount * stock_entity.first_price
                )

                if stock_entity.amount < ipo_stock_to_user_input_model.amount:
                    raise BadRequestException(error_code=2006)

                if user_entity.balance < total_price:
                    raise BadRequestException(error_code=2007)

                user_stock_entity = UserStockEntity(
                    amount=ipo_stock_to_user_input_model.amount,
                    user_id=ipo_stock_to_user_input_model.user_id,
                    stock_symbol=ipo_stock_to_user_input_model.stock_symbol,
                    price=total_price,
                )

                stock_entity.amount = (
                    stock_entity.amount - ipo_stock_to_user_input_model.amount
                )

                user_entity.balance = user_entity.balance - total_price

                repository_manager.merge(stock_entity)
                repository_manager.add(user_stock_entity)
                repository_manager.commit()
