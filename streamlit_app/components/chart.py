"""Plotly candlestick chart component with technical indicators."""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from streamlit_app.utils.styles import CHART_COLORS


def filter_weekend_data(df: pd.DataFrame, interval: str) -> pd.DataFrame:
    """Filter out weekend data (Saturday and Sunday) from the DataFrame."""
    if df is None or df.empty:
        return df

    # Ensure Date column is datetime
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # Filter out Saturday (5) and Sunday (6)
    mask = df["Date"].dt.dayofweek < 5
    df = df[mask].reset_index(drop=True)

    # Format date labels based on interval
    if interval in ["1day", "1week", "1month"]:
        df["DateLabel"] = df["Date"].dt.strftime("%b %d")
    else:
        # Intraday intervals - show date and time
        df["DateLabel"] = df["Date"].dt.strftime("%b %d %H:%M")

    return df


def create_candlestick_chart(
    df: pd.DataFrame,
    symbol: str,
    interval: str,
    indicators: dict,
    pivot_levels: dict | None = None,
) -> go.Figure:
    """
    Create an interactive Plotly candlestick chart with technical indicators.

    Args:
        df: DataFrame with OHLC data and indicators
        symbol: Trading symbol for title
        interval: Time interval for title
        indicators: Dict of indicator toggles (e.g., {"ema_20": True, "rsi": True})
        pivot_levels: Optional pivot point levels

    Returns:
        Plotly Figure object
    """
    # Filter out weekend data and format labels
    df = filter_weekend_data(df, interval)

    # Determine subplot configuration
    subplot_indicators = []
    has_volume = "Volume" in df.columns and df["Volume"].notna().any()

    if has_volume and indicators.get("volume", True):
        subplot_indicators.append("Volume")
    if indicators.get("rsi"):
        subplot_indicators.append("RSI")
    if indicators.get("macd"):
        subplot_indicators.append("MACD")
    if indicators.get("atr"):
        subplot_indicators.append("ATR")

    num_rows = 1 + len(subplot_indicators)

    # Calculate row heights - main chart gets more space
    if num_rows == 1:
        row_heights = [1.0]
    else:
        main_height = 0.6
        subplot_height = (1 - main_height) / len(subplot_indicators)
        row_heights = [main_height] + [subplot_height] * len(subplot_indicators)

    # Create subplots
    fig = make_subplots(
        rows=num_rows,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=row_heights,
        subplot_titles=[f"{symbol} ({interval})"] + subplot_indicators,
    )

    # === Main Candlestick Chart (Row 1) ===
    fig.add_trace(
        go.Candlestick(
            x=df["DateLabel"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="OHLC",
            increasing_line_color=CHART_COLORS["candle_up"],
            decreasing_line_color=CHART_COLORS["candle_down"],
            increasing_fillcolor=CHART_COLORS["candle_up"],
            decreasing_fillcolor=CHART_COLORS["candle_down"],
        ),
        row=1, col=1
    )

    # === EMA Overlays ===
    ema_configs = [
        ("ema_10", "EMA10", CHART_COLORS["ema_10"], 1),
        ("ema_20", "EMA20", CHART_COLORS["ema_20"], 1),
        ("ema_50", "EMA50", CHART_COLORS["ema_50"], 1.5),
        ("ema_100", "EMA100", CHART_COLORS["ema_100"], 1.5),
    ]

    for key, col, color, width in ema_configs:
        if indicators.get(key) and col in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df["DateLabel"],
                    y=df[col],
                    name=col,
                    line=dict(color=color, width=width),
                    hovertemplate=f"{col}: %{{y:.4f}}<extra></extra>",
                ),
                row=1, col=1
            )

    # === Bollinger Bands ===
    if indicators.get("bb") and "BB_Upper" in df.columns:
        # Upper band
        fig.add_trace(
            go.Scatter(
                x=df["DateLabel"],
                y=df["BB_Upper"],
                name="BB Upper",
                line=dict(color=CHART_COLORS["bb_band"], width=1, dash="dash"),
                hovertemplate="BB Upper: %{y:.4f}<extra></extra>",
            ),
            row=1, col=1
        )
        # Lower band
        fig.add_trace(
            go.Scatter(
                x=df["DateLabel"],
                y=df["BB_Lower"],
                name="BB Lower",
                line=dict(color=CHART_COLORS["bb_band"], width=1, dash="dash"),
                fill="tonexty",
                fillcolor="rgba(96, 125, 139, 0.1)",
                hovertemplate="BB Lower: %{y:.4f}<extra></extra>",
            ),
            row=1, col=1
        )
        # Middle band (SMA)
        fig.add_trace(
            go.Scatter(
                x=df["DateLabel"],
                y=df["BB_Middle"],
                name="BB Middle",
                line=dict(color=CHART_COLORS["bb_middle"], width=1),
                hovertemplate="BB Middle: %{y:.4f}<extra></extra>",
            ),
            row=1, col=1
        )

    # === Pivot Points ===
    # Pivot values are displayed in the header area (app.py) when enabled

    # === Subplot Indicators ===
    current_row = 2

    # Volume
    if "Volume" in subplot_indicators:
        colors = [
            CHART_COLORS["volume_up"] if close >= open_
            else CHART_COLORS["volume_down"]
            for close, open_ in zip(df["Close"], df["Open"])
        ]
        fig.add_trace(
            go.Bar(
                x=df["DateLabel"],
                y=df["Volume"],
                name="Volume",
                marker_color=colors,
                hovertemplate="Volume: %{y:,.0f}<extra></extra>",
            ),
            row=current_row, col=1
        )
        current_row += 1

    # RSI
    if "RSI" in subplot_indicators and "RSI" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["DateLabel"],
                y=df["RSI"],
                name="RSI(14)",
                line=dict(color=CHART_COLORS["rsi"], width=1.5),
                hovertemplate="RSI: %{y:.2f}<extra></extra>",
            ),
            row=current_row, col=1
        )
        # Overbought/Oversold lines
        fig.add_hline(y=70, line=dict(color=CHART_COLORS["rsi_overbought"], width=1, dash="dash"), row=current_row, col=1)
        fig.add_hline(y=30, line=dict(color=CHART_COLORS["rsi_oversold"], width=1, dash="dash"), row=current_row, col=1)
        fig.add_hline(y=50, line=dict(color="#404040", width=1, dash="dot"), row=current_row, col=1)

        # Update RSI y-axis range
        fig.update_yaxes(range=[0, 100], row=current_row, col=1)
        current_row += 1

    # MACD
    if "MACD" in subplot_indicators and "MACD" in df.columns:
        # MACD line
        fig.add_trace(
            go.Scatter(
                x=df["DateLabel"],
                y=df["MACD"],
                name="MACD",
                line=dict(color=CHART_COLORS["macd_line"], width=1.5),
                hovertemplate="MACD: %{y:.4f}<extra></extra>",
            ),
            row=current_row, col=1
        )
        # Signal line
        fig.add_trace(
            go.Scatter(
                x=df["DateLabel"],
                y=df["MACD_Signal"],
                name="Signal",
                line=dict(color=CHART_COLORS["macd_signal"], width=1.5),
                hovertemplate="Signal: %{y:.4f}<extra></extra>",
            ),
            row=current_row, col=1
        )
        # Histogram
        hist_colors = [
            CHART_COLORS["macd_hist_pos"] if val >= 0 else CHART_COLORS["macd_hist_neg"]
            for val in df["MACD_Hist"]
        ]
        fig.add_trace(
            go.Bar(
                x=df["DateLabel"],
                y=df["MACD_Hist"],
                name="Histogram",
                marker_color=hist_colors,
                hovertemplate="Hist: %{y:.4f}<extra></extra>",
            ),
            row=current_row, col=1
        )
        # Zero line
        fig.add_hline(y=0, line=dict(color="#404040", width=1), row=current_row, col=1)
        current_row += 1

    # ATR
    if "ATR" in subplot_indicators and "ATR" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["DateLabel"],
                y=df["ATR"],
                name="ATR(14)",
                line=dict(color=CHART_COLORS["atr"], width=1.5),
                fill="tozeroy",
                fillcolor="rgba(41, 182, 246, 0.2)",
                hovertemplate="ATR: %{y:.4f}<extra></extra>",
            ),
            row=current_row, col=1
        )

    # === Apply Dark Theme ===
    fig = apply_dark_theme(fig, num_rows)

    return fig


def apply_dark_theme(fig: go.Figure, num_rows: int) -> go.Figure:
    """Apply light theme to the chart."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family="Inter, sans-serif", color="#1a1a1a", size=12),
        xaxis_rangeslider_visible=False,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.8)",
            font=dict(size=10),
        ),
        margin=dict(l=60, r=60, t=80, b=40),
        hovermode="x unified",
        height=600 + (num_rows - 1) * 180,
    )

    # Update all axes
    for i in range(1, num_rows + 1):
        fig.update_xaxes(
            gridcolor="#e0e0e0",
            showgrid=True,
            zeroline=False,
            showline=True,
            linecolor="#e0e0e0",
            type="category",  # Use categorical axis to avoid gaps
            nticks=10,  # Limit number of tick labels
            tickangle=-45,  # Angle labels for better readability
            row=i, col=1
        )
        fig.update_yaxes(
            gridcolor="#e0e0e0",
            showgrid=True,
            zeroline=False,
            showline=True,
            linecolor="#e0e0e0",
            side="right",
            row=i, col=1
        )

    # Hide x-axis labels for all but last row
    for i in range(1, num_rows):
        fig.update_xaxes(showticklabels=False, row=i, col=1)

    return fig


def get_latest_values(df: pd.DataFrame) -> dict:
    """Extract latest indicator values for display."""
    if df is None or df.empty:
        return {}

    latest = df.iloc[-1]
    values = {
        "close": latest.get("Close"),
        "change": None,
        "change_pct": None,
    }

    # Calculate change from previous close
    if len(df) >= 2:
        prev_close = df.iloc[-2]["Close"]
        values["change"] = latest["Close"] - prev_close
        values["change_pct"] = (values["change"] / prev_close) * 100

    # Add indicator values if present
    indicator_cols = ["EMA10", "EMA20", "EMA50", "EMA100", "RSI", "MACD", "ATR"]
    for col in indicator_cols:
        if col in df.columns:
            values[col.lower()] = latest.get(col)

    return values
