from src.core.service.user.order_service import OrderService
from src.core.service.user.user_service import UserService
from src.infra.config.dependency_injection_config import (
    get_user_repository,
    get_order_event_publisher,
)


def get_user_service():
    return UserService(
        user_repository_port=get_user_repository(),
    )


def get_order_service():
    return OrderService(
        order_event_publish_port=get_order_event_publisher(),
    )
