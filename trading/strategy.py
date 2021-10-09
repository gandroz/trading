from data import Data
from plotting import plot
import numpy as np


class BaseStrategy:
    def __init__(self, initial_value, data_history):
        self.initial_value = initial_value
        self.df = data_history

    def buy(self):
        pass

    def sell(self):
        pass

    def simulate(self):
        pass


class TwoEMAStrategy(BaseStrategy):
    def __init__(self, initial_value, data_history, slow_ema, fast_ema, allocation_percent, 
                 tailing_stop=None):
        super().__init__(initial_value, data_history)
        self.slow_ema = slow_ema
        self.fast_ema = fast_ema
        self.alloc = allocation_percent  # percentage of the current ptf value to risk
        self.tailing_stop = tailing_stop  # % of min over last x closes
        # TODO: define class for tailing stops
        # TODO: define class for money management

    def simulate(self):
        _df = self.df.copy()

        _df["EMAslow"] = _df.Close.ewm(span=self.slow_ema, adjust=False).mean()
        _df["EMAfast"] = _df.Close.ewm(span=self.fast_ema, adjust=False).mean()

        _df["signal"] = np.where(_df["EMAfast"] > _df["EMAslow"], 1.0, 0.0)
        _df["signal"] = _df.signal.diff()  # +1 for buy signal and -1 for sell signal

        _df["stop"] = _df.Close.rolling(window=20).min() * self.tailing_stop / 100

        _long = _df.Close[_df.signal > 0].index
        _short = _df.Close[(_df.signal < 0)|(_df.Close <= _df.stop)].index

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
        res = self._compute_positions(_df)
        print(f"Final value: {res}")

    def _compute_positions(self, df):
        # TODO: il faudrait ouvrir et fermer une position a l'ouverture de la prochaine journee
        value = self.initial_value
        nb_shares = 0
        history = []  # build history

        for index, row in df.iterrows():
            if row.long:
                nb_shares = int(value*self.alloc / row.Close)
                price = row.Open
            if row.short:
                pl = nb_shares * row.Close
                value += pl
            
        return value


if __name__ == "__main__":
    data = Data()
    data.read()
    strategy = TwoEMAStrategy(1000, data.df["AAPL"], 20, 10, 100, tailing_stop=100)
    strategy.simulate()
