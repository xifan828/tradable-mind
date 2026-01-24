"""Data service for fetching market data from TwelveData."""

import os
import pandas as pd
import streamlit as st
from twelvedata import TDClient
from dotenv import load_dotenv


class ChartDataService:
    """Service for fetching and caching chart data from TwelveData."""

    SUPPORTED_INTERVALS = [
        "1min", "5min", "15min", "30min", "45min",
        "1h", "2h", "4h", "1day", "1week", "1month"
    ]

    def __init__(self):
        """Initialize the data service with TwelveData API key from environment."""
        load_dotenv()
        api_key = os.getenv("TD_API_KEY")
        if not api_key:
            raise ValueError("TD_API_KEY not found in environment variables")
        self.api_key = api_key
        self.client = TDClient(apikey=api_key)

    def fetch_ohlc_data(
        self,
        symbol: str,
        interval: str,
        outputsize: int = 200,
        timezone: str = "UTC"
    ) -> pd.DataFrame | None:
        """
        Fetch OHLC data with technical indicators.

        Args:
            symbol: Trading symbol (e.g., "EUR/USD", "AAPL")
            interval: Time interval (e.g., "1h", "4h", "1day")
            outputsize: Number of data points to fetch
            timezone: Timezone for the data

        Returns:
            DataFrame with OHLC + indicators or None if error
        """
        try:
            ts = self.client.time_series(
                symbol=symbol,
                interval=interval,
                outputsize=outputsize,
                timezone=timezone,
            )

            df = (
                ts
                .with_ema(time_period=10)
                .with_ema(time_period=20)
                .with_ema(time_period=50)
                .with_ema(time_period=100)
                .with_bbands(ma_type="SMA", sd=2, series_type="close", time_period=20)
                .with_macd(fast_period=12, series_type="close", signal_period=9, slow_period=26)
                .with_rsi(time_period=14)
                .with_atr(time_period=14)
                .with_roc(time_period=12)
                .as_pandas()
            )

            # Reverse to oldest-first order
            df = df[::-1].reset_index()

            # Rename columns
            df = df.rename(columns={
                "datetime": "Date",
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "ema1": "EMA10",
                "ema2": "EMA20",
                "ema3": "EMA50",
                "ema4": "EMA100",
                "upper_band": "BB_Upper",
                "middle_band": "BB_Middle",
                "lower_band": "BB_Lower",
                "macd": "MACD",
                "macd_signal": "MACD_Signal",
                "macd_hist": "MACD_Hist",
                "rsi": "RSI",
                "atr": "ATR",
                "roc": "ROC",
            })

            return df

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return None

    def fetch_ohlcv_data(
        self,
        symbol: str,
        interval: str,
        outputsize: int = 200,
        timezone: str = "UTC"
    ) -> pd.DataFrame | None:
        """
        Fetch OHLCV data (with volume) and technical indicators.

        Args:
            symbol: Trading symbol
            interval: Time interval
            outputsize: Number of data points
            timezone: Timezone

        Returns:
            DataFrame with OHLCV + indicators or None if error
        """
        try:
            # First try to get data with volume
            ts = self.client.time_series(
                symbol=symbol,
                interval=interval,
                outputsize=outputsize,
                timezone=timezone,
            )

            # Build with indicators
            ts_with_indicators = (
                ts
                .with_ema(time_period=10)
                .with_ema(time_period=20)
                .with_ema(time_period=50)
                .with_ema(time_period=100)
                .with_bbands(ma_type="SMA", sd=2, series_type="close", time_period=20)
                .with_macd(fast_period=12, series_type="close", signal_period=9, slow_period=26)
                .with_rsi(time_period=14)
                .with_atr(time_period=14)
                .with_roc(time_period=12)
            )

            df = ts_with_indicators.as_pandas()

            # Reverse to oldest-first order
            df = df[::-1].reset_index()

            # Check if volume exists
            has_volume = "volume" in df.columns

            # Build rename dict
            rename_dict = {
                "datetime": "Date",
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "ema1": "EMA10",
                "ema2": "EMA20",
                "ema3": "EMA50",
                "ema4": "EMA100",
                "upper_band": "BB_Upper",
                "middle_band": "BB_Middle",
                "lower_band": "BB_Lower",
                "macd": "MACD",
                "macd_signal": "MACD_Signal",
                "macd_hist": "MACD_Hist",
                "rsi": "RSI",
                "atr": "ATR",
                "roc": "ROC",
            }

            if has_volume:
                rename_dict["volume"] = "Volume"

            df = df.rename(columns=rename_dict)

            return df

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return None

    def calculate_pivot_points(self, df: pd.DataFrame) -> dict | None:
        """
        Calculate standard pivot points from the previous period's OHLC.

        Args:
            df: DataFrame with High, Low, Close columns

        Returns:
            Dictionary with Pivot, R1-R3, S1-S3 levels
        """
        if df is None or len(df) < 2:
            return None

        try:
            high = df["High"].iloc[-2]
            low = df["Low"].iloc[-2]
            close = df["Close"].iloc[-2]

            pivot = (high + low + close) / 3

            return {
                "Pivot": pivot,
                "R1": (2 * pivot) - low,
                "R2": pivot + (high - low),
                "R3": high + 2 * (pivot - low),
                "S1": (2 * pivot) - high,
                "S2": pivot - (high - low),
                "S3": low - 2 * (high - pivot),
            }
        except Exception:
            return None

@st.cache_data(ttl=300, show_spinner=False)
def fetch_cached_data(
    symbol: str,
    interval: str,
    outputsize: int = 200
) -> pd.DataFrame | None:
    """
    Cached wrapper for fetching OHLCV data.

    Data is cached for 5 minutes to avoid excessive API calls.
    """
    service = ChartDataService()
    return service.fetch_ohlcv_data(symbol, interval, outputsize)


@st.cache_data(ttl=300, show_spinner=False)
def fetch_daily_change(symbol: str) -> dict | None:
    """
    Fetch daily change data for a symbol.

    Returns:
        Dictionary with 'change' and 'change_pct' or None if error
    """
    try:
        load_dotenv()
        api_key = os.getenv("TD_API_KEY")
        if not api_key:
            return None

        client = TDClient(apikey=api_key)
        ts = client.time_series(
            symbol=symbol,
            interval="1day",
            outputsize=2,
            timezone="UTC",
        )
        df = ts.as_pandas()

        if df is None or len(df) < 2:
            return None

        # df is newest-first from API
        current_close = df.iloc[0]["close"]
        prev_close = df.iloc[1]["close"]

        change = current_close - prev_close
        change_pct = (change / prev_close) * 100

        return {
            "change": change,
            "change_pct": change_pct,
        }
    except Exception:
        return None
