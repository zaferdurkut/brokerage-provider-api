from typing import cast

from src.core.port.order_event_publish_port import OrderEventPublishPort
from src.core.port.user_repository_port import UserRepositoryPort
from src.infra.adapter.producer.kafka.order_producer import OrderEventProducer
from src.infra.adapter.repository.postgres.user_repository import UserRepository


def get_user_repository():
    return cast(UserRepositoryPort, UserRepository())


def get_order_event_publisher():
    return cast(OrderEventPublishPort, OrderEventProducer())
