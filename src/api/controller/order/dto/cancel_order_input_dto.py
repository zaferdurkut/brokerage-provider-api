from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CancelOrderInputDto(BaseModel):
    order_id: UUID = Field(..., example=uuid4())
