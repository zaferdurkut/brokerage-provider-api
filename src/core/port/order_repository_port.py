from typing import Protocol, Optional, List
from uuid import UUID

from src.core.model.order.get_order_output_model import GetOrderOutputModel
from src.core.model.stock.create_stock_input_model import CreateStockInputModel
from src.core.model.stock.ipo_stock_to_user_input_model import IPOStockToUserInputModel


class OrderRepositoryPort(Protocol):
    def get_orders(self, user_id: Optional[UUID]) -> List[GetOrderOutputModel]:
        ...

    def get_order(self, order_id: UUID) -> GetOrderOutputModel:
        ...
