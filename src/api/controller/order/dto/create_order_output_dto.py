from pydantic import BaseModel, Field
from uuid import UUID


class CreateOrderOutputDto(BaseModel):
    id: UUID = Field(..., example="111d0a13-ea9a-4d6e-82e4-46f2d339f8e2")
