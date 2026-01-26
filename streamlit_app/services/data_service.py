"""Data service for fetching market data - thin wrapper around TwelveData with Streamlit caching."""

import pandas as pd
import streamlit as st

from src.utils.twelve_data import TwelveData, AssetType


@st.cache_data(ttl=300, show_spinner=False)
def fetch_cached_data(
    symbol: str,
    interval: str,
    outputsize: int = 200,
    asset_type: AssetType = None
) -> pd.DataFrame | None:
    """
    Cached wrapper for fetching OHLCV data with technical indicators.

    Uses TwelveData class with Streamlit caching (5 minute TTL).
    """
    try:
        td = TwelveData(
            symbol=symbol,
            interval=interval,
            outputsize=outputsize,
            asset_type=asset_type
        )
        return td.get_data_with_ti()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None


@st.cache_data(ttl=300, show_spinner=False)
def fetch_daily_change(symbol: str, asset_type: AssetType = None) -> dict | None:
    """
    Fetch daily change data for a symbol.

    Uses TwelveData class to ensure weekend filtering for forex/commodity.

    Returns:
        Dictionary with 'change' and 'change_pct' or None if error
    """
    try:
        # Fetch enough daily bars to get 2 valid trading days after filtering
        td = TwelveData(
            symbol=symbol,
            interval="1day",
            outputsize=5,  # Extra bars to account for weekend filtering
            asset_type=asset_type
        )
        df = td.get_data()

        if df is None or len(df) < 2:
            return None

        # df is oldest-first after TwelveData processing
        current_close = df["Close"].iloc[-1]
        prev_close = df["Close"].iloc[-2]

        change = current_close - prev_close
        change_pct = (change / prev_close) * 100

        return {
            "change": change,
            "change_pct": change_pct,
        }
    except Exception:
        return None


@st.cache_data(ttl=300, show_spinner=False)
def fetch_pivot_points(symbol: str, asset_type: AssetType = None) -> dict | None:
    """
    Fetch pivot points calculated from daily data.

    Always uses daily OHLC regardless of chart interval.
    Uses TwelveData's calculate_pivot_points method.

    Args:
        symbol: Trading symbol
        asset_type: Asset type for weekend filtering

    Returns:
        Dictionary with Pivot, R1-R3, S1-S3 levels or None if error
    """
    try:
        td = TwelveData(
            symbol=symbol,
            interval="1day",  # Interval doesn't matter, calculate_pivot_points fetches daily
            asset_type=asset_type
        )
        return td.calculate_pivot_points()
    except Exception:
        return None
