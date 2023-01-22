from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.core.model.base_models.order_type import OrderTypeEnum


class OrderEventModel(BaseModel):
    order_id: Optional[UUID]
    price: Optional[float]
    amount: Optional[float]
    stock_symbol: str
    type: OrderTypeEnum
    user_id: UUID
