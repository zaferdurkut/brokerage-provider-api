from pydantic import BaseModel, Field


class CreateOrderInputDto(BaseModel):
    amount: float = Field(..., example=11.123)
    symbol: str = Field(..., example="APPL")
