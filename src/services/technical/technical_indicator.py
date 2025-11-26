from src.utils.twelve_data import TwelveData
#from backend.service.IBKRData import IBKRData
from src.utils.charts import TechnicalCharts
from typing import Literal
import pandas as pd

class TechnicalIndicatorService:
    def __init__(self, currency_pair: str, interval: str):
        self.currecy_pair = currency_pair
        self.interval = interval

    def get_data_from_td(self, **kwargs) -> pd.DataFrame:
        if self.currecy_pair == "BTC/USD":
            exchange = "Coinbase Pro"
        else:
            exchange = "OANDA"

        td = TwelveData(
            currency_pair=self.currecy_pair,
            interval=self.interval,
            exchange=exchange,
            **kwargs
        )
        return td.get_data_with_ti()
    
    # def get_data_from_ibkr(self) -> pd.DataFrame:
    #     ibkr = IBKRData(
    #         currency_pair=self.currecy_pair,
    #         interval=self.interval
    #     )
    #     return ibkr.get_data()
    
    def prepare_data(self, data_source: Literal["TwelveData", "IBKR"], **kwargs) -> pd.DataFrame:
        if data_source == "TwelveData":
            data = self.get_data_from_td(**kwargs)
        # elif data_source == "IBKR":
        #     data = self.get_data_from_ibkr()
        else:
            raise ValueError("Invalid data source. Choose 'TwelveData' or 'IBKR'.")
        
        if data is None or data.empty:
            raise ValueError("No data returned from the source.")
        
        return data
    
    def prepare_chart(
            self, 
            df: pd.DataFrame, 
            size: int, 
            analysis_type: Literal["ema", "rsi", "macd", "atr"],
            ) -> str:
        chart_name = f"{self.currecy_pair}_{self.interval}_{analysis_type}"
        chart = TechnicalCharts(
            currency_pair=self.currecy_pair,
            interval=self.interval,
            df=df,
            size=size,
            chart_name=chart_name
        )
        if analysis_type == "ema":
            _, encoded_chart = chart.plot_chart(EMA20=True, EMA50=True, EMA100=True)
        elif analysis_type == "rsi":
            _, encoded_chart = chart.plot_chart(RSI14=True)
        elif analysis_type == "macd":
            _, encoded_chart = chart.plot_chart(MACD=True)
        elif analysis_type == "atr":
            _, encoded_chart = chart.plot_chart(ATR14=True)
        elif analysis_type == "normal":
            _, encoded_chart = chart.plot_chart()
        else:
            raise ValueError("Invalid analysis type. Choose 'ema', 'rsi', 'macd', or 'atr'.")
        
        return encoded_chart




        
    