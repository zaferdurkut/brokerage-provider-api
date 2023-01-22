from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID


class BaseEntity:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    deleted = Column(Boolean, default=False)
