from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.core.model.base_models.order_status import OrderStatusEnum
from src.core.model.base_models.order_type import OrderTypeEnum


class GetUserStockOutputDto(BaseModel):
    id: UUID = Field(..., example=uuid4())
    amount: float = Field(..., example=10)
    stock_symbol: str = Field(..., example="AAPL")
    price: float = Field(..., example=127.87)


class GetUserOrderOutputDto(BaseModel):
    id: UUID = Field(..., example=uuid4())
    created_at: datetime = Field(..., example=datetime.utcnow())
    price: float = Field(..., example=110.123)
    amount: float = Field(..., example=11.123)
    stock_symbol: str = Field(..., example="AAPL")
    type: OrderTypeEnum = Field(..., example=OrderTypeEnum.BUY)
    status: OrderStatusEnum = Field(..., example=OrderStatusEnum.COMPLETED)


class GetUserOutputDto(BaseModel):
    id: UUID = Field(..., example=uuid4())
    name: str = Field(..., example="Zafer")
    surname: str = Field(..., example="Durkut")
    email: str = Field(..., example="sad@asd.com")
    balance: Optional[float] = Field(None, example=37000.60)
    orders: List[GetUserOrderOutputDto]
    stocks: List[GetUserStockOutputDto]
