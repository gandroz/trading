from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


class OrderType(Enum):
    Buy = auto()
    Sell = auto()


@dataclass
class Order:
    order_type: OrderType
    price: float
    date: datetime
    quantity: int = 0


class Position:
    def __init__(self):
        self.buy_order:Order = None
        self.sell_order:Order = None
        self._profit:float = None
        self._quantity:int = None
    
    @property
    def is_opened(self):
        return self.buy_order is not None and self.sell_order is None

    @property
    def is_closed(self):
        return self.buy_order is not None and self.sell_order is not None

    @property
    def quantity(self):
        if self._quantity is None:
            if self.buy_order is not None:
                self._quantity = self.buy_order.quantity
        return self._quantity

    @property
    def profit(self):
        if self._profit is None:
            self._profit = self.sell_order.price * self.sell_order.quantity - self.buy_order.price * self.buy_order.quantity
        return self._profit

    @property
    def duration(self):
        return self.sell_order.date - self.buy_order.date

