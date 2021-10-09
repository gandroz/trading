import yfinance as yf
import pandas as pd


class Data:
    def __init__(self):
        self.df = None
        self.__default_tickers = ["AAPL", "MSFT"]
        self.filename = '/home/guillaume/src/trading/data/stocks.csv'
    
    def download(self, tickers=None, period="5y", interval="1d"):
        _tickers = tickers or self.__default_tickers
        self.df = yf.download(_tickers, period=period, interval=interval, threads=True, group_by='Ticker')

    def save(self, filename=None):
        if self.df is not None:
            _filename = filename or self.filename
            self.df.to_csv(_filename)

    def read(self, filename=None):
        _filename = filename or self.filename
        self.df = pd.read_csv(_filename, header=[0, 1])
        self.df.drop([0], axis=0, inplace=True)  # drop this row because it only has one column with Date in it
        self.df[('Unnamed: 0_level_0', 'Unnamed: 0_level_1')] = pd.to_datetime(self.df[('Unnamed: 0_level_0', 'Unnamed: 0_level_1')], format='%Y-%m-%d')  # convert the first column to a datetime
        self.df.set_index(('Unnamed: 0_level_0', 'Unnamed: 0_level_1'), inplace=True)  # set the first column as the index
        self.df.index.name = "Date"  # rename the index


if __name__ == "__main__":
    data = Data()
    data.download()
    data.save()
