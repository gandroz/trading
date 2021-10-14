from typing import List, Union
from datetime import date, datetime
import pandas as pd
from trading.order import Order, OrderType
from trading.position import Position
from trading.position_manager import PositionManager
from trading.money_management import BaseMoneyManagement
from trading.plotting import plot
import numpy as np


class BaseStrategy:
    def __init__(self, data_history:pd.DataFrame, money_management:BaseMoneyManagement):
        self.df:pd.DataFrame = data_history
        self.orders:List[Order] = []
        self.positions:List[Position] = [Position()]
        self.position_manager:PositionManager = PositionManager()
        self.mm = money_management

    def buy(self, ticker:str, price:float, date:datetime):
        order = Order(ticker, OrderType.Buy, price, date)
        order.quantity = self.mm.compute_nb_share(order.price)
        self.orders.append(order)
        self.position_manager.add(order)

    def sell(self, ticker:str, price:float, date:datetime):
        order = Order(ticker, OrderType.Sell, price, date)
        self.orders.append(order)
        self.position_manager.add(order)

    def summary(self):
        for ticker in self.position_manager.get_tickers():
            for position in self.position_manager.get_positions(ticker):
                # TODO: complete
                pass

    def simulate(self, tickers:List[str]):
        raise NotImplemented


class TwoEMAStrategy(BaseStrategy):
    def __init__(self, data_history:pd.DataFrame, money_management:BaseMoneyManagement, slow_ema, fast_ema):
        super().__init__(data_history, money_management)
        self.slow_ema = slow_ema
        self.fast_ema = fast_ema

    def simulate(self, tickers:List[str]):
        for ticker in tickers:
            _df = self.df[ticker].copy()
            assert isinstance(_df, pd.DataFrame)

            _df["EMAslow"] = _df.Close.ewm(span=self.slow_ema, adjust=False).mean()
            _df["EMAfast"] = _df.Close.ewm(span=self.fast_ema, adjust=False).mean()

            _df["signal"] = np.where(_df.EMAfast > _df.EMAslow, 1.0, 0.0)
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
            assert isinstance(_df, pd.DataFrame)
            self._compute_order(_df, ticker)

    def _compute_order(self, df:pd.DataFrame, ticker:str):
        # TODO: il faudrait ouvrir et fermer une position a l'ouverture de la prochaine journee
        for _, row in df.iterrows():
            date = row.index
            assert isinstance(date, datetime)
            if row.long:
                self.buy(ticker, row.Open, date)
            if row.short:
                self.sell(ticker, row.Close, date)
