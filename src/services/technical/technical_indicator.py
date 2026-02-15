from src.utils.twelve_data import TwelveData, AssetType
from src.utils.yfinance_data import YFinanceData
from src.utils.charts import TechnicalCharts
from typing import Literal
import pandas as pd

class TechnicalIndicatorService:
    def __init__(self, symbol: str, timezone: str, interval: str, asset_type: AssetType | None = None):
        self.symbol = symbol
        self.timezone = timezone
        self.interval = interval
        self.asset_type = asset_type

    def get_data_from_td(self, **kwargs) -> pd.DataFrame:
        td = TwelveData(
            symbol=self.symbol,
            timezone=self.timezone,
            interval=self.interval,
            asset_type=self.asset_type,
            **kwargs
        )
        return td.get_data_with_ti()

    def get_data_from_yfinance(self, **kwargs) -> pd.DataFrame:
        """Fetch data from yfinance with technical indicators.

        Use this for assets not available on TwelveData:
        - Dollar Index: DX-Y.NYB
        - Treasury Yields: ^TNX (10Y), ^TYX (30Y), ^FVX (5Y)
        - Other indices and ETFs
        """
        yf_data = YFinanceData(
            symbol=self.symbol,
            interval=self.interval,
            timezone=self.timezone,
            asset_type=self.asset_type,
            **kwargs
        )
        return yf_data.get_data_with_ti()

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

    def get_pivot_levels(self, **kwargs) -> dict:
        """Get pivot points calculated from the previous day's OHLC."""
        td = TwelveData(
            symbol=self.symbol,
            timezone=self.timezone,
            interval="1day",
            asset_type=self.asset_type,
            **kwargs
        )
        return td.calculate_pivot_points()

    def get_fibonacci_levels(self, lookback: int = 50, **kwargs) -> dict:
        """Get Fibonacci retracement levels from recent high/low over lookback period."""
        td = TwelveData(
            symbol=self.symbol,
            timezone=self.timezone,
            outputsize=max(lookback + 10, 60),
            interval=self.interval,
            asset_type=self.asset_type,
            **kwargs
        )
        df = td.get_data()
        return td.calculate_fibonacci_levels(df, lookback=lookback)

    def prepare_chart(
            self,
            df: pd.DataFrame,
            size: int,
            analysis_type: Literal["ema", "rsi", "macd", "atr", "bb", "pivot", "fibonacci", "none"],
            pivot_levels: dict = None,
            fibonacci_levels: dict = None,
            ) -> str:
        chart_name = f"{self.symbol}_{self.interval}_{analysis_type}"
        chart = TechnicalCharts(
            symbol=self.symbol,
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
        elif analysis_type == "bb":
            _, encoded_chart = chart.plot_chart(BB=True)
        elif analysis_type == "pivot":
            _, encoded_chart = chart.plot_chart(pivot_levels=pivot_levels)
        elif analysis_type == "fibonacci":
            _, encoded_chart = chart.plot_chart(fibonacci_levels=fibonacci_levels)
        elif analysis_type == "none":
            _, encoded_chart = chart.plot_chart()
        else:
            raise ValueError("Invalid analysis type. Choose 'ema', 'rsi', 'macd', 'atr', 'bb', 'pivot', or 'fibonacci'. or 'normal'.")
        
        return encoded_chart
    
    def prepare_extra_context(
            self,
            df: pd.DataFrame,
            analysis_type: Literal["ema", "rsi", "macd", "atr", "bb", "pivot", "fibonacci", "normal"],
            decimal_places: int = 5,
            pivot_levels: dict = None,
            fibonacci_levels: dict = None,
            ) -> str:
        
        if analysis_type == "ema":
            last_bar = df.iloc[-1]
            values = {
                'EMA20': last_bar['EMA20'].round(decimal_places),
                'EMA50': last_bar['EMA50'].round(decimal_places),
                'EMA100': last_bar['EMA100'].round(decimal_places),
                'Close': last_bar['Close'].round(decimal_places),
            }
            sorted_items = sorted(values.items(), key=lambda x: x[1], reverse=True)
            extra_context = " > ".join([f"{k}: {v}" for k, v in sorted_items])
            return f"Latest Values in descending order:\n{extra_context}"
        elif analysis_type == "rsi":
            last_rsi = df['RSI14'].iloc[-1].round(2)
            return f"RSI14: {last_rsi}"
        elif analysis_type == "macd":
            last_macd = df['MACD'].iloc[-1].round(4)
            last_signal = df['MACD_Signal'].iloc[-1].round(4)
            histogram = df['MACD_Diff'].iloc[-1].round(4)
            return f"MACD: {last_macd}, MACD Signal: {last_signal}, Histogram: {histogram}"
        elif analysis_type == "atr":
            last_atr = df['ATR'].iloc[-1].round(4)
            return f"ATR: {last_atr}"
        elif analysis_type == "bb":
            last_upper = df['BB_Upper'].iloc[-1].round(decimal_places)
            last_middle = df['BB_Middle'].iloc[-1].round(decimal_places)
            last_lower = df['BB_Lower'].iloc[-1].round(decimal_places)
            return f"Bollinger Bands - Upper: {last_upper}, Middle: {last_middle}, Lower: {last_lower}"
        elif analysis_type == "pivot":
            if pivot_levels is None:
                return "No pivot levels provided."
            rounded_levels = {k: round(v, decimal_places) for k, v in pivot_levels.items()}
            levels_str = ", ".join([f"{k}: {v}" for k, v in rounded_levels.items()])
            return f"Pivot Levels\n{levels_str}"
        elif analysis_type == "fibonacci":
            if fibonacci_levels is None:
                return "No Fibonacci levels provided."
            rounded_levels = {k: round(v, decimal_places) for k, v in fibonacci_levels.items()}
            levels_str = ", ".join([f"{k}: {v}" for k, v in rounded_levels.items()])
            return f"Fibonacci Levels\n{levels_str}"
        else:
            return "No extra context for this analysis type."


if __name__ == "__main__":
    size = 80
    analysis_type = "ema"
    asset = "AAPL"
    interval = "1day"
    timezone="Europe/Berlin"

    service = TechnicalIndicatorService(symbol=asset, interval="4h", timezone="Europe/Berlin")
    df = service.get_data_from_td(outputsize=size)
    print(df.tail())

    # Get pivot levels using 1day interval
    # pivot_levels = service.get_pivot_levels(interval="1day")
    # print("Pivot Levels:", pivot_levels)

    # # Get fibonacci levels using 50 period lookback
    # fib_levels = service.get_fibonacci_levels(lookback=50)
    # print("Fibonacci Levels:", fib_levels)

    # # Generate chart with pivot levels
    # service.prepare_chart(
    #     df=df,
    #     size=96,
    #     analysis_type="pivot",
    #     pivot_levels=pivot_levels
    # )

    # service.prepare_chart(
    #     df=df,
    #     size=96,
    #     analysis_type="fibonacci",
    #     fibonacci_levels=fib_levels
    # )

    # service.prepare_chart(
    #     df=df,
    #     size=size,
    #     analysis_type=analysis_type
    # )

    # print(service.prepare_extra_context(
    #     df=df,
    #     analysis_type=analysis_type,
    #     decimal_places=4
    # ))

        
    