from typing import cast

from src.core.port.order_event_publish_port import OrderEventPublishPort
from src.core.port.order_repository_port import OrderRepositoryPort
from src.core.port.stock_repository_port import StockRepositoryPort
from src.core.port.user_cache_repository_port import UserCacheRepositoryPort
from src.core.port.user_repository_port import UserRepositoryPort
from src.infra.adapter.producer.kafka.order_producer import OrderEventProducer
from src.infra.adapter.repository.postgres.order_repository import OrderRepository
from src.infra.adapter.repository.postgres.stock_repository import StockRepository
from src.infra.adapter.repository.postgres.user_repository import UserRepository
from src.infra.adapter.repository.redis.user_cache_adapter import UserCacheAdapter


def get_user_repository():
    return cast(UserRepositoryPort, UserRepository())


def get_stock_repository():
    return cast(StockRepositoryPort, StockRepository())


def get_order_repository():
    return cast(OrderRepositoryPort, OrderRepository())


def get_order_event_publisher():
    return cast(OrderEventPublishPort, OrderEventProducer())


def get_user_cache_repository():
    return cast(UserCacheRepositoryPort, UserCacheAdapter())
