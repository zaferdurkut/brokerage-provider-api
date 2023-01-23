from uuid import UUID

from pydantic import BaseModel


class CancelOrderInputModel(BaseModel):
    order_id: UUID
