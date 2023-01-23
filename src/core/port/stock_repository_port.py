from typing import Protocol

from src.core.model.stock.create_stock_input_model import CreateStockInputModel


class StockRepositoryPort(Protocol):
    def create_stock(self, create_stock_input_model: CreateStockInputModel):
        ...

    def check_stock(self, stock_symbol: str):
        ...
