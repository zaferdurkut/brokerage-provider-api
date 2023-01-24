from time import sleep
from uuid import uuid4

import pytest
from requests import Response
from starlette import status

from src.api.controller.order.dto.get_order_output_dto import GetOrderOutputDto
from src.core.model.base_models.order_status import OrderStatusEnum
from src.core.model.base_models.order_type import OrderTypeEnum
from src.core.model.order.buy_order_input_model import BuyOrderInputModel
from src.core.model.order.cancel_order_input_model import CancelOrderInputModel
from src.core.model.order.order_result_output_model import (
    OrderRepositoryResultOutputModel,
)
from src.core.model.order.sell_order_input_model import SellOrderInputModel
from src.infra.adapter.repository.postgres.entity import OrderEntity
from src.infra.adapter.repository.postgres.repository_manager import RepositoryManager
from tests.integration.controller.order.test_constants import (
    ORDER_CONTROLLER_SELL_PATH,
    ORDER_CONTROLLER_BASE_PATH,
    ORDER_WAITING_TIME,
)
from tests.integration.controller.order.test_input import (
    populate_user_id_and_stock,
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


class TestOrderRepositoryPostgresAdapter:
    def test_should_buy_order(self, test_client, order_repository_postgres_adapter):
        # given
        user_id, stock_symbol = populate_user_id_and_stock(test_client)
        buy_order_input_dto = populate_buy_order_dto()
        buy_order_input_dto.user_id = user_id
        buy_order_input_dto.stock_symbol = stock_symbol

        # when

        buy_order_output_model: OrderRepositoryResultOutputModel = (
            order_repository_postgres_adapter.buy_order(
                buy_order_input_model=BuyOrderInputModel(**buy_order_input_dto.dict())
            )
        )

        # then
        assert buy_order_output_model.error_code is None
        assert buy_order_output_model.status == OrderStatusEnum.WAITING

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

        # given
        buy_order_input_dto.amount = 100000

        # when
        buy_order_output_model: OrderRepositoryResultOutputModel = (
            order_repository_postgres_adapter.buy_order(
                buy_order_input_model=BuyOrderInputModel(**buy_order_input_dto.dict())
            )
        )

        # then
        assert buy_order_output_model.error_code == 2006
        assert buy_order_output_model.status == OrderStatusEnum.FAILED

    def test_should_sell_order(self, test_client, order_repository_postgres_adapter):
        # given
        user_id, stock_symbol = populate_user_id_and_stock(test_client)
        sell_order_input_dto = populate_sell_order_dto()
        sell_order_input_dto.user_id = user_id
        sell_order_input_dto.stock_symbol = stock_symbol

        # when
        sell_order_output_model: OrderRepositoryResultOutputModel = (
            order_repository_postgres_adapter.sell_order(
                sell_order_input_model=SellOrderInputModel(
                    **sell_order_input_dto.dict()
                )
            )
        )

        # then
        assert sell_order_output_model.error_code is None
        assert sell_order_output_model.status == OrderStatusEnum.WAITING

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

        # given
        sell_order_input_dto.amount = 55

        # when
        sell_order_output_model: OrderRepositoryResultOutputModel = (
            order_repository_postgres_adapter.sell_order(
                sell_order_input_model=SellOrderInputModel(
                    **sell_order_input_dto.dict()
                )
            )
        )

        # then
        assert sell_order_output_model.error_code == 2007
        assert sell_order_output_model.status == OrderStatusEnum.FAILED

    def test_should_cancel_order(self, test_client, order_repository_postgres_adapter):
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
        cancel_order_output_model: OrderRepositoryResultOutputModel = (
            order_repository_postgres_adapter.cancel_order(
                cancel_order_input_model=CancelOrderInputModel(order_id=order_id)
            )
        )

        # then
        assert cancel_order_output_model.error_code is None
        assert cancel_order_output_model.status == OrderStatusEnum.CANCELLED

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

        # when
        cancel_order_output_model: OrderRepositoryResultOutputModel = (
            order_repository_postgres_adapter.cancel_order(
                cancel_order_input_model=CancelOrderInputModel(order_id=order_id)
            )
        )

        # then
        assert cancel_order_output_model.error_code == 2014
        assert cancel_order_output_model.status == OrderStatusEnum.CANCELLED

        # when
        cancel_order_output_model: OrderRepositoryResultOutputModel = (
            order_repository_postgres_adapter.cancel_order(
                cancel_order_input_model=CancelOrderInputModel(order_id=uuid4())
            )
        )

        # then
        assert cancel_order_output_model.error_code == 2011
        assert cancel_order_output_model.status == OrderStatusEnum.CANCELLED
