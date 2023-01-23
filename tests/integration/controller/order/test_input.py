from uuid import uuid4

from requests import Response
from starlette import status

from tests.integration.controller.stock.test_constants import STOCK_CONTROLLER_BASE_PATH
from tests.integration.controller.user.test_constants import USER_CONTROLLER_BASE_PATH
from tests.integration.test_input_common import (
    populate_create_stock_dto,
    populate_create_user_dto,
)


def generate_invalid_buy_order_inputs():
    return [
        {"price": 123.33, "stock_symbol": "AAPL", "amount": 100},
        {"user_id": str(uuid4()), "stock_symbol": "AAPL", "amount": 100},
        {"user_id": str(uuid4()), "price": 123.33, "amount": 100},
        {"user_id": str(uuid4()), "price": 123.33, "stock_symbol": "AAPL"},
        {"user_id": "test", "price": 123.33, "stock_symbol": "AAPL", "amount": 100},
        {
            "user_id": str(uuid4()),
            "price": "test",
            "stock_symbol": "AAPL",
            "amount": 100,
        },
        {
            "user_id": str(uuid4()),
            "price": 123.33,
            "stock_symbol": "AAPL",
            "amount": "test",
        },
    ]


def generate_invalid_sell_order_inputs():
    return [
        {"price": 123.33, "stock_symbol": "AAPL", "amount": 100},
        {"user_id": str(uuid4()), "stock_symbol": "AAPL", "amount": 100},
        {"user_id": str(uuid4()), "price": 123.33, "amount": 100},
        {"user_id": str(uuid4()), "price": 123.33, "stock_symbol": "AAPL"},
        {"user_id": "test", "price": 123.33, "stock_symbol": "AAPL", "amount": 100},
        {
            "user_id": str(uuid4()),
            "price": "test",
            "stock_symbol": "AAPL",
            "amount": 100,
        },
        {
            "user_id": str(uuid4()),
            "price": 123.33,
            "stock_symbol": "AAPL",
            "amount": "test",
        },
    ]


def populate_user_id_and_stock(test_client):
    # given
    create_stock_input_dto = populate_create_stock_dto()
    # when
    create_stock_response: Response = test_client.post(
        STOCK_CONTROLLER_BASE_PATH,
        data=create_stock_input_dto.json(),
    )
    assert create_stock_response.status_code == status.HTTP_201_CREATED

    # given
    create_user_input_dto = populate_create_user_dto()
    # when
    create_user_response: Response = test_client.post(
        USER_CONTROLLER_BASE_PATH,
        data=create_user_input_dto.json(),
    )
    assert create_user_response.status_code == status.HTTP_201_CREATED

    return create_user_response.json()["id"], create_stock_input_dto.symbol
