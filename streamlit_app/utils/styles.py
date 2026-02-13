"""Dark theme styling for Tradable Mind Streamlit app."""

# Color palette
COLORS = {
    "background": "#0e1117",
    "sidebar": "#1a1a2e",
    "card": "#1e1e2e",
    "border": "#262730",
    "text": "#fafafa",
    "text_muted": "#a0a0a0",
    "primary": "#4a90d9",
    "primary_hover": "#3a7bc8",
    "success": "#26a69a",
    "danger": "#ef5350",
    "warning": "#ffca28",
    "info": "#29b6f6",
}

# Chart colors
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

DARK_THEME_CSS = """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global styles */
    .stApp {
        background-color: #f5f5f5;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #1a1a1a;
    }

    /* Main header styling */
    .main-header {
        background: linear-gradient(90deg, #ffffff 0%, #f5f5f5 100%);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }

    .main-header h1 {
        color: #1a1a1a;
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
    }

    .main-header p {
        color: #666666;
        margin: 0.25rem 0 0 0;
        font-size: 0.875rem;
    }

    /* Chat message styling */
    [data-testid="stChatMessage"] {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border: 1px solid #e0e0e0;
    }

    /* Tool call containers */
    .tool-call-container {
        background-color: #e3f2fd;
        border-left: 3px solid #1976d2;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 6px 6px 0;
        font-size: 0.875rem;
    }

    .tool-call-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        color: #1976d2;
        margin-bottom: 0.5rem;
    }

    .tool-result-container {
        background-color: #e8f5e9;
        border-left: 3px solid #388e3c;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 6px 6px 0;
        font-size: 0.875rem;
    }

    .thinking-container {
        background-color: #fff8e1;
        border-left: 3px solid #f9a825;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 6px 6px 0;
        font-style: italic;
        font-size: 0.875rem;
        color: #666666;
    }

    .task-container {
        background-color: #e0f2f1;
        border-left: 3px solid #00897b;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 6px 6px 0;
        font-size: 0.875rem;
    }

    .todo-container {
        background-color: #f3e5f5;
        border-left: 3px solid #7b1fa2;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 6px 6px 0;
    }

    .todo-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0;
        font-size: 0.875rem;
    }

    .todo-pending { color: #9e9e9e; }
    .todo-in-progress { color: #f9a825; }
    .todo-completed { color: #388e3c; }

    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #1a1a1a;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
    }

    .stTextInput > div > div > input:focus {
        border-color: #1976d2;
        box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2);
    }

    /* Text area styling - natural background */
    .stTextArea > div > div > textarea {
        background-color: #ffffff;
        color: #1a1a1a;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #1976d2;
        box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2);
        background-color: #ffffff;
    }

    /* Select boxes */
    .stSelectbox > div > div {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
    }

    /* Buttons */
    .stButton > button {
        background-color: #1976d2;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: background-color 0.2s;
    }

    .stButton > button:hover {
        background-color: #1565c0;
    }

    .stButton > button:active {
        background-color: #0d47a1;
    }

    /* Secondary buttons - override for natural grey */
    button[kind="secondary"],
    button[data-testid="baseButton-secondary"] {
        background-color: #f5f5f5 !important;
        color: #1a1a1a !important;
        border: 1px solid #e0e0e0 !important;
    }

    button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover {
        background-color: #e0e0e0 !important;
        border-color: #bdbdbd !important;
    }

    button[kind="secondary"]:active,
    button[data-testid="baseButton-secondary"]:active {
        background-color: #d0d0d0 !important;
    }

    button[kind="secondary"]:disabled,
    button[data-testid="baseButton-secondary"]:disabled {
        background-color: #fafafa !important;
        color: #9e9e9e !important;
        border-color: #f0f0f0 !important;
    }

    /* Checkboxes */
    .stCheckbox > label {
        color: #1a1a1a;
    }

    /* Sliders */
    .stSlider > div > div > div {
        background-color: #e0e0e0;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border-radius: 6px;
        border: 1px solid #e0e0e0;
    }

    .streamlit-expanderHeader:hover {
        background-color: #f5f5f5;
    }

    /* Chart container */
    .chart-container {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
    }

    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 16px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .status-loading {
        background-color: rgba(249, 168, 37, 0.2);
        color: #f9a825;
    }

    .status-success {
        background-color: rgba(56, 142, 60, 0.2);
        color: #388e3c;
    }

    .status-error {
        background-color: rgba(211, 47, 47, 0.2);
        color: #d32f2f;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f5f5f5;
    }

    ::-webkit-scrollbar-thumb {
        background: #bdbdbd;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #9e9e9e;
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #e0e0e0;
        margin: 1rem 0;
    }

    /* Section headers in sidebar */
    .sidebar-section {
        font-size: 0.75rem;
        font-weight: 600;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }

    /* Asset info card */
    .asset-info-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .asset-symbol {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1a1a1a;
    }

    .asset-price {
        font-size: 1.5rem;
        font-weight: 600;
    }

    .price-up { color: #388e3c; }
    .price-down { color: #d32f2f; }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.25rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: #f5f5f5;
        border-radius: 8px;
        padding: 0.25rem;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 6px;
        color: #666666;
        padding: 0.5rem 1rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        color: #1a1a1a;
    }

    /* Front Page Styles */
    .front-page {
        text-align: center;
        padding: 4rem 2rem 1rem 2rem;
    }

    .front-page-logo {
        font-size: 2.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1976d2 0%, #7c4dff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }

    .front-page-headline {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }

    .front-page-tagline {
        font-size: 1rem;
        color: #666666;
        margin-bottom: 2rem;
    }

    .tagline-highlight {
        color: #1976d2;
        font-weight: 600;
    }

    .front-page-cta {
        margin-bottom: 0.5rem;
    }

    .cta-text {
        color: #64748b;
        font-size: 0.9rem;
        margin: 0;
    }

    .front-page-link {
        text-align: center;
        margin-top: 1rem;
    }

    .front-page-link a {
        color: #1976d2;
        font-size: 0.85rem;
        text-decoration: none;
    }

    .front-page-link a:hover {
        text-decoration: underline;
    }

</style>
"""


def inject_custom_css():
    """Inject custom CSS into the Streamlit app."""
    import streamlit as st
    st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)


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
