import pandas as pd


class TradeDataManager:
    def __init__(self,trade_data_path="data/trade_data.parquet"):
        self.trade_data_path = trade_data_path
        self._df = None

    @property
    def df(self):
        if self._df is None:
            self._load_data()
        return self._df
    
    def _load_data(self):
        self._df = pd.read_parquet(self.trade_data_path)
        

    