import pytest
from starlette.testclient import TestClient

from main import app
from src.core.service.user_service import UserService
from src.infra.adapter.repository.postgres.user_repository import UserRepository


@pytest.fixture(scope="session")
def test_client():
    return TestClient(app, base_url="http://localhost")


@pytest.fixture(scope="session")
def user_repository_postgres_adapter():
    return UserRepository()


@pytest.fixture(scope="session")
def user_service(
    user_repository_postgres_adapter,
):
    return UserService(user_repository_port=user_repository_postgres_adapter)
