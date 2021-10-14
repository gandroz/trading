from pandas import DataFrame
from trading.data import Data
from trading.tailing_stop import BaseStop


class BaseMoneyManagement:
    def __init__(self, initial_value:float, tailing_stop:BaseStop=BaseStop()):
        self.initial_value:float = initial_value
        self.tailing_stop:BaseStop = tailing_stop

    def compute_stop(self, df:DataFrame):
        self.tailing_stop.compute(df)

    def compute_nb_share(self, current_price:float) -> int:
        raise NotImplemented


class BasicMM(BaseMoneyManagement):
    def __init__(self, initial_value:float, tailing_stop:BaseStop=BaseStop()):
        super().__init__(initial_value, tailing_stop)

    def compute_stop(self, df:DataFrame):
        super().compute_stop(df)

    def compute_nb_share(self, current_price:float) -> int:
        raise NotImplemented
