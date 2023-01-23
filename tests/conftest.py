import pytest
from starlette.testclient import TestClient

from main import app
from src.core.port.order_event_publish_port import OrderEventPublishPort
from src.core.service.order_service import OrderService
from src.core.service.stock_service import StockService
from src.core.service.user_service import UserService
from src.infra.adapter.repository.postgres.order_repository import OrderRepository
from src.infra.adapter.repository.postgres.stock_repository import StockRepository
from src.infra.adapter.repository.postgres.user_repository import UserRepository


@pytest.fixture(scope="session")
def test_client():
    return TestClient(app, base_url="http://localhost")


@pytest.fixture(scope="session")
def user_repository_postgres_adapter():
    return UserRepository()


@pytest.fixture(scope="session")
def order_repository_postgres_adapter():
    return OrderRepository()


@pytest.fixture(scope="session")
def stock_repository_postgres_adapter():
    return StockRepository()


@pytest.fixture(scope="session")
def order_event_publisher_kafka_adapter():
    return OrderEventPublishPort()


@pytest.fixture(scope="session")
def user_service(
    user_repository_postgres_adapter,
):
    return UserService(user_repository_port=user_repository_postgres_adapter)


@pytest.fixture(scope="session")
def stock_service(
    stock_repository_postgres_adapter,
):
    return StockService(stock_repository_port=stock_repository_postgres_adapter)


@pytest.fixture(scope="session")
def order_service(
    order_repository_postgres_adapter,
    order_event_publisher_kafka_adapter,
    user_repository_postgres_adapter,
    stock_repository_postgres_adapter,
):
    return OrderService(
        order_repository_port=order_repository_postgres_adapter,
        order_event_publish_port=order_event_publisher_kafka_adapter,
        user_repository_port=user_repository_postgres_adapter,
        stock_repository_port=stock_repository_postgres_adapter,
    )
