"""Sidebar component with input controls."""

import uuid
import streamlit as st

# Asset type examples for placeholder text
ASSET_EXAMPLES = {
    "forex": "e.g., EUR/USD, GBP/USD, USD/JPY",
    "commodity": "e.g., XAU/USD, XAG/USD, USOIL",
    "crypto": "e.g., BTC/USD, ETH/USD, SOL/USD",
    "stock": "e.g., AAPL, MSFT, GOOGL",
}


def _is_streaming() -> bool:
    """Check if agent is currently streaming."""
    return st.session_state.get("is_streaming", False)


def render_sidebar() -> dict:
    """
    Render the sidebar with all input controls.

    Returns:
        Dictionary with current settings from the sidebar
    """
    with st.sidebar:
        # App title/logo - matching landing page style
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem 0;">
                <div style="font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #1976d2 0%, #7c4dff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: -0.02em;">Tradable Mind</div>
                <p class="sidebar-tagline">
                    AI-Powered Market Analysis
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Theme toggle
        is_dark = st.session_state.get("theme_mode", "light") == "dark"
        toggle_label = "\u2600\ufe0f Light" if is_dark else "\U0001f319 Dark"
        if st.button(toggle_label, key="theme_toggle", use_container_width=True, type="secondary"):
            st.session_state.theme_mode = "light" if is_dark else "dark"
            st.rerun()

        # Show warning when agent is working
        if _is_streaming():
            st.warning("Agent working... Controls disabled", icon=":material/hourglass_empty:")

        st.divider()

        # === Asset & Chart Settings ===
        st.markdown('<p class="sidebar-section">Chart Settings</p>', unsafe_allow_html=True)

        asset_type = st.selectbox(
            "Asset Type",
            options=["forex", "commodity", "crypto", "stock"],
            index=["forex", "commodity", "crypto", "stock"].index(
                st.session_state.get("current_asset_type", "forex")
            ),
            help="Select the asset type for proper market hours filtering",
            disabled=_is_streaming()
        )

        symbol = st.text_input(
            "Asset Symbol",
            value=st.session_state.get("current_symbol", "EUR/USD"),
            placeholder=ASSET_EXAMPLES.get(asset_type, ""),
            help="Enter a valid trading symbol",
            disabled=_is_streaming()
        )

        col1, col2 = st.columns(2)

        with col1:
            interval = st.selectbox(
                "Interval",
                options=["1min", "5min", "15min", "30min", "1h", "2h", "4h", "1day", "1week"],
                index=6,  # Default to 4h
                help="Chart timeframe",
                disabled=_is_streaming()
            )

        with col2:
            chart_size = st.number_input(
                "Bars",
                min_value=50,
                max_value=300,
                value=100,
                step=10,
                help="Number of candlesticks",
                disabled=_is_streaming()
            )

        st.divider()

        # === Technical Indicators ===
        st.markdown('<p class="sidebar-section">Overlay Indicators</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            ema_10 = st.checkbox("EMA 10", value=False, disabled=_is_streaming())
            ema_50 = st.checkbox("EMA 50", value=True, disabled=_is_streaming())
        with col2:
            ema_20 = st.checkbox("EMA 20", value=True, disabled=_is_streaming())
            ema_100 = st.checkbox("EMA 100", value=False, disabled=_is_streaming())

        bb = st.checkbox("Bollinger Bands", value=False, disabled=_is_streaming())

        st.markdown('<p class="sidebar-section">Subplot Indicators</p>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            rsi = st.checkbox("RSI", value=False, disabled=_is_streaming())
        with col2:
            macd = st.checkbox("MACD", value=False, disabled=_is_streaming())
        with col3:
            atr = st.checkbox("ATR", value=False, disabled=_is_streaming())

        st.markdown('<p class="sidebar-section">Price Levels</p>', unsafe_allow_html=True)

        pivot = st.checkbox("Pivot Points", value=False, disabled=_is_streaming())

        st.divider()

        # === Load Chart Button ===
        load_clicked = st.button(
            "Load Chart",
            type="primary",
            use_container_width=True,
            help="Fetch data and render chart" if not _is_streaming() else "Please wait for agent to finish",
            disabled=_is_streaming()
        )

        # Show status
        if st.session_state.get("chart_loaded"):
            st.success("Chart loaded successfully", icon=":material/check:")

        st.divider()

        # === Clear Conversation Button ===
        clear_clicked = st.button(
            "Clear Conversation",
            type="secondary",
            use_container_width=True,
            help="Clear chat history and start fresh" if not _is_streaming() else "Please wait for agent to finish",
            disabled=_is_streaming()
        )

        if clear_clicked:
            if _is_streaming():
                # Queue the clear for when streaming finishes
                st.session_state.pending_clear_conversation = True
                st.toast("Will clear after agent finishes")
            else:
                st.session_state.messages = []
                st.session_state.pending_tasks = {}
                st.session_state.thread_id = str(uuid.uuid4())  # New thread for fresh conversation
                st.rerun()

        # === Return Settings ===
        # Get API key from session state (set during landing page)
        gemini_api_key = st.session_state.get("gemini_api_key", "")
        return {
            "gemini_api_key": gemini_api_key,
            "asset_type": asset_type,
            "symbol": symbol.strip().upper() if symbol else "",
            "interval": interval,
            "chart_size": chart_size,
            "indicators": {
                "ema_10": ema_10,
                "ema_20": ema_20,
                "ema_50": ema_50,
                "ema_100": ema_100,
                "bb": bb,
                "rsi": rsi,
                "macd": macd,
                "atr": atr,
                "pivot": pivot,
                "volume": True,  # Always show volume if available
            },
            "load_clicked": load_clicked,
        }


def validate_inputs(settings: dict) -> tuple[bool, str]:
    """
    Validate sidebar inputs.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not settings["symbol"]:
        return False, "Please enter an asset symbol"

    return True, ""
