from uuid import uuid4

from requests import Response

from src.api.controller.order.dto.buy_order_input_dto import BuyOrderInputDto
from src.api.controller.order.dto.sell_order_input_dto import SellOrderInputDto
from src.api.controller.stock.dto.create_stock_input_dto import CreateStockInputDto
from src.api.controller.user.dto.create_user_input_dto import CreateUserInputDto
from src.infra.adapter.repository.postgres.entity import OrderEntity, UserStockEntity
from src.infra.adapter.repository.postgres.entity.stock_entity import StockEntity
from src.infra.adapter.repository.postgres.entity.user_entity import UserEntity
from src.infra.adapter.repository.postgres.repository_manager import RepositoryManager


def delete_all_tables():
    with RepositoryManager() as repository_manager:
        repository_manager.query(OrderEntity).delete()
        repository_manager.query(UserStockEntity).delete()
        repository_manager.query(StockEntity).delete()
        repository_manager.query(UserEntity).delete()
        repository_manager.commit()


def populate_create_user_dto():
    return CreateUserInputDto(
        name="test", surname="test", email="test@test.com", balance=10000
    )


def populate_create_stock_dto():
    return CreateStockInputDto(
        name="Apple", symbol="AAPL", first_price=150.1, currency="USD", amount=100
    )


def populate_buy_order_dto():
    return BuyOrderInputDto(user_id=uuid4(), price=100, amount=15, stock_symbol="AAPL")


def populate_sell_order_dto():
    return SellOrderInputDto(user_id=uuid4(), price=100, amount=5, stock_symbol="AAPL")
