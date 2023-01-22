from typing import Protocol
from uuid import UUID

from src.core.model.user.create_user_input_model import CreateUserInputModel
from src.core.model.user.create_user_output_model import CreateUserOutputModel
from src.core.model.user.get_user_output_model import GetUserOutputModel


class UserRepositoryPort(Protocol):
    def create_user(
        self, create_user_input_model: CreateUserInputModel
    ) -> CreateUserOutputModel:
        ...

    def get_user(self, user_id: UUID) -> GetUserOutputModel:
        ...
