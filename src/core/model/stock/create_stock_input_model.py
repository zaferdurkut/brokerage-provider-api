from pydantic import BaseModel


class CreateStockInputModel(BaseModel):
    amount: float
    name: str
    symbol: str
    first_price: float
    currency: str
