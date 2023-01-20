from src.core.port.user_repository_port import UserRepositoryPort


class UserService:
    def __init__(
        self,
        user_repository_port: UserRepositoryPort,
    ):
        self.user_repository_port = user_repository_port
