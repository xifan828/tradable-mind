from twelvedata import TDClient
import pandas as pd
import os
from dotenv import load_dotenv
import asyncio

class TwelveData:

    def __init__(self, currency_pair: str, interval: str, outputsize: int = 400, exchange: str = "OANDA", start_date: str = None, end_date: str = None, timezone: str = "UTC"):
        self.currency_pair = currency_pair
        self.interval = interval
        self.outputsize = outputsize
        self.exchange = exchange
        self.start_date = start_date
        self.end_date = end_date
        self.timezone = timezone
        load_dotenv()
        self._init_client()

    def _init_client(self):
        api_key = os.getenv("TD_API_KEY", None)
        if not api_key:
            raise ValueError("API key for TwelveData is not set in environment variables.")
        self.client = TDClient(apikey=api_key)
    
    async def aget_data(self) -> pd.DataFrame:
        """Async wrapper for get_data to avoid blocking the event loop"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_data)
    
    async def aget_data_with_ti(self) -> pd.DataFrame:
        """Async wrapper for get_data_with_ti to avoid blocking the event loop"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_data_with_ti)
    
    def get_data(self) -> pd.DataFrame:
        try:
            if self.start_date and self.end_date:
                data = self.client.time_series(
                    symbol=self.currency_pair,
                    interval=self.interval,
                    start_date=self.start_date,
                    end_date=self.end_date,
                    exchange=self.exchange
                ).as_pandas()
            else:
                data = self.client.time_series(
                    symbol=self.currency_pair,
                    interval=self.interval,
                    outputsize=self.outputsize,
                    exchange=self.exchange
                ).as_pandas()
            data.columns = ["Open", "High", "Low", "Close"]
            return data[::-1]
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def get_data_with_ti(self) -> pd.DataFrame:
        ts = self.client.time_series(
            symbol=self.currency_pair,
            interval=self.interval,
            outputsize=self.outputsize,
            exchange=self.exchange,
            timezone=self.timezone
        )
        df = (
            ts
            .with_ema(time_period=10)
            .with_ema(time_period=20)
            .with_ema(time_period=50)
            .with_ema(time_period=100)
        # .with_bbands(ma_type="SMA", sd=2, series_type="close", time_period=20)
            .with_macd(fast_period=12, series_type="close", signal_period=9, slow_period=26)
            .with_rsi(time_period=14)
            .with_atr(time_period=14)
            .with_roc(time_period=12)
        # .with_roc(time_period=12)
            .as_pandas()
        )
        df = df[::-1]
        df = df.reset_index()
        #df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # rename columns
        df = df.rename(columns={
            "datetime": "Date",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            'ema1': 'EMA10',
            'ema2': 'EMA20',
            'ema3': 'EMA50',
            'ema4': 'EMA100',
            "macd": "MACD",
            "macd_signal": "MACD_Signal",
            "macd_hist": "MACD_Diff",
            "rsi": "RSI14",
            "atr": "ATR",
            "roc": "ROC12"
        })

        return df

    

if __name__ == "__main__":
    # Example usage
    # td = TwelveData(currency_pair="GBP/USD", interval="1h", outputsize=200, exchange="OANDA")
    # data = td.get_data()
    # print("head")
    # print(data.head())
    # print("tail")
    # print(data.tail())
    td = TwelveData(currency_pair="BTC/USD", interval="1h", outputsize=10, exchange="Coinbase Pro")
    data = td.get_data_with_ti()
    print(data.head(20))
    print(data.info())
