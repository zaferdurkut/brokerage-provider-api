from opentracing_instrumentation import get_current_span

from src.core.model.stock.create_stock_input_model import CreateStockInputModel
from src.core.model.stock.ipo_stock_to_user_input_model import IPOStockToUserInputModel
from src.core.port.stock_repository_port import StockRepositoryPort
from src.infra.config.open_tracing_config import tracer


class StockService:
    def __init__(
        self,
        stock_repository_port: StockRepositoryPort,
    ):
        self.stock_repository_port = stock_repository_port

    def create_stock(self, create_stock_input_model: CreateStockInputModel):
        with tracer.start_active_span(
            "StockService-create_stock",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "create_stock_input_model",
                create_stock_input_model,
            )
            self.stock_repository_port.create_stock(
                create_stock_input_model=create_stock_input_model
            )

    def ipo_stock_to_user(
        self, ipo_stock_to_user_input_model: IPOStockToUserInputModel
    ):
        with tracer.start_active_span(
            "StockService-create_stock",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "ipo_stock_to_user_input_model",
                ipo_stock_to_user_input_model,
            )
            self.stock_repository_port.ipo_stock_to_user(
                ipo_stock_to_user_input_model=ipo_stock_to_user_input_model
            )
