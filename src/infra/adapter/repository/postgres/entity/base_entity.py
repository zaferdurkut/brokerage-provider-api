from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Boolean, Column, DateTime, Integer, String


class BaseEntity:
    id = Column(UUID, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    deleted = Column(Boolean, default=False)
    created_by = Column(String)
    updated_by = Column(String)
