from enum import Enum


class OrderTypeEnum(str, Enum):
    BUY = "buy"
    SELL = "sell"
    CANCEL = "cancel"
