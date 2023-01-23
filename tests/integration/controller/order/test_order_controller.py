import json
from time import sleep
from uuid import uuid4

import pytest
from requests import Response
from starlette import status

from src.api.controller.order.dto.cancel_order_input_dto import CancelOrderInputDto
from src.api.controller.order.dto.get_order_output_dto import GetOrderOutputDto
from src.core.model.base_models.order_status import OrderStatusEnum
from src.core.model.base_models.order_type import OrderTypeEnum
from src.infra.adapter.repository.postgres.entity import OrderEntity
from src.infra.adapter.repository.postgres.repository_manager import RepositoryManager
from tests.integration.controller.order.test_constants import (
    ORDER_CONTROLLER_BUY_PATH,
    ORDER_CONTROLLER_SELL_PATH,
    ORDER_WAITING_TIME,
    ORDER_CONTROLLER_BASE_PATH,
    ORDER_CONTROLLER_CANCEL_PATH,
)
from tests.integration.controller.order.test_input import (
    populate_user_id_and_stock,
    generate_invalid_buy_order_inputs,
    generate_invalid_sell_order_inputs,
)
from tests.integration.test_input_common import (
    delete_all_tables,
    populate_buy_order_dto,
    populate_sell_order_dto,
)


@pytest.fixture(autouse=True)
def clear_all_tables_before_after_each_method():
    delete_all_tables()
    yield
    delete_all_tables()


class TestOrderController:
    def test_should_buy_order(self, test_client):
        # given
        user_id, stock_symbol = populate_user_id_and_stock(test_client)
        buy_order_input_dto = populate_buy_order_dto()
        buy_order_input_dto.user_id = user_id
        buy_order_input_dto.stock_symbol = stock_symbol

        # when
        buy_order_response: Response = test_client.post(
            ORDER_CONTROLLER_BUY_PATH,
            data=buy_order_input_dto.json(),
        )

        # then
        assert buy_order_response.status_code == status.HTTP_202_ACCEPTED

        sleep(ORDER_WAITING_TIME)

        with RepositoryManager() as repository_manager:
            order_entity = (
                repository_manager.query(OrderEntity)
                .filter(OrderEntity.stock_symbol == buy_order_input_dto.stock_symbol)
                .filter(OrderEntity.deleted.is_(False))
                .first()
            )
            assert order_entity is not None
            assert str(order_entity.user_id) == user_id
            assert order_entity.price == buy_order_input_dto.price
            assert order_entity.amount == buy_order_input_dto.amount
            assert order_entity.stock_symbol == buy_order_input_dto.stock_symbol
            assert order_entity.type == OrderTypeEnum.BUY
            assert order_entity.status == OrderStatusEnum.WAITING
            assert order_entity.error_code is None

    @pytest.mark.parametrize("buy_order_input", generate_invalid_buy_order_inputs())
    def test_should_raise_bad_request_error_when_buy_order_if_input_dto_is_invalid(
        self, test_client, buy_order_input
    ):
        # given
        # when
        buy_order_response: Response = test_client.post(
            ORDER_CONTROLLER_BUY_PATH,
            data=json.dumps(buy_order_input),
        )
        # then
        assert buy_order_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_raise_not_found_error_when_buy_order_if_user_id_does_not_exist(
        self, test_client
    ):
        # given
        _, stock_symbol = populate_user_id_and_stock(test_client)
        buy_order_input_dto = populate_buy_order_dto()
        buy_order_input_dto.user_id = uuid4()
        buy_order_input_dto.stock_symbol = stock_symbol

        # when
        buy_order_response: Response = test_client.post(
            ORDER_CONTROLLER_BUY_PATH,
            data=buy_order_input_dto.json(),
        )

        # then
        assert buy_order_response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_raise_not_found_error_when_buy_order_if_stock_does_not_exist(
        self, test_client
    ):
        # given
        user_id, stock_symbol = populate_user_id_and_stock(test_client)
        buy_order_input_dto = populate_buy_order_dto()
        buy_order_input_dto.user_id = user_id
        buy_order_input_dto.stock_symbol = stock_symbol + "X"

        # when
        buy_order_response: Response = test_client.post(
            ORDER_CONTROLLER_BUY_PATH,
            data=buy_order_input_dto.json(),
        )

        # then
        assert buy_order_response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_sell_order(self, test_client):
        # given
        user_id, stock_symbol = populate_user_id_and_stock(test_client)
        sell_order_input_dto = populate_sell_order_dto()
        sell_order_input_dto.user_id = user_id
        sell_order_input_dto.stock_symbol = stock_symbol

        # when
        sell_order_response: Response = test_client.post(
            ORDER_CONTROLLER_SELL_PATH,
            data=sell_order_input_dto.json(),
        )

        # then
        assert sell_order_response.status_code == status.HTTP_202_ACCEPTED

        sleep(ORDER_WAITING_TIME)

        with RepositoryManager() as repository_manager:
            order_entity = (
                repository_manager.query(OrderEntity)
                .filter(OrderEntity.stock_symbol == sell_order_input_dto.stock_symbol)
                .filter(OrderEntity.deleted.is_(False))
                .first()
            )
            assert order_entity is not None
            assert str(order_entity.user_id) == user_id
            assert order_entity.price == sell_order_input_dto.price
            assert order_entity.amount == sell_order_input_dto.amount
            assert order_entity.stock_symbol == sell_order_input_dto.stock_symbol
            assert order_entity.type == OrderTypeEnum.SELL
            assert order_entity.status == OrderStatusEnum.WAITING
            assert order_entity.error_code is None

    @pytest.mark.parametrize("sell_order_input", generate_invalid_sell_order_inputs())
    def test_should_raise_bad_request_error_when_sell_order_if_input_dto_is_invalid(
        self, test_client, sell_order_input
    ):
        # given
        # when
        sell_order_response: Response = test_client.post(
            ORDER_CONTROLLER_SELL_PATH,
            data=json.dumps(sell_order_input),
        )
        # then
        assert sell_order_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_raise_not_found_error_when_sell_order_if_user_id_does_not_exist(
        self, test_client
    ):
        # given
        _, stock_symbol = populate_user_id_and_stock(test_client)
        sell_order_input_dto = populate_sell_order_dto()
        sell_order_input_dto.user_id = uuid4()
        sell_order_input_dto.stock_symbol = stock_symbol

        # when
        sell_order_response: Response = test_client.post(
            ORDER_CONTROLLER_SELL_PATH,
            data=sell_order_input_dto.json(),
        )

        # then
        assert sell_order_response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_raise_not_found_error_when_sell_order_if_stock_does_not_exist(
        self, test_client
    ):
        # given
        user_id, stock_symbol = populate_user_id_and_stock(test_client)
        sell_order_input_dto = populate_sell_order_dto()
        sell_order_input_dto.user_id = user_id
        sell_order_input_dto.stock_symbol = stock_symbol + "X"

        # when
        sell_order_response: Response = test_client.post(
            ORDER_CONTROLLER_SELL_PATH,
            data=sell_order_input_dto.json(),
        )

        # then
        assert sell_order_response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_get_orders(self, test_client):
        # given
        user_id, stock_symbol = populate_user_id_and_stock(test_client)
        sell_order_input_dto = populate_sell_order_dto()
        sell_order_input_dto.user_id = user_id
        sell_order_input_dto.stock_symbol = stock_symbol

        sell_order_response: Response = test_client.post(
            ORDER_CONTROLLER_SELL_PATH,
            data=sell_order_input_dto.json(),
        )
        assert sell_order_response.status_code == status.HTTP_202_ACCEPTED

        sleep(ORDER_WAITING_TIME)

        # when
        get_orders_response: Response = test_client.get(
            ORDER_CONTROLLER_BASE_PATH,
        )

        # then
        assert get_orders_response.status_code == status.HTTP_200_OK
        get_orders_response_data = get_orders_response.json()
        assert len(get_orders_response_data) == 1
        get_orders_response_data_model = GetOrderOutputDto(
            **get_orders_response_data[0]
        )
        assert str(get_orders_response_data_model.user_id) == user_id
        assert get_orders_response_data_model.price == sell_order_input_dto.price
        assert get_orders_response_data_model.amount == sell_order_input_dto.amount
        assert (
            get_orders_response_data_model.stock_symbol
            == sell_order_input_dto.stock_symbol
        )
        assert get_orders_response_data_model.type == OrderTypeEnum.SELL
        assert get_orders_response_data_model.status == OrderStatusEnum.WAITING

    def test_should_get_order(self, test_client):
        # given
        user_id, stock_symbol = populate_user_id_and_stock(test_client)
        sell_order_input_dto = populate_sell_order_dto()
        sell_order_input_dto.user_id = user_id
        sell_order_input_dto.stock_symbol = stock_symbol

        sell_order_response: Response = test_client.post(
            ORDER_CONTROLLER_SELL_PATH,
            data=sell_order_input_dto.json(),
        )
        assert sell_order_response.status_code == status.HTTP_202_ACCEPTED

        sleep(ORDER_WAITING_TIME)
        get_orders_response: Response = test_client.get(
            ORDER_CONTROLLER_BASE_PATH,
        )
        assert get_orders_response.status_code == status.HTTP_200_OK
        get_orders_response_data = get_orders_response.json()
        get_orders_response_data_model = GetOrderOutputDto(
            **get_orders_response_data[0]
        )
        assert len(get_orders_response_data) == 1

        # when
        get_order_response: Response = test_client.get(
            ORDER_CONTROLLER_BASE_PATH + f"/{str(get_orders_response_data_model.id)}",
        )

        # then
        assert get_order_response.status_code == status.HTTP_200_OK
        get_order_response_data = get_order_response.json()
        get_order_response_data_model = GetOrderOutputDto(**get_order_response_data)
        assert get_order_response_data_model.id == get_orders_response_data_model.id
        assert str(get_order_response_data_model.user_id) == user_id
        assert get_order_response_data_model.price == sell_order_input_dto.price
        assert get_order_response_data_model.amount == sell_order_input_dto.amount
        assert (
            get_order_response_data_model.stock_symbol
            == sell_order_input_dto.stock_symbol
        )
        assert get_order_response_data_model.type == OrderTypeEnum.SELL
        assert get_order_response_data_model.status == OrderStatusEnum.WAITING

    def test_should_raise_not_found_error_when_get_order_if_order_does_not_found(
        self, test_client
    ):
        # given

        # when
        get_order_response: Response = test_client.get(
            ORDER_CONTROLLER_BASE_PATH + f"/{str(uuid4())}",
        )

        # then
        assert get_order_response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_raise_bad_request_exception_when_get_order_if_order_id_is_invalid(
        self, test_client
    ):
        # given

        # when
        get_order_response: Response = test_client.get(
            ORDER_CONTROLLER_BASE_PATH + "/123",
        )

        # then
        assert get_order_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_cancel_order(self, test_client):
        # given
        user_id, stock_symbol = populate_user_id_and_stock(test_client)
        sell_order_input_dto = populate_sell_order_dto()
        sell_order_input_dto.user_id = user_id
        sell_order_input_dto.stock_symbol = stock_symbol

        sell_order_response: Response = test_client.post(
            ORDER_CONTROLLER_SELL_PATH,
            data=sell_order_input_dto.json(),
        )
        assert sell_order_response.status_code == status.HTTP_202_ACCEPTED

        sleep(ORDER_WAITING_TIME)
        get_orders_response: Response = test_client.get(
            ORDER_CONTROLLER_BASE_PATH,
        )
        assert get_orders_response.status_code == status.HTTP_200_OK
        get_orders_response_data = get_orders_response.json()
        order_id = GetOrderOutputDto(**get_orders_response_data[0]).id
        assert len(get_orders_response_data) == 1

        # when
        cancel_order_response: Response = test_client.post(
            ORDER_CONTROLLER_CANCEL_PATH,
            data=CancelOrderInputDto(order_id=order_id).json(),
        )

        # then
        assert cancel_order_response.status_code == status.HTTP_202_ACCEPTED

        sleep(ORDER_WAITING_TIME)

        with RepositoryManager() as repository_manager:
            order_entity = (
                repository_manager.query(OrderEntity)
                .filter(OrderEntity.stock_symbol == sell_order_input_dto.stock_symbol)
                .filter(OrderEntity.deleted.is_(False))
                .first()
            )
            assert order_entity is not None
            assert str(order_entity.user_id) == user_id
            assert order_entity.price == sell_order_input_dto.price
            assert order_entity.amount == sell_order_input_dto.amount
            assert order_entity.stock_symbol == sell_order_input_dto.stock_symbol
            assert order_entity.type == OrderTypeEnum.SELL
            assert order_entity.status == OrderStatusEnum.CANCELLED
            assert order_entity.error_code is None
