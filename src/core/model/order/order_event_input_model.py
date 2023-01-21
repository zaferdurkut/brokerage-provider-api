from pydantic import BaseModel


class CreateOrderInputModel(BaseModel):
    amount: float
    symbol: str
