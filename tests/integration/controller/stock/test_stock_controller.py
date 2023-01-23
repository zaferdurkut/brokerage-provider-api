import json

import pytest
from requests import Response
from starlette import status

from src.infra.adapter.repository.postgres.entity.stock_entity import StockEntity
from src.infra.adapter.repository.postgres.repository_manager import RepositoryManager
from tests.integration.controller.stock.test_constants import STOCK_CONTROLLER_BASE_PATH
from tests.integration.controller.stock.test_input import (
    generate_invalid_create_stock_inputs,
)
from tests.integration.test_input_common import (
    delete_all_tables,
    populate_create_stock_dto,
)


@pytest.fixture(autouse=True)
def clear_all_tables_before_after_each_method():
    delete_all_tables()
    yield
    delete_all_tables()


class TestStockController:
    def test_should_create_stock(self, test_client):
        # given
        create_stock_input_dto = populate_create_stock_dto()
        # when
        create_stock_response: Response = test_client.post(
            STOCK_CONTROLLER_BASE_PATH,
            data=create_stock_input_dto.json(),
        )

        # then
        assert create_stock_response.status_code == status.HTTP_201_CREATED

        with RepositoryManager() as repository_manager:
            stock_entity = (
                repository_manager.query(StockEntity)
                .filter(StockEntity.symbol == create_stock_input_dto.symbol)
                .filter(StockEntity.deleted.is_(False))
                .first()
            )
            assert stock_entity is not None
            assert stock_entity.name == create_stock_input_dto.name
            assert stock_entity.symbol == create_stock_input_dto.symbol
            assert stock_entity.first_price == create_stock_input_dto.first_price
            assert stock_entity.currency == create_stock_input_dto.currency
            assert stock_entity.price is None

    @pytest.mark.parametrize(
        "create_stock_input", generate_invalid_create_stock_inputs()
    )
    def test_should_raise_bad_request_error_when_create_stock_if_input_dto_is_invalid(
        self, test_client, create_stock_input
    ):
        # given
        # when
        create_stock_response: Response = test_client.post(
            STOCK_CONTROLLER_BASE_PATH,
            data=json.dumps(create_stock_input),
        )

        # then
        assert create_stock_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_raise_bad_request_exception_when_create_stock_if_stock_exists(
        self, test_client
    ):
        # given
        create_stock_input_dto = populate_create_stock_dto()
        create_stock_response: Response = test_client.post(
            STOCK_CONTROLLER_BASE_PATH,
            data=create_stock_input_dto.json(),
        )
        assert create_stock_response.status_code == status.HTTP_201_CREATED
        # when
        create_stock_response: Response = test_client.post(
            STOCK_CONTROLLER_BASE_PATH,
            data=create_stock_input_dto.json(),
        )

        # then
        assert create_stock_response.status_code == status.HTTP_400_BAD_REQUEST
