from uuid import UUID

from pydantic import BaseModel


class IPOStockToUserInputModel(BaseModel):
    amount: float
    user_id: UUID
    stock_symbol: str
