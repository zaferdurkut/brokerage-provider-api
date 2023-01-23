from typing import Protocol, Optional, List
from uuid import UUID

from src.core.model.order.get_order_output_model import GetOrderOutputModel


class OrderRepositoryPort(Protocol):
    def get_orders(self, user_id: Optional[UUID]) -> List[GetOrderOutputModel]:
        ...

    def get_order(self, order_id: UUID) -> GetOrderOutputModel:
        ...
