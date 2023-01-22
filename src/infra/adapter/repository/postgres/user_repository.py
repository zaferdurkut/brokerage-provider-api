from src.core.model.user.create_user_input_model import CreateUserInputModel
from src.core.model.user.create_user_output_model import CreateUserOutputModel


class UserRepository:
    def create_user(
        self, create_user_input_model: CreateUserInputModel
    ) -> CreateUserOutputModel:
        ...
