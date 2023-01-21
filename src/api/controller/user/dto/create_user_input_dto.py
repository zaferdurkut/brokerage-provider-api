from typing import Optional

from pydantic import BaseModel, Field


class CreateUserInputDto(BaseModel):
    name: str = Field(..., example="Zafer")
    surname: str = Field(..., example="Durkut")
    email: str = Field(..., example="sad@asd.com")
    balance: Optional[float] = Field(default=37000, example=37000.60)
