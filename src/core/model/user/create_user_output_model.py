from uuid import UUID

from pydantic import BaseModel


class CreateUserOutputModel(BaseModel):
    id: UUID
