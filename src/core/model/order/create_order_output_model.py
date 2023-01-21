from uuid import UUID

from pydantic import BaseModel


class CreateOrderOutputModel(BaseModel):
    id: UUID
