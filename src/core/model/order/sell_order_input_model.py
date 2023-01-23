from uuid import UUID

from pydantic import BaseModel


class SellOrderInputModel(BaseModel):
    price: float
    amount: float
    stock_symbol: str
    user_id: UUID
