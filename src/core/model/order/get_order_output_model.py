from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.core.model.base_models.order_status import OrderStatusEnum
from src.core.model.base_models.order_type import OrderTypeEnum


class GetOrderOutputModel(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    price: float
    amount: float
    stock_symbol: str
    type: OrderTypeEnum
    status: OrderStatusEnum
