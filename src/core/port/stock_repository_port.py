from typing import Protocol

from src.core.model.stock.create_stock_input_model import CreateStockInputModel
from src.core.model.stock.ipo_stock_to_user_input_model import IPOStockToUserInputModel


class StockRepositoryPort(Protocol):
    def create_stock(self, create_stock_input_model: CreateStockInputModel):
        ...

    def ipo_stock_to_user(
        self, ipo_stock_to_user_input_model: IPOStockToUserInputModel
    ):
        ...
