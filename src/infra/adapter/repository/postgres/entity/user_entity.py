from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from src.infra.adapter.repository.postgres.entity.base_entity import BaseEntity
from src.infra.adapter.repository.postgres.repository_config import Base


class UserEntity(Base, BaseEntity):
    __tablename__ = "user"
    crm_provider_opportunity_id = Column(String, nullable=True)
    name = Column(String)
    account_name = Column(String)
    type = Column(String)
