from typing import Optional, List
from trading.order import Order, OrderType
from dataclasses import dataclass
from datetime import datetime, timedelta


class Position:
    def __init__(self) -> None:
        self._current_quantity:int = 0
        self.orders: List[Order] = []

    @property
    def is_opened(self) -> bool:
        return len(self.orders) > 0 and self._current_quantity > 0

    @property
    def is_closed(self) -> bool:
        return len(self.orders) > 0 and self._current_quantity == 0

    @property
    def profit(self) -> float:
        if not self.is_closed:
            # can be opened of not started
            return 0
        
        pl = 0
        for order in self.orders:
            sign = 2 * int(order.order_type == OrderType.Buy) - 1
            pl += sign * order.price * order.quantity
        return pl

    @property
    def open_time(self) -> datetime:
        # manage case when new position
        return self.orders[0].date

    @property
    def close_time(self) -> datetime:
        # TODO: manage case when position is not closed
        return self.orders[-1].date

    @property
    def duration(self) -> timedelta:
        return self.close_time - self.open_time

    def add_order(self, order:Order) -> None:
        index = 0
        for i, o in enumerate(self.orders):
            # TODO: could use binary search
            if o.date > order.date:
                index = i
                break
        self.orders.insert(index, order)
        self._current_quantity += order.quantity
