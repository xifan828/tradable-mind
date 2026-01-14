"""
Tradable Mind - AI-Powered Technical Analysis Platform

Main Streamlit application entry point.
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio
import streamlit as st

from streamlit_app.utils.styles import inject_custom_css
from streamlit_app.components.sidebar import render_sidebar, validate_inputs
from streamlit_app.components.chart import create_candlestick_chart, get_latest_values
from streamlit_app.components.chat import (
    initialize_chat_state,
    render_chat_history,
    add_message,
    process_user_input,
)
from streamlit_app.services.data_service import ChartDataService, fetch_cached_data


# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="Tradable Mind - Technical Analysis",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="expanded",
)


def initialize_session_state():
    """Initialize all session state variables."""
    defaults = {
        "chart_data": None,
        "current_symbol": "EUR/USD",
        "current_interval": "4h",
        "chart_loaded": False,
        "pivot_levels": None,
        "fibonacci_levels": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Initialize chat state
    initialize_chat_state()


def render_header():
    """Render the main header."""
    st.markdown(
        """
        <div class="main-header">
            <h1>Technical Analysis</h1>
            <p>Interactive charts powered by AI insights</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_chart_section(settings: dict):
    """Render the chart section with price info."""
    if st.session_state.chart_data is None:
        st.info(
            "Enter an asset symbol and click 'Load Chart' to begin.",
            icon=":material/candlestick_chart:"
        )
        return

    df = st.session_state.chart_data

    # Price info row
    latest = get_latest_values(df)
    if latest.get("close"):
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

        with col1:
            st.markdown(f"### {st.session_state.current_symbol}")

        with col2:
            close_price = latest["close"]
            st.metric("Price", f"{close_price:.4f}")

        with col3:
            change = latest.get("change", 0)
            change_pct = latest.get("change_pct", 0)
            if change is not None:
                delta_color = "normal" if change >= 0 else "inverse"
                st.metric(
                    "Change",
                    f"{change:+.4f}",
                    f"{change_pct:+.2f}%",
                    delta_color=delta_color
                )

        with col4:
            rsi = latest.get("rsi")
            if rsi:
                st.metric("RSI", f"{rsi:.1f}")

    # Create and display chart
    fig = create_candlestick_chart(
        df=df,
        symbol=st.session_state.current_symbol,
        interval=st.session_state.current_interval,
        indicators=settings["indicators"],
        pivot_levels=st.session_state.pivot_levels,
        fibonacci_levels=st.session_state.fibonacci_levels,
    )

    st.plotly_chart(fig, use_container_width=True, config={
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    })


def render_chat_section(settings: dict):
    """Render the chat section with input."""
    st.markdown("---")
    st.markdown("### AI Analysis Chat")

    # Display chat history
    render_chat_history()

    # Check if we can chat
    can_chat = bool(settings.get("gemini_api_key"))

    if not can_chat:
        st.warning(
            "Enter your Gemini API key in the sidebar to enable AI analysis chat.",
            icon=":material/key:"
        )

    # Chat input
    if prompt := st.chat_input(
        "Ask about the chart or request analysis...",
        disabled=not can_chat
    ):
        # Add user message
        add_message("user", prompt, "text")

        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process with agent
        with st.chat_message("assistant"):
            asyncio.run(process_user_input(
                user_input=prompt,
                gemini_api_key=settings["gemini_api_key"],
                current_symbol=st.session_state.current_symbol,
                current_interval=st.session_state.current_interval,
            ))


def load_chart_data(settings: dict):
    """Load chart data based on current settings."""
    is_valid, error = validate_inputs(settings)

    if not is_valid:
        st.error(error)
        return False

    with st.spinner(f"Loading data for {settings['symbol']}..."):
        try:
            # Fetch data
            df = fetch_cached_data(
                symbol=settings["symbol"],
                interval=settings["interval"],
                outputsize=settings["chart_size"]
            )

            if df is None or df.empty:
                st.error("Failed to fetch data. Please check the symbol and try again.")
                return False

            # Calculate levels if needed
            service = ChartDataService()
            pivot_levels = None
            fibonacci_levels = None

            if settings["indicators"].get("pivot"):
                pivot_levels = service.calculate_pivot_points(df)

            if settings["indicators"].get("fibonacci"):
                fibonacci_levels = service.calculate_fibonacci_levels(df)

            # Update session state
            st.session_state.chart_data = df
            st.session_state.current_symbol = settings["symbol"]
            st.session_state.current_interval = settings["interval"]
            st.session_state.pivot_levels = pivot_levels
            st.session_state.fibonacci_levels = fibonacci_levels
            st.session_state.chart_loaded = True

            return True

        except Exception as e:
            st.error(f"Error loading data: {e}")
            return False


def main():
    """Main application entry point."""
    # Initialize state
    initialize_session_state()

    # Inject custom CSS
    inject_custom_css()

    # Render sidebar and get settings
    settings = render_sidebar()

    # Handle load chart button
    if settings["load_clicked"]:
        success = load_chart_data(settings)
        if success:
            st.rerun()

    # Main content area
    render_header()

    # Chart section
    render_chart_section(settings)

    # Chat section
    render_chat_section(settings)


if __name__ == "__main__":
    main()
