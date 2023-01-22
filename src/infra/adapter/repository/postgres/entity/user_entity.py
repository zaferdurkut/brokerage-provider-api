from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship

from src.infra.adapter.repository.postgres.entity.base_entity import BaseEntity
from src.infra.adapter.repository.postgres.repository_config import Base


class UserEntity(Base, BaseEntity):
    __tablename__ = "user"
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    balance = Column(Float(precision=16), nullable=True)
    type = Column(String, nullable=False)

    user_stocks = relationship(
        "UserStockEntity",
        back_populates="user",
    )

    user_orders = relationship(
        "OrderEntity",
        back_populates="user",
    )
