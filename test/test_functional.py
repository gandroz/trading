from trading.strategy import TwoEMAStrategy
from trading.money_management import BasicMM
from trading.data import Data
from trading.tailing_stop import MinWindow


def test_all():
    initial_value = 1000
    data = Data()
    data.read()
    
    stop = MinWindow(20, 1)
    mm = BasicMM(initial_value, stop)
    strategy = TwoEMAStrategy(data.df, mm, 20, 10)
    strategy.simulate()
    strategy.summary()