from enum import Enum


class UserTypeEnum(str, Enum):
    NORMAL = "normal"
    MANAGER = "manager"
    BROKER = "broker"
