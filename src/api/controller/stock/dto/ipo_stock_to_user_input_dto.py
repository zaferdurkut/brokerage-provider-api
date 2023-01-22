from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class IPOStockToUserInputDto(BaseModel):
    amount: float = Field(..., example=5)
    user_id: UUID = Field(..., example=uuid4())
    stock_symbol: str = Field(..., example="AAPL")
