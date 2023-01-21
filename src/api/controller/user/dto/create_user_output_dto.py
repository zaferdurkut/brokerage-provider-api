from uuid import UUID

from pydantic import BaseModel


class CreateUserOutputDto(BaseModel):
    id: UUID
