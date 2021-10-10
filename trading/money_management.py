class BaseMoneyManagement:
    def __init__(self, initial_value, tailing_stop=None):
        self.initial_value = initial_value
        self.tailing_stop = tailing_stop

    def compute_stop(self, df):
        self.tailing_stop.compute(df)


class BasicMM(BaseMoneyManagement):
    def __init__(self, initial_value, tailing_stop=None):
        super().__init__(initial_value)
        self.tailing_stop = tailing_stop

    def compute_stop(self, df):
        super().compute_stop(df)
