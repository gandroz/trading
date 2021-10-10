import pandas as pd
from data import Data
from order import Order, OrderType, Position
from money_management import BaseMoneyManagement
from plotting import plot
import numpy as np


class BaseStrategy:
    def __init__(self, data_history:pd.DataFrame, money_management:BaseMoneyManagement):
        self.df = data_history
        self.orders = []
        self.positions = [Position()]
        self.mm = money_management

    def buy(self, price, date):
        self.orders.append(Order(OrderType.Buy, price, date))

    def sell(self, price, date):
        self.orders.append(Order(OrderType.Sell, price, date))

    def _open_position(self, order):
        if self.positions[-1].is_opened:
           # do nothing
           return
        if self.positions[-1].is_closed:
            position = Position()

        order.quantity = self.mm.compute_nb_share(order.price)  # TODO: manage multiple entries with MM - Review logic
        self.positions[-1].buy_order = order
        position.buy_order = order
        self.positions.append(position)

    def _close_position(self, order):
        if self.positions[-1].is_closed:
            # last position already closed
            return
        order.quantity = self.positions[-1].buy_order.quantity
        self.positions[-1].sell_order = order

    def summary(self):
        for order in self.orders:
            if order.order_type == OrderType.Buy:
                self._open_position(order)
            else:
                self._close_position(order)
        

    def simulate(self):
        raise not NotImplemented()


class TwoEMAStrategy(BaseStrategy):
    def __init__(self, data_history:pd.DataFrame, money_management:BaseMoneyManagement, slow_ema, fast_ema):
        super().__init__(data_history, money_management)
        self.slow_ema = slow_ema
        self.fast_ema = fast_ema
        # self.alloc = allocation_percent  # percentage of the current ptf value to risk
        # self.tailing_stop = tailing_stop  # % of min over last x closes
        # TODO: define class for tailing stops
        # TODO: define class for money management

    def simulate(self):
        _df = self.df.copy()

        _df["EMAslow"] = _df.Close.ewm(span=self.slow_ema, adjust=False).mean()
        _df["EMAfast"] = _df.Close.ewm(span=self.fast_ema, adjust=False).mean()

        _df["signal"] = np.where(_df["EMAfast"] > _df["EMAslow"], 1.0, 0.0)
        _df["signal"] = _df.signal.diff()  # +1 for buy signal and -1 for sell signal

        # compute stop in money management.
        self.mm.compute_stop(_df)

        _df["long"] = _df.signal > 0
        _df["short"] = (_df.signal < 0)|(_df.Close <= _df.stop)
        _df = _df[(_df.long)|(_df.short)]

        counter = -1  # we want to start with a long position
        idx_to_remove = []
        for index, row in _df.iterrows():
            if row.short and counter == -1:
                idx_to_remove.append(index)
            elif row.long and counter == 1:
                idx_to_remove.append(index)
            else:
                counter *= -1
        _df.drop(idx_to_remove, inplace=True)
        self._compute_order(_df)

    def _compute_order(self, df):
        # TODO: il faudrait ouvrir et fermer une position a l'ouverture de la prochaine journee

        for _, row in df.iterrows():
            if row.long:
                self.buy(row.Open, row.index)
            if row.short:
                self.sell(row.Close, row.index)


if __name__ == "__main__":
    data = Data()
    data.read()
    strategy = TwoEMAStrategy(1000, data.df["AAPL"], 20, 10)
    strategy.simulate()
