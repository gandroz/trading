from pandas import DataFrame


class BaseStop:
    def __init__(self) -> None:
        pass

    def compute(self, df:DataFrame):
        df["stop"] = 0


class MinWindow(BaseStop):
    def __init__(self, window:int, factor:float) -> None:
        super().__init__()
        self.window = window
        self.factor = factor

    def compute(self, df:DataFrame):
        df["stop"] = df.Close.rolling(window=self.window).min() * self.factor
