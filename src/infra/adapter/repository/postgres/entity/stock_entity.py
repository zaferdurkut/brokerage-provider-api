from datetime import datetime
from uuid import uuid4

from sqlalchemy import Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Boolean

from src.infra.adapter.repository.postgres.entity.base_entity import BaseEntity
from src.infra.adapter.repository.postgres.repository_config import Base


class StockEntity(Base, BaseEntity):
    __tablename__ = "stock"
    id = Column(UUID(as_uuid=True), default=uuid4)
    amount = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False, primary_key=True)
    first_price = Column(Float, nullable=False)
    price = Column(Float)
    currency = Column(String, nullable=False)

    stock_users = relationship(
        "UserStockEntity",
        back_populates="stock",
    )

    stock_orders = relationship(
        "OrderEntity",
        back_populates="stock",
    )
