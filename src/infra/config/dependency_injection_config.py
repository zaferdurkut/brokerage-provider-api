from typing import cast

from src.core.port.user_repository_port import UserRepositoryPort
from src.infra.adapter.repository.postgres.user_repository import UserRepository


def get_user_repository():
    return cast(UserRepositoryPort, UserRepository)
