from sqlalchemy import Column, ForeignKey, Float, String
from sqlalchemy.dialects.postgresql import UUID
from src.infra.adapter.repository.postgres.entity.base_entity import BaseEntity
from src.infra.adapter.repository.postgres.entity.stock_entity import StockEntity
from src.infra.adapter.repository.postgres.entity.user_entity import UserEntity
from src.infra.adapter.repository.postgres.repository_config import Base
from sqlalchemy.orm import relationship


class UserStockEntity(Base, BaseEntity):
    __tablename__ = "user_stock"
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    stock_symbol = Column(String, ForeignKey("stock.symbol"))
    amount = Column(Float)
    price = Column(Float, nullable=False)

    user = relationship(UserEntity, back_populates="user_stocks")
    stock = relationship(StockEntity, back_populates="stock_users")
