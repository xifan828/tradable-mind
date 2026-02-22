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

from streamlit_app.utils.styles import inject_custom_css, PIVOT_COLORS
from streamlit_app.components.sidebar import render_sidebar, validate_inputs
from streamlit_app.components.chart import create_candlestick_chart, get_latest_values
from streamlit_app.components.chat import (
    initialize_chat_state,
    render_chat_history,
    add_message,
    process_user_input,
)
from streamlit_app.services.data_service import fetch_cached_data, fetch_daily_change, fetch_pivot_points


# Default question prompts for first-time users
DEFAULT_QUESTIONS = [
    "What's the overall picture here? Create a trading strategy.",
    "Analyze the current market structure. What are the critical price levels to watch?",
    "How strong is the current trend? Is momentum building or fading?",
    "What does the historical data suggest about the current setup?"
]


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
        # Theme
        "theme_mode": "light",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Initialize chat state
    initialize_chat_state()


def render_front_page():
    """Render the redesigned front page."""
    st.markdown("""
    <style>
        .block-container {
            max-width: 960px !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            margin: 0 auto !important;
        }
    </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([11, 9], gap="large")

    with col_left:
        st.markdown("""
        <div class="lp-hero-left">
            <div class="lp-badge">
                <span class="lp-badge-dot"></span>
                Powered by Google Gemini 3.0
            </div>
            <h1 class="lp-title">Tradable Mind: Your AI Thinking Partner<br><span class="lp-title-accent" style="font-size:0.75em;">for Real-Time Market Analysis</span></h1>
            <p class="lp-desc">
                Multi-agent analysis with specialized Chart &amp; Quant agents.
                Move beyond black-box signals with institutional-grade reasoning chains
                and visual pattern recognition.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_input, col_btn = st.columns([3, 1])
        with col_input:
            api_key = st.text_input(
                "API Key",
                type="password",
                placeholder="Enter your Gemini API Key",
                key="front_page_api_key",
                label_visibility="collapsed",
            )
        with col_btn:
            st.button("Get Started", type="primary", use_container_width=True)

        st.markdown("""
        <div class="lp-api-link">
            <a href="https://aistudio.google.com/app/apikey" target="_blank">
                &#8599; Get your Gemini API key from Google AI Studio
            </a>
            <span class="lp-api-note">&#9888; Requires a paid tier — free API keys will not work.</span>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="lp-mockup-wrapper">
            <div class="lp-mockup-glow"></div>
            <div class="lp-mockup-chrome-only">
                <div class="lp-mockup-dots">
                    <div class="lp-mockup-dot" style="background:#f87171"></div>
                    <div class="lp-mockup-dot" style="background:#fbbf24"></div>
                    <div class="lp-mockup-dot" style="background:#4ade80"></div>
                </div>
                <div class="lp-mockup-title">Tradable Mind — Live Demo</div>
                <div style="width:16px"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        video_path = Path(__file__).parent / "utils" / "vedio.mp4"
        st.video(str(video_path), loop=True, muted=True, autoplay=True)

    # Features section
    st.markdown("""
    <div class="lp-features-section">
        <h2 class="lp-features-heading" style="text-align:center;max-width:100%;">Think deeper, trade smarter with collaborative AI agents.</h2>
        <div class="lp-cards-grid">
            <div class="lp-card">
                <div class="lp-card-icon">
                    <span class="material-symbols-outlined">hub</span>
                </div>
                <div class="lp-card-title">Multi-agent Analysis</div>
                <p class="lp-card-desc">Seamless orchestration between specialized Vision agents (pattern recognition) and Math agents (quant data).</p>
            </div>
            <div class="lp-card">
                <div class="lp-card-icon">
                    <span class="material-symbols-outlined">visibility</span>
                </div>
                <div class="lp-card-title">Pattern Recognition</div>
                <p class="lp-card-desc">Our AI identifies visual candlestick structures like Head &amp; Shoulders or flags while simultaneously computing RSI divergence.</p>
            </div>
            <div class="lp-card">
                <div class="lp-card-icon">
                    <span class="material-symbols-outlined">account_tree</span>
                </div>
                <div class="lp-card-title">Full Reasoning Chains</div>
                <p class="lp-card-desc">No black boxes. See the full logical deduction path for every trade signal, citing specific data points and patterns.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="lp-footer">
        <div class="lp-footer-logo">
            <div class="lp-footer-logo-icon">
                <span class="material-symbols-outlined" style="font-size:1rem">neurology</span>
            </div>
            <span class="lp-footer-logo-text">Tradable Mind</span>
        </div>
        <div class="lp-footer-disclosure">
            <div class="lp-footer-disclosure-title">Transparency &amp; Risk Disclosure</div>
            <div class="lp-footer-disclosure-items">
                <div class="lp-footer-disclosure-item">
                    <span class="lp-footer-disclosure-label">Data Variance:</span>
                    Market data may vary slightly across different providers. If you notice any inconsistencies, we actively review and adjust.
                </div>
                <div class="lp-footer-disclosure-item">
                    <span class="lp-footer-disclosure-label">AI Analysis:</span>
                    Insights are generated by a multi-agent reasoning engine. While designed for logic and structure, AI outputs may contain errors or hallucinate market context.
                </div>
                <div class="lp-footer-disclosure-item">
                    <span class="lp-footer-disclosure-label">Not Financial Advice:</span>
                    Tradable Mind is a research and reasoning tool. It does not provide financial advice or trade execution. Never invest based solely on AI-generated analysis.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    theme_mode = st.session_state.get("theme_mode", "light")

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
            pc = PIVOT_COLORS.get(theme_mode, PIVOT_COLORS["light"])
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
                    <span style="background: {pc['R3']['bg']}; color: {pc['R3']['text']}; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">
                        R3: {pivot_levels.get('R3', 0):.4f}
                    </span>
                    <span style="background: {pc['R2']['bg']}; color: {pc['R2']['text']}; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">
                        R2: {pivot_levels.get('R2', 0):.4f}
                    </span>
                    <span style="background: {pc['R1']['bg']}; color: {pc['R1']['text']}; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">
                        R1: {pivot_levels.get('R1', 0):.4f}
                    </span>
                    <span style="background: {pc['Pivot']['bg']}; color: {pc['Pivot']['text']}; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">
                        P: {pivot_levels.get('Pivot', 0):.4f}
                    </span>
                    <span style="background: {pc['S1']['bg']}; color: {pc['S1']['text']}; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">
                        S1: {pivot_levels.get('S1', 0):.4f}
                    </span>
                    <span style="background: {pc['S2']['bg']}; color: {pc['S2']['text']}; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">
                        S2: {pivot_levels.get('S2', 0):.4f}
                    </span>
                    <span style="background: {pc['S3']['bg']}; color: {pc['S3']['text']}; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">
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
        theme_mode=theme_mode,
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

    # Chat input with send button (allows pre-filling from default questions)
    is_streaming = st.session_state.get("is_streaming", False)

    # Only show input controls when not streaming
    if not is_streaming:
        # Show default questions for first-time users
        render_default_questions()

        # Initialize chat_input_area if not present
        if "chat_input_area" not in st.session_state:
            st.session_state.chat_input_area = ""

        # Check if we should clear the input (set by send button callback)
        if st.session_state.get("clear_chat_input", False):
            st.session_state.chat_input_area = ""
            st.session_state.clear_chat_input = False

        # Icon before text input
        from streamlit_app.utils.styles import LIGHT_COLORS, DARK_COLORS
        _tm = st.session_state.get("theme_mode", "light")
        _colors = DARK_COLORS if _tm == "dark" else LIGHT_COLORS
        st.markdown(
            f'<div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; color: {_colors["text_primary"]};">'
            '<span style="font-size: 1rem;">▶</span>'
            '<span style="font-weight: 500;">Your Message</span>'
            '</div>',
            unsafe_allow_html=True
        )

        # Text area for message input
        prompt = st.text_area(
            "Message",
            placeholder="Ask about the chart or request analysis...",
            disabled=not can_chat,
            key="chat_input_area",
            height=100,
            label_visibility="collapsed"
        )

        # Send button
        col1, col2, col3 = st.columns([5, 1, 5])
        with col2:
            send_clicked = st.button(
                "Send",
                disabled=not can_chat or not prompt.strip(),
                use_container_width=True,
                type="primary"
            )
    else:
        # During streaming, no input controls shown
        send_clicked = False
        prompt = ""

    if send_clicked and prompt.strip():
        # Set flag to clear input on next rerun
        st.session_state.clear_chat_input = True

        # Store prompt and set streaming flag, then rerun to disable sidebar
        st.session_state.pending_prompt = prompt.strip()
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


def render_default_questions():
    """
    Render default question buttons in an expander.
    Only shown when chart is loaded, API key present, no messages, and not streaming.
    """
    # Display conditions
    show_questions = (
        st.session_state.get("chart_data") is not None
        and st.session_state.get("gemini_api_key")
        and not st.session_state.get("is_streaming", False)
        and len(st.session_state.messages) == 0
    )

    if not show_questions:
        return

    with st.expander("Quick Start Questions", expanded=True, icon=":material/chat:"):
        st.caption("Click a question to populate the input field, then modify or send as-is.")

        # Wrapper for custom button styling
        st.markdown('<div class="default-questions-container">', unsafe_allow_html=True)

        # 2x2 grid layout
        col1, col2 = st.columns(2)

        # Left column: Questions 1 and 3
        with col1:
            if st.button(
                DEFAULT_QUESTIONS[0],
                key="default_q1",
                disabled=st.session_state.get("is_streaming", False),
                use_container_width=True,
                type="secondary"
            ):
                st.session_state.chat_input_area = DEFAULT_QUESTIONS[0]
                st.rerun()

            if st.button(
                DEFAULT_QUESTIONS[2],
                key="default_q3",
                disabled=st.session_state.get("is_streaming", False),
                use_container_width=True,
                type="secondary"
            ):
                st.session_state.chat_input_area = DEFAULT_QUESTIONS[2]
                st.rerun()

        # Right column: Questions 2 and 4
        with col2:
            if st.button(
                DEFAULT_QUESTIONS[1],
                key="default_q2",
                disabled=st.session_state.get("is_streaming", False),
                use_container_width=True,
                type="secondary"
            ):
                st.session_state.chat_input_area = DEFAULT_QUESTIONS[1]
                st.rerun()

            if st.button(
                DEFAULT_QUESTIONS[3],
                key="default_q4",
                disabled=st.session_state.get("is_streaming", False),
                use_container_width=True,
                type="secondary"
            ):
                st.session_state.chat_input_area = DEFAULT_QUESTIONS[3]
                st.rerun()

        # Close wrapper div
        st.markdown('</div>', unsafe_allow_html=True)


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
    theme_mode = st.session_state.get("theme_mode", "light")
    inject_custom_css(theme_mode)

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
