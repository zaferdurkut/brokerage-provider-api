from src.core.service.order_service import OrderService
from src.core.service.stock_service import StockService
from src.core.service.user_service import UserService
from src.infra.config.dependency_injection_config import (
    get_user_repository,
    get_order_event_publisher,
    get_stock_repository,
    get_order_repository,
)


def get_user_service():
    return UserService(
        user_repository_port=get_user_repository(),
    )


def get_order_service():
    return OrderService(
        order_event_publish_port=get_order_event_publisher(),
        order_repository_port=get_order_repository(),
        user_repository_port=get_user_repository(),
        stock_repository_port=get_stock_repository(),
    )


def get_stock_service():
    return StockService(
        stock_repository_port=get_stock_repository(),
    )
