from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from src.core.model.base_models.order_status import OrderStatusEnum
from src.core.model.base_models.order_type import OrderTypeEnum


class GetUserStockOutputModel(BaseModel):
    id: UUID
    amount: float
    stock_symbol: str
    price: float


class GetUserOrderOutputModel(BaseModel):
    id: UUID
    price: Optional[float]
    amount: Optional[float]
    stock_symbol: str
    type: OrderTypeEnum
    status: OrderStatusEnum


class GetUserOutputModel(BaseModel):
    id: UUID
    name: str
    surname: str
    email: str
    balance: Optional[float]
    orders: List[GetUserOrderOutputModel]
    stocks: List[GetUserStockOutputModel]
