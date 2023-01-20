from src.core.service.user_service import UserService
from src.infra.config.dependency_injection_config import (
    get_user_repository,
)


def get_user_service():
    return UserService(
        get_user_repository(),
    )
