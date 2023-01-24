from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.core.model.base_models.order_status import OrderStatusEnum
from src.core.model.user.get_user_output_model import GetUserOutputModel


class NotificationErrorEventModel(BaseModel):
    error_message: Optional[str]
    error_code: Optional[int]
    is_system_error: Optional[bool]


class NotificationEventModel(BaseModel):
    user: Optional[GetUserOutputModel]
    order_id: Optional[UUID]
    status: OrderStatusEnum
    error: Optional[NotificationErrorEventModel]
