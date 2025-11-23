from src.utils.twelve_data import TwelveData
#from backend.service.IBKRData import IBKRData
from src.utils.charts import TechnicalCharts
from typing import Literal
import pandas as pd

class TechnicalDataService:
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
            return_binary: bool = True
            ) -> bytes:
        chart_name = f"{self.currecy_pair}_{self.interval}_{analysis_type}"
        chart = TechnicalCharts(
            currency_pair=self.currecy_pair,
            interval=self.interval,
            df=df,
            size=size,
            chart_name=chart_name
        )
        if analysis_type == "ema":
            _, binary_data = chart.plot_chart(return_binary=return_binary, EMA20=True, EMA50=True, EMA100=True)
        elif analysis_type == "rsi":
            _, binary_data = chart.plot_chart(return_binary=return_binary, RSI14=True)
        elif analysis_type == "macd":
            _, binary_data = chart.plot_chart(return_binary=return_binary, MACD=True)
        elif analysis_type == "atr":
            _, binary_data = chart.plot_chart(return_binary=return_binary, ATR14=True)
        elif analysis_type == "normal":
            _, binary_data = chart.plot_chart(return_binary=return_binary)
        else:
            raise ValueError("Invalid analysis type. Choose 'ema', 'rsi', 'macd', or 'atr'.")
        
        return binary_data


if __name__ == "__main__":
    pair = "USD/JPY"
    size = 96
    interval = "1h"
    service = TechnicalDataService(currency_pair=pair, interval=interval)
    
    # Example usage:
    data = service.prepare_data(data_source="TwelveData", outputsize=size)
    print(data.head())
    print(data.shape)
    # print(data.tail())
    binary_data = service.prepare_chart(data, size=size, analysis_type="ema", return_binary=True)
    print(binary_data[:100]) 
    print(type(binary_data))  
    


        
    