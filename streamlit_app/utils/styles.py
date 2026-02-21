"""Theme styling for Tradable Mind Streamlit app."""

# ---------------------------------------------------------------------------
# Color palettes
# ---------------------------------------------------------------------------

LIGHT_COLORS = {
    # Backgrounds
    "app_bg": "#f5f5f5",
    "sidebar_bg": "#ffffff",
    "card_bg": "#ffffff",
    "border": "#e0e0e0",
    # Text
    "text_primary": "#1a1a1a",
    "text_muted": "#666666",
    # Accent
    "primary": "#1976d2",
    "primary_hover": "#1565c0",
    "primary_active": "#0d47a1",
    "primary_shadow": "rgba(25, 118, 210, 0.2)",
    # Containers
    "tool_call_bg": "#e3f2fd",
    "tool_result_bg": "#e8f5e9",
    "thinking_bg": "#fff8e1",
    "task_bg": "#e0f2f1",
    "todo_bg": "#f3e5f5",
    # Inputs
    "input_bg": "#ffffff",
    "input_border": "#e0e0e0",
    # Secondary button
    "secondary_bg": "#f5f5f5",
    "secondary_hover": "#e0e0e0",
    "secondary_active": "#d0d0d0",
    "secondary_border": "#e0e0e0",
    "secondary_border_hover": "#bdbdbd",
    "secondary_disabled_bg": "#fafafa",
    "secondary_disabled_text": "#9e9e9e",
    "secondary_disabled_border": "#f0f0f0",
    # Misc
    "header_gradient_end": "#f5f5f5",
    "expander_hover": "#f5f5f5",
    "tab_bg": "#f5f5f5",
    "tab_selected_bg": "#ffffff",
    "scrollbar_track": "#f5f5f5",
    "scrollbar_thumb": "#bdbdbd",
    "scrollbar_thumb_hover": "#9e9e9e",
    "slider_track": "#e0e0e0",
    "cta_text": "#64748b",
}

DARK_COLORS = {
    # Backgrounds
    "app_bg": "#0e1117",
    "sidebar_bg": "#1a1a2e",
    "card_bg": "#1a1a2e",
    "border": "#2d2d3d",
    # Text
    "text_primary": "#e8e8f0",
    "text_muted": "#a0a0b0",
    # Accent
    "primary": "#4a90d9",
    "primary_hover": "#3a7bc8",
    "primary_active": "#2a6bb8",
    "primary_shadow": "rgba(74, 144, 217, 0.3)",
    # Containers
    "tool_call_bg": "#1a2435",
    "tool_result_bg": "#1a2d1e",
    "thinking_bg": "#2d2a1f",
    "task_bg": "#1a2d2d",
    "todo_bg": "#261d2e",
    # Inputs
    "input_bg": "#252535",
    "input_border": "#3d3d4d",
    # Secondary button
    "secondary_bg": "#2d2d3d",
    "secondary_hover": "#3d3d4d",
    "secondary_active": "#4d4d5d",
    "secondary_border": "#3d3d4d",
    "secondary_border_hover": "#4d4d5d",
    "secondary_disabled_bg": "#1a1a2e",
    "secondary_disabled_text": "#555566",
    "secondary_disabled_border": "#2d2d3d",
    # Misc
    "header_gradient_end": "#0e1117",
    "expander_hover": "#252535",
    "tab_bg": "#1a1a2e",
    "tab_selected_bg": "#252535",
    "scrollbar_track": "#0e1117",
    "scrollbar_thumb": "#3d3d4d",
    "scrollbar_thumb_hover": "#555566",
    "slider_track": "#3d3d4d",
    "cta_text": "#8090a0",
}

# ---------------------------------------------------------------------------
# Chart colors (shared across themes - vibrant enough for both)
# ---------------------------------------------------------------------------

CHART_COLORS = {
    "candle_up": "#26a69a",
    "candle_down": "#ef5350",
    "ema_10": "#2196F3",
    "ema_20": "#FF9800",
    "ema_50": "#9C27B0",
    "ema_100": "#E91E63",
    "bb_band": "#607D8B",
    "bb_middle": "#2196F3",
    "rsi": "#9C27B0",
    "rsi_overbought": "#ef5350",
    "rsi_oversold": "#26a69a",
    "macd_line": "#2196F3",
    "macd_signal": "#FF9800",
    "macd_hist_pos": "#26a69a",
    "macd_hist_neg": "#ef5350",
    "atr": "#29b6f6",
    "volume_up": "rgba(38, 166, 154, 0.5)",
    "volume_down": "rgba(239, 83, 80, 0.5)",
    "pivot": "#2196F3",
    "resistance": "#ef5350",
    "support": "#26a69a",
}

# Dark-mode overrides for chart elements that need visibility adjustments
CHART_THEME = {
    "light": {
        "template": "plotly_white",
        "paper_bg": "#ffffff",
        "plot_bg": "#ffffff",
        "grid": "#e0e0e0",
        "font_color": "#1a1a1a",
        "legend_bg": "rgba(255,255,255,0.8)",
        "ref_line": "#404040",
        "bb_fill_opacity": 0.1,
        "atr_fill_opacity": 0.2,
    },
    "dark": {
        "template": "plotly_dark",
        "paper_bg": "#1a1a2e",
        "plot_bg": "#1a1a2e",
        "grid": "#2d2d3d",
        "font_color": "#e8e8f0",
        "legend_bg": "rgba(26,26,46,0.95)",
        "ref_line": "#808090",
        "bb_fill_opacity": 0.15,
        "atr_fill_opacity": 0.3,
    },
}

# Pivot badge colors per theme
PIVOT_COLORS = {
    "light": {
        "R3": {"bg": "#fee2e2", "text": "#dc2626"},
        "R2": {"bg": "#fecaca", "text": "#dc2626"},
        "R1": {"bg": "#fef2f2", "text": "#dc2626"},
        "Pivot": {"bg": "#f3f4f6", "text": "#374151"},
        "S1": {"bg": "#f0fdf4", "text": "#16a34a"},
        "S2": {"bg": "#bbf7d0", "text": "#16a34a"},
        "S3": {"bg": "#86efac", "text": "#16a34a"},
    },
    "dark": {
        "R3": {"bg": "#3d1a1a", "text": "#ff9999"},
        "R2": {"bg": "#4d2020", "text": "#ff9999"},
        "R1": {"bg": "#5d2626", "text": "#ff9999"},
        "Pivot": {"bg": "#2d2d3d", "text": "#e8e8f0"},
        "S1": {"bg": "#1a3d1a", "text": "#99ff99"},
        "S2": {"bg": "#204d20", "text": "#99ff99"},
        "S3": {"bg": "#266626", "text": "#99ff99"},
    },
}


# ---------------------------------------------------------------------------
# CSS generation
# ---------------------------------------------------------------------------

def _build_css(colors: dict) -> str:
    """Build the full CSS string using the given color palette."""
    return f"""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global styles */
    .stApp {{
        background-color: {colors["app_bg"]};
        font-family: 'Inter', sans-serif;
        color: {colors["text_primary"]};
    }}

    /* Global text color overrides for all Streamlit widgets */
    .stApp label,
    .stApp .stMarkdown,
    .stApp .stMarkdown p,
    .stApp .stMarkdown li,
    .stApp .stMarkdown h1,
    .stApp .stMarkdown h2,
    .stApp .stMarkdown h3,
    .stApp .stMarkdown h4,
    .stApp .stMarkdown h5,
    .stApp .stMarkdown h6,
    .stApp .stCaption,
    .stApp [data-testid="stWidgetLabel"],
    .stApp [data-testid="stWidgetLabel"] p,
    .stApp [data-testid="stMarkdownContainer"],
    .stApp [data-testid="stMarkdownContainer"] p,
    .stApp [data-testid="stMarkdownContainer"] li,
    .stApp [data-testid="stChatMessage"] p,
    .stApp [data-testid="stChatMessage"] li,
    .stApp [data-testid="stChatMessage"] h1,
    .stApp [data-testid="stChatMessage"] h2,
    .stApp [data-testid="stChatMessage"] h3,
    .stApp [data-testid="stExpander"] summary,
    .stApp [data-testid="stExpander"] summary span {{
        color: {colors["text_primary"]} !important;
    }}

    /* Select box / number input / dropdown text */
    .stApp [data-baseweb="select"] span,
    .stApp [data-baseweb="select"] div,
    .stApp [data-baseweb="input"] input,
    .stApp .stSelectbox div[data-baseweb="select"] > div {{
        color: {colors["text_primary"]} !important;
    }}

    /* Number input text */
    .stApp .stNumberInput input {{
        color: {colors["text_primary"]} !important;
        background-color: {colors["input_bg"]} !important;
        border-color: {colors["input_border"]} !important;
    }}

    /* Muted / caption text */
    .stApp small,
    .stApp .stCaption p,
    .stApp [data-testid="stCaptionContainer"] p {{
        color: {colors["text_muted"]} !important;
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {colors["sidebar_bg"]};
        border-right: 1px solid {colors["border"]};
    }}

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {{
        color: {colors["text_primary"]};
    }}

    /* Main header styling */
    .main-header {{
        background: linear-gradient(90deg, {colors["card_bg"]} 0%, {colors["header_gradient_end"]} 100%);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid {colors["border"]};
    }}

    .main-header h1 {{
        color: {colors["text_primary"]};
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
    }}

    .main-header p {{
        color: {colors["text_muted"]};
        margin: 0.25rem 0 0 0;
        font-size: 0.875rem;
    }}

    /* Chat message styling */
    [data-testid="stChatMessage"] {{
        background-color: {colors["card_bg"]};
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border: 1px solid {colors["border"]};
    }}

    /* Tool call containers */
    .tool-call-container {{
        background-color: {colors["tool_call_bg"]};
        border-left: 3px solid {colors["primary"]};
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 6px 6px 0;
        font-size: 0.875rem;
    }}

    .tool-call-header {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        color: {colors["primary"]};
        margin-bottom: 0.5rem;
    }}

    .tool-result-container {{
        background-color: {colors["tool_result_bg"]};
        border-left: 3px solid #388e3c;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 6px 6px 0;
        font-size: 0.875rem;
    }}

    .thinking-container {{
        background-color: {colors["thinking_bg"]};
        border-left: 3px solid #f9a825;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 6px 6px 0;
        font-style: italic;
        font-size: 0.875rem;
        color: {colors["text_muted"]};
    }}

    .task-container {{
        background-color: {colors["task_bg"]};
        border-left: 3px solid #00897b;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 6px 6px 0;
        font-size: 0.875rem;
    }}

    .todo-container {{
        background-color: {colors["todo_bg"]};
        border-left: 3px solid #7b1fa2;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 6px 6px 0;
    }}

    .todo-item {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0;
        font-size: 0.875rem;
    }}

    .todo-pending {{ color: #9e9e9e; }}
    .todo-in-progress {{ color: #f9a825; }}
    .todo-completed {{ color: #388e3c; }}

    /* Input fields */
    .stTextInput > div > div > input {{
        background-color: {colors["input_bg"]};
        color: {colors["text_primary"]};
        border: 1px solid {colors["input_border"]};
        border-radius: 6px;
    }}

    .stTextInput > div > div > input:focus {{
        border-color: {colors["primary"]};
        box-shadow: 0 0 0 2px {colors["primary_shadow"]};
    }}

    /* Text area styling */
    .stTextArea > div > div > textarea {{
        background-color: {colors["input_bg"]};
        color: {colors["text_primary"]};
        border: 1px solid {colors["input_border"]};
        border-radius: 6px;
    }}

    .stTextArea > div > div > textarea:focus {{
        border-color: {colors["primary"]};
        box-shadow: 0 0 0 2px {colors["primary_shadow"]};
        background-color: {colors["input_bg"]};
    }}

    /* Select boxes */
    .stSelectbox > div > div {{
        background-color: {colors["input_bg"]};
        border: 1px solid {colors["input_border"]};
        border-radius: 6px;
    }}

    .stSelectbox > div > div > div[data-baseweb="select"] > div {{
        background-color: {colors["input_bg"]} !important;
    }}

    /* Dropdown menu */
    [data-baseweb="popover"] > div,
    [data-baseweb="menu"],
    [data-baseweb="menu"] li {{
        background-color: {colors["card_bg"]} !important;
        color: {colors["text_primary"]} !important;
    }}

    [data-baseweb="menu"] li:hover {{
        background-color: {colors["secondary_hover"]} !important;
    }}

    /* Buttons */
    .stButton > button {{
        background-color: {colors["primary"]};
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: background-color 0.2s;
    }}

    .stButton > button:hover {{
        background-color: {colors["primary_hover"]};
    }}

    .stButton > button:active {{
        background-color: {colors["primary_active"]};
    }}

    /* Secondary buttons */
    button[kind="secondary"],
    button[data-testid="baseButton-secondary"] {{
        background-color: {colors["secondary_bg"]} !important;
        color: {colors["text_primary"]} !important;
        border: 1px solid {colors["secondary_border"]} !important;
    }}

    button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover {{
        background-color: {colors["secondary_hover"]} !important;
        border-color: {colors["secondary_border_hover"]} !important;
    }}

    button[kind="secondary"]:active,
    button[data-testid="baseButton-secondary"]:active {{
        background-color: {colors["secondary_active"]} !important;
    }}

    button[kind="secondary"]:disabled,
    button[data-testid="baseButton-secondary"]:disabled {{
        background-color: {colors["secondary_disabled_bg"]} !important;
        color: {colors["secondary_disabled_text"]} !important;
        border-color: {colors["secondary_disabled_border"]} !important;
    }}

    /* Checkboxes */
    .stCheckbox > label,
    .stCheckbox > label span {{
        color: {colors["text_primary"]} !important;
    }}

    /* Sliders */
    .stSlider > div > div > div {{
        background-color: {colors["slider_track"]};
    }}

    /* Expanders */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] > details > summary,
    [data-testid="stExpander"] summary {{
        background-color: {colors["card_bg"]} !important;
        border-radius: 6px;
        border: 1px solid {colors["border"]} !important;
        color: {colors["text_primary"]} !important;
    }}

    .streamlit-expanderHeader:hover,
    [data-testid="stExpander"] > details > summary:hover,
    [data-testid="stExpander"] summary:hover {{
        background-color: {colors["expander_hover"]} !important;
    }}

    [data-testid="stExpander"] > details {{
        border: 1px solid {colors["border"]} !important;
        border-radius: 6px;
        background-color: {colors["card_bg"]} !important;
    }}

    [data-testid="stExpander"] details > div[data-testid="stExpanderDetails"] {{
        background-color: {colors["card_bg"]} !important;
    }}

    /* Chart container */
    .chart-container {{
        background-color: {colors["card_bg"]};
        border: 1px solid {colors["border"]};
        border-radius: 8px;
        padding: 1rem;
    }}

    /* Status indicators */
    .status-indicator {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 16px;
        font-size: 0.75rem;
        font-weight: 500;
    }}

    .status-loading {{
        background-color: rgba(249, 168, 37, 0.2);
        color: #f9a825;
    }}

    .status-success {{
        background-color: rgba(56, 142, 60, 0.2);
        color: #388e3c;
    }}

    .status-error {{
        background-color: rgba(211, 47, 47, 0.2);
        color: #d32f2f;
    }}

    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* Scrollbar styling */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: {colors["scrollbar_track"]};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {colors["scrollbar_thumb"]};
        border-radius: 4px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {colors["scrollbar_thumb_hover"]};
    }}

    /* Divider */
    hr {{
        border: none;
        border-top: 1px solid {colors["border"]};
        margin: 1rem 0;
    }}

    /* Section headers in sidebar */
    .sidebar-section {{
        font-size: 0.75rem;
        font-weight: 600;
        color: {colors["text_muted"]};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }}

    /* Asset info card */
    .asset-info-card {{
        background-color: {colors["card_bg"]};
        border: 1px solid {colors["border"]};
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }}

    .asset-symbol {{
        font-size: 1.25rem;
        font-weight: 700;
        color: {colors["text_primary"]};
    }}

    .asset-price {{
        font-size: 1.5rem;
        font-weight: 600;
    }}

    .price-up {{ color: #388e3c; }}
    .price-down {{ color: #d32f2f; }}

    /* Metrics */
    [data-testid="stMetricValue"] {{
        font-size: 1.25rem;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0;
        background-color: {colors["tab_bg"]};
        border-radius: 8px;
        padding: 0.25rem;
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border-radius: 6px;
        color: {colors["text_muted"]};
        padding: 0.5rem 1rem;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {colors["tab_selected_bg"]};
        color: {colors["text_primary"]};
    }}

    /* Front Page Styles */
    .front-page {{
        text-align: center;
        padding: 3rem 0 1.5rem 0;
    }}

    .front-page-features {{
        list-style: none;
        padding: 0;
        margin: 0 0 2rem 0;
        display: inline-block;
        text-align: left;
    }}

    .front-page-features li {{
        color: {colors["text_muted"]};
        font-size: 0.9rem;
        padding: 0.3rem 0;
        padding-left: 1.25rem;
        position: relative;
    }}

    .front-page-features li::before {{
        content: "✦";
        position: absolute;
        left: 0;
        color: {colors["primary"]};
        font-size: 0.6rem;
        top: 0.45rem;
    }}

    .front-page-logo {{
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1976d2 0%, #7c4dff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.25rem;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }}

    .front-page-headline {{
        font-size: 1.4rem;
        font-weight: 600;
        color: {colors["text_primary"]};
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }}

    .front-page-tagline {{
        font-size: 1.05rem;
        color: {colors["text_muted"]};
        margin-bottom: 1.75rem;
    }}

    .tagline-highlight {{
        color: {colors["primary"]};
        font-weight: 600;
    }}

    .cta-text {{
        color: {colors["cta_text"]};
        font-size: 0.9rem;
        margin: 0 0 0.5rem 0;
    }}

    .front-page-link {{
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }}

    .front-page-link a {{
        color: {colors["primary"]};
        font-size: 0.85rem;
        text-decoration: none;
    }}

    .front-page-link a:hover {{
        text-decoration: underline;
    }}

    /* Video card */
    .video-card-label {{
        text-align: center;
        color: {colors["text_muted"]};
        font-size: 0.8rem;
        font-weight: 500;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        padding-top: 1rem;
    }}

    [data-testid="stVideo"] {{
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(25, 118, 210, 0.12);
        border: 1px solid {colors["border"]};
    }}

    /* Sidebar tagline */
    .sidebar-tagline {{
        color: {colors["text_muted"]};
        font-size: 0.875rem;
        margin-top: 0.25rem;
    }}

    /* Theme toggle button */
    .theme-toggle-btn {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        margin: 0 auto;
        padding: 0.3rem 0.8rem;
        border-radius: 16px;
        font-size: 0.8rem;
        font-weight: 500;
        cursor: pointer;
        background-color: {colors["secondary_bg"]};
        color: {colors["text_muted"]};
        border: 1px solid {colors["border"]};
    }}

</style>
"""


def inject_custom_css(theme_mode: str = "light"):
    """Inject custom CSS into the Streamlit app."""
    import streamlit as st

    colors = DARK_COLORS if theme_mode == "dark" else LIGHT_COLORS
    st.markdown(_build_css(colors), unsafe_allow_html=True)


def get_tool_call_html(tool_name: str, content: str, tool_type: str = "default") -> str:
    """Generate HTML for tool call display."""
    icons = {
        "think_tool": "brain",
        "write_todos": "list-check",
        "read_todos": "list",
        "task": "cpu",
    }

    container_class = {
        "think_tool": "thinking-container",
        "write_todos": "todo-container",
        "read_todos": "todo-container",
        "task": "task-container",
    }.get(tool_name, "tool-call-container")

    return f"""
    <div class="{container_class}">
        <div class="tool-call-header">
            <span>{tool_name}</span>
        </div>
        <div>{content}</div>
    </div>
    """


def get_todo_html(todos: list) -> str:
    """Generate HTML for todo list display."""
    status_icons = {
        "pending": "[ ]",
        "in_progress": "[~]",
        "completed": "[x]",
    }

    items_html = ""
    for todo in todos:
        status = todo.get("status", "pending")
        content = todo.get("content", "")
        status_class = f"todo-{status.replace('_', '-')}"
        icon = status_icons.get(status, "[ ]")
        items_html += f'<div class="todo-item {status_class}">{icon} {content}</div>'

    return f'<div class="todo-container">{items_html}</div>'
