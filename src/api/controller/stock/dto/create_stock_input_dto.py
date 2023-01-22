from pydantic import BaseModel, Field


class CreateStockInputDto(BaseModel):
    amount: float = Field(..., example=10)
    symbol: str = Field(..., example="AAPL")
    first_price: float = Field(..., example=137.87)
    currency: str = Field(..., example="USD")
