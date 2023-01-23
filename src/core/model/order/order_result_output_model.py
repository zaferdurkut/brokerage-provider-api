from typing import Optional

from pydantic import BaseModel

from src.core.model.base_models.order_status import OrderStatusEnum


class OrderRepositoryResultOutputModel(BaseModel):
    status: OrderStatusEnum
    error_code: Optional[int]
