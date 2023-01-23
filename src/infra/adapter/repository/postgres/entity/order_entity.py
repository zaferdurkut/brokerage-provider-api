from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.model.base_models.order_status import OrderStatusEnum
from src.infra.adapter.repository.postgres.entity.base_entity import BaseEntity
from src.infra.adapter.repository.postgres.entity.stock_entity import StockEntity
from src.infra.adapter.repository.postgres.entity.user_entity import UserEntity
from src.infra.adapter.repository.postgres.repository_config import Base


class OrderEntity(Base, BaseEntity):
    __tablename__ = "order"
    stock_symbol = Column(String, ForeignKey("stock.symbol"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False, default=OrderStatusEnum.WAITING.value)
    error_code = Column(Integer, nullable=True)

    user = relationship(UserEntity, back_populates="user_orders")
    stock = relationship(StockEntity, back_populates="stock_orders")
