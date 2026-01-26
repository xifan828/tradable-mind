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
from streamlit_app.services.data_service import fetch_cached_data, fetch_daily_change, fetch_pivot_points


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
        "current_asset_type": "forex",  # Asset type for market hours filtering
        "chart_loaded": False,
        "pivot_levels": None,
        "daily_change": None,  # Store daily change data
        "current_indicators": {},  # Store selected indicators for AI context
        # API key (stored for front page flow)
        "gemini_api_key": "",
        # Agent configuration
        "min_research_iterations": 2,
        "max_research_iterations": 6,
        "max_concurrent_tasks": 4,
        # Pending actions (queued during streaming)
        "pending_load_chart": False,
        "pending_clear_conversation": False,
        "pending_chart_settings": None,
        # Pending prompt (set before rerun to ensure sidebar is disabled)
        "pending_prompt": None,
        "pending_prompt_settings": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Initialize chat state
    initialize_chat_state()


def render_front_page():
    """Render the front page when API key is not provided."""
    # Full centered layout
    st.markdown(
        """
        <div class="front-page">
            <div class="front-page-logo">Tradable Mind</div>
            <p class="front-page-headline">AI Agent that helps you reason about the market.</p>
            <p class="front-page-tagline">
                Stop following indicators. <span class="tagline-highlight">Start following reasoning.</span>
            </p>
            <div class="front-page-cta">
                <p class="cta-text">To begin, enter your Gemini API key</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Very narrow center column for input
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Paste API key here",
            key="front_page_api_key",
            label_visibility="collapsed"
        )

    st.markdown(
        """
        <div class="front-page-link">
            <a href="https://aistudio.google.com/app/apikey" target="_blank">
                Get your free API key from Google AI Studio →
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    return api_key


def render_chart_section(settings: dict):
    """Render the chart section with price info."""
    if st.session_state.chart_data is None:
        st.info(
            "**To begin:**\n"
            "- Enter an asset symbol\n"
            "- Choose your indicators\n"
            "- Press Load Chart",
            icon=":material/candlestick_chart:"
        )
        return

    df = st.session_state.chart_data

    # Price info row - compact layout
    latest = get_latest_values(df)
    if latest.get("close"):
        close_price = latest["close"]

        # Use daily change instead of interval change
        daily_change = st.session_state.daily_change
        if daily_change:
            change = daily_change.get("change", 0)
            change_pct = daily_change.get("change_pct", 0)
        else:
            change = latest.get("change", 0)
            change_pct = latest.get("change_pct", 0)

        # Build change display
        if change is not None and change >= 0:
            change_color = "#22c55e"
            change_icon = "▲"
        else:
            change_color = "#ef4444"
            change_icon = "▼"

        # Check if pivot points should be displayed
        show_pivot = settings["indicators"].get("pivot") and st.session_state.pivot_levels

        if show_pivot:
            pivot_levels = st.session_state.pivot_levels
            # Single row layout with price info and pivot points inline
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 1.5rem; flex-wrap: wrap;">
                    <span style="font-size: 1.5rem; font-weight: 600;">{st.session_state.current_symbol}</span>
                    <span style="font-size: 1.25rem; font-weight: 500;">{close_price:.4f}</span>
                    <span style="color: {change_color}; font-size: 0.95rem;">
                        {change_icon} {abs(change):.4f} ({change_pct:+.2f}%)
                    </span>
                    <span style="color: #9ca3af; margin: 0 0.25rem;">|</span>
                    <span style="background: #fee2e2; color: #dc2626; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">
                        R3: {pivot_levels.get('R3', 0):.4f}
                    </span>
                    <span style="background: #fecaca; color: #dc2626; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">
                        R2: {pivot_levels.get('R2', 0):.4f}
                    </span>
                    <span style="background: #fef2f2; color: #dc2626; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">
                        R1: {pivot_levels.get('R1', 0):.4f}
                    </span>
                    <span style="background: #f3f4f6; color: #374151; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">
                        P: {pivot_levels.get('Pivot', 0):.4f}
                    </span>
                    <span style="background: #f0fdf4; color: #16a34a; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">
                        S1: {pivot_levels.get('S1', 0):.4f}
                    </span>
                    <span style="background: #bbf7d0; color: #16a34a; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">
                        S2: {pivot_levels.get('S2', 0):.4f}
                    </span>
                    <span style="background: #86efac; color: #16a34a; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">
                        S3: {pivot_levels.get('S3', 0):.4f}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Compact layout without pivot points
            st.markdown(
                f"""
                <div style="display: flex; align-items: baseline; gap: 1rem; flex-wrap: wrap;">
                    <span style="font-size: 1.5rem; font-weight: 600;">{st.session_state.current_symbol}</span>
                    <span style="font-size: 1.25rem; font-weight: 500;">{close_price:.4f}</span>
                    <span style="color: {change_color}; font-size: 0.95rem;">
                        {change_icon} {abs(change):.4f} ({change_pct:+.2f}%)
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Create and display chart
    fig = create_candlestick_chart(
        df=df,
        symbol=st.session_state.current_symbol,
        interval=st.session_state.current_interval,
        indicators=settings["indicators"],
        pivot_levels=st.session_state.pivot_levels,
    )

    st.plotly_chart(fig, use_container_width=True, config={
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    })


def render_agent_settings():
    """Render agent configuration settings in an expander."""
    # Clamp values to valid ranges (in case of existing sessions with old limits)
    st.session_state.min_research_iterations = min(st.session_state.min_research_iterations, 6)
    st.session_state.max_research_iterations = min(st.session_state.max_research_iterations, 6)
    st.session_state.max_concurrent_tasks = min(st.session_state.max_concurrent_tasks, 4)

    with st.expander("Agent Configuration", expanded=True, icon=":material/tune:"):
        st.caption("Settings are applied automatically to the next message.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.session_state.min_research_iterations = st.selectbox(
                "Min Iterations",
                options=[1, 2, 3, 4, 5, 6],
                index=st.session_state.min_research_iterations - 1,
                help="Minimum research iterations before concluding"
            )

        with col2:
            st.session_state.max_research_iterations = st.selectbox(
                "Max Iterations",
                options=[1, 2, 3, 4, 5, 6],
                index=st.session_state.max_research_iterations - 1,
                help="Maximum research iterations allowed"
            )

        with col3:
            st.session_state.max_concurrent_tasks = st.selectbox(
                "Parallel Tasks",
                options=[1, 2, 3, 4],
                index=st.session_state.max_concurrent_tasks - 1,
                help="Maximum tasks to run in parallel"
            )


def render_chat_section(settings: dict):
    """Render the chat section with input."""
    st.markdown("---")
    st.markdown("### Ask the Agent")

    # Agent settings
    render_agent_settings()

    # Display chat history
    render_chat_history()

    # Check if we can chat
    can_chat = bool(settings.get("gemini_api_key"))

    if not can_chat:
        st.warning(
            "Enter your Gemini API key in the sidebar to enable AI analysis chat.",
            icon=":material/key:"
        )

    # Chat input (disabled during streaming)
    is_streaming = st.session_state.get("is_streaming", False)
    if prompt := st.chat_input(
        "Ask about the chart or request analysis..." if not is_streaming
        else "Please wait for analysis to complete...",
        disabled=not can_chat or is_streaming
    ):
        # Store prompt and set streaming flag, then rerun to disable sidebar
        st.session_state.pending_prompt = prompt
        st.session_state.pending_prompt_settings = {
            "gemini_api_key": settings["gemini_api_key"],
            "current_symbol": st.session_state.current_symbol,
            "current_interval": st.session_state.current_interval,
            "current_indicators": st.session_state.current_indicators,
            "current_asset_type": st.session_state.current_asset_type,
        }
        st.session_state.is_streaming = True
        st.rerun()

    # Process pending prompt (after rerun with disabled sidebar)
    if st.session_state.get("pending_prompt") and is_streaming:
        prompt = st.session_state.pending_prompt
        prompt_settings = st.session_state.pending_prompt_settings
        st.session_state.pending_prompt = None
        st.session_state.pending_prompt_settings = None

        # Add user message
        add_message("user", prompt, "text")

        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process with agent
        with st.chat_message("assistant"):
            asyncio.run(process_user_input(
                user_input=prompt,
                gemini_api_key=prompt_settings["gemini_api_key"],
                current_symbol=prompt_settings["current_symbol"],
                current_interval=prompt_settings["current_interval"],
                current_indicators=prompt_settings["current_indicators"],
                current_asset_type=prompt_settings.get("current_asset_type"),
            ))


def load_chart_data(settings: dict):
    """Load chart data based on current settings."""
    is_valid, error = validate_inputs(settings)

    if not is_valid:
        st.error(error)
        return False

    with st.spinner(f"Loading data for {settings['symbol']}..."):
        try:
            # Fetch data with asset_type for proper market hours filtering
            df = fetch_cached_data(
                symbol=settings["symbol"],
                interval=settings["interval"],
                outputsize=settings["chart_size"],
                asset_type=settings.get("asset_type")
            )

            if df is None or df.empty:
                st.error("Failed to fetch data. Please check the symbol and try again.")
                return False

            # Calculate levels if needed
            pivot_levels = None

            if settings["indicators"].get("pivot"):
                pivot_levels = fetch_pivot_points(
                    settings["symbol"],
                    asset_type=settings.get("asset_type")
                )

            # Fetch daily change with asset_type for proper filtering
            daily_change = fetch_daily_change(
                settings["symbol"],
                asset_type=settings.get("asset_type")
            )

            # Update session state
            st.session_state.chart_data = df
            st.session_state.current_symbol = settings["symbol"]
            st.session_state.current_interval = settings["interval"]
            st.session_state.current_asset_type = settings.get("asset_type", "forex")
            st.session_state.pivot_levels = pivot_levels
            st.session_state.daily_change = daily_change
            st.session_state.current_indicators = settings["indicators"]
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

    # Check if we have an API key stored from previous session or front page
    stored_api_key = st.session_state.get("gemini_api_key", "")

    # If no stored API key, show front page
    if not stored_api_key:
        front_page_key = render_front_page()
        if front_page_key:
            st.session_state.gemini_api_key = front_page_key
            st.rerun()
        return

    # Render sidebar and get settings
    settings = render_sidebar()

    # Handle load chart button
    if settings["load_clicked"]:
        if st.session_state.get("is_streaming", False):
            # Queue the load for when streaming finishes
            st.session_state.pending_load_chart = True
            st.session_state.pending_chart_settings = settings.copy()
            st.toast("Chart will load after agent finishes")
        else:
            success = load_chart_data(settings)
            if success:
                st.rerun()

    # Process queued chart load (after streaming completed)
    if st.session_state.get("pending_load_chart") and not st.session_state.get("is_streaming"):
        st.session_state.pending_load_chart = False
        pending_settings = st.session_state.get("pending_chart_settings")
        if pending_settings:
            st.session_state.pending_chart_settings = None
            success = load_chart_data(pending_settings)
            if success:
                st.rerun()

    # Chart section
    render_chart_section(settings)

    # Chat section (only show after chart is loaded)
    if st.session_state.chart_loaded:
        render_chat_section(settings)


if __name__ == "__main__":
    main()
