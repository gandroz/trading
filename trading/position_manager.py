from typing import List
from trading.order import Order, OrderType
from trading.position import Position


class PositionManager:
    def __init__(self) -> None:
        self.positions = {}

    def add(self, order:Order) -> None:
        position = self._find_opened_position_for_ticker(order.ticker)
        position.add_order(order)

    def get_positions(self, ticker:str) -> List[Position]:
        return self.positions.get(ticker, [])

    def get_tickers(self) -> List[str]:
        return list(self.positions.keys())

    def _find_opened_position_for_ticker(self, ticker:str) -> Position:
        # find positions for the ticker or crete new position
        if ticker not in self.positions:
            self.positions[ticker] = [Position()]

        # find opened position
        positions = self.positions.get(ticker)
        assert positions is not None

        current_position = None
        for position in positions:
            if position.is_opened:
                current_position = position
                break
        assert current_position is not None

        return current_position
