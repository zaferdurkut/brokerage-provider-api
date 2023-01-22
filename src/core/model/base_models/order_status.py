from enum import Enum


class OrderStatusEnum(str, Enum):
    COMPLETED = "completed"
    WAITING = "waiting"
    CANCELLED = "cancelled"
    FAILED = "failed"
