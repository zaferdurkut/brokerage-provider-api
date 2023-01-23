from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field, BaseModel

from src.core.model.base_models.order_status import OrderStatusEnum
from src.core.model.base_models.order_type import OrderTypeEnum


class GetOrderOutputDto(BaseModel):
    id: UUID = Field(..., example=uuid4())
    user_id: UUID = Field(..., example=uuid4())
    created_at: datetime = Field(..., example=datetime.utcnow())
    updated_at: Optional[datetime] = Field(None, example=datetime.utcnow())
    price: float = Field(..., example=110.123)
    amount: float = Field(..., example=11.123)
    stock_symbol: str = Field(..., example="AAPL")
    type: OrderTypeEnum = Field(..., example=OrderTypeEnum.BUY)
    status: OrderStatusEnum = Field(..., example=OrderStatusEnum.WAITING)
    error_code: Optional[int] = Field(None)
