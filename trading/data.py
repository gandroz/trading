from typing import List, Union, Optional
import yfinance as yf
import pandas as pd


class Data:
    def __init__(self):
        self.__default_tickers:List = ["AAPL", "MSFT"]
        self.filename:str = '/home/guillaume/src/trading/data/stocks.csv'

    def download(self, tickers:Union[List[str], str]=None, period:str="5y", interval:str="1d") -> pd.DataFrame:
        _tickers = tickers or self.__default_tickers
        return yf.download(_tickers, period=period, interval=interval, threads=True, group_by='Ticker')

    def save(self, df:pd.DataFrame, filename:str=None) -> None:
        assert df is not None
        _filename = filename or self.filename
        df.to_csv(_filename)

    def read(self, filename:str=None) -> pd.DataFrame:
        _filename = filename or self.filename
        _df = pd.read_csv(_filename, header=[0, 1])
        _df.drop([0], axis=0, inplace=True)  # drop this row because it only has one column with Date in it
        _df[('Unnamed: 0_level_0', 'Unnamed: 0_level_1')] = pd.to_datetime(_df[('Unnamed: 0_level_0', 'Unnamed: 0_level_1')], format='%Y-%m-%d')  # convert the first column to a datetime
        _df.set_index(('Unnamed: 0_level_0', 'Unnamed: 0_level_1'), inplace=True)  # set the first column as the index
        _df.index.name = "Date"  # rename the index
        return _df
