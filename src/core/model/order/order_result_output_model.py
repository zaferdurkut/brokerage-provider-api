from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.core.model.base_models.order_status import OrderStatusEnum


class OrderRepositoryResultOutputModel(BaseModel):
    order_id: Optional[UUID]
    user_id: Optional[UUID]
    status: OrderStatusEnum
    error_code: Optional[int]
