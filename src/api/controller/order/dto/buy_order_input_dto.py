from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BuyOrderInputDto(BaseModel):
    price: float = Field(..., example=110.123)
    amount: float = Field(..., example=11.123)
    stock_symbol: str = Field(..., example="APPL")
    user_id: UUID = Field(..., example=uuid4())