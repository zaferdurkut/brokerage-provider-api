from typing import Optional

from pydantic import BaseModel


class CreateUserInputModel(BaseModel):
    name: str
    surname: str
    email: str
    balance: Optional[float]
