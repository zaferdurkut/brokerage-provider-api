from opentracing_instrumentation import get_current_span

from src.core.model.stock.create_stock_input_model import CreateStockInputModel
from src.infra.adapter.repository.postgres.entity.stock_entity import StockEntity
from src.infra.adapter.repository.postgres.repository_manager import RepositoryManager
from src.infra.config.open_tracing_config import tracer
from src.infra.exception.bad_request_exception import BadRequestException
from src.infra.exception.not_found_exception import NotFoundException


class StockRepository:
    def create_stock(self, create_stock_input_model: CreateStockInputModel):
        with tracer.start_active_span(
            "StockRepository-create_stock",
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

    def check_stock(self, stock_symbol: str):
        with tracer.start_active_span(
            "StockRepository-check_stock",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "stock_symbol",
                stock_symbol,
            )
            with RepositoryManager() as repository_manager:
                stock_entity = (
                    repository_manager.query(StockEntity)
                    .filter(StockEntity.symbol == stock_symbol)
                    .filter(StockEntity.deleted.is_(False))
                    .first()
                )

                if stock_entity is None:
                    raise NotFoundException(error_code=2005)
