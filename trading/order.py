from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


class OrderType(Enum):
    Buy = auto()
    Sell = auto()


@dataclass
class Order:
    ticker:str
    order_type: OrderType
    price: float
    date: datetime
    quantity: int = 0
