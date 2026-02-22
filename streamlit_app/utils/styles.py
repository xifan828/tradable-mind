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
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

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

    /* --- New Landing Page --- */

    /* Hero left column */
    .lp-hero-left {{ padding: 3rem 0 2rem 0; }}

    /* Badge pill */
    .lp-badge {{
        display: inline-flex; align-items: center; gap: 0.5rem;
        padding: 0.25rem 0.75rem; border-radius: 9999px;
        background: rgba(25,118,210,0.1); border: 1px solid rgba(25,118,210,0.2);
        color: #1152d4; font-size: 0.75rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.05em;
        margin-bottom: 1.5rem;
    }}
    .lp-badge-dot {{
        width: 8px; height: 8px; border-radius: 50%; background: #1152d4;
        box-shadow: 0 0 0 3px rgba(17,82,212,0.25);
        animation: lp-ping 1.5s ease-in-out infinite;
    }}
    @keyframes lp-ping {{
        0%, 100% {{ box-shadow: 0 0 0 3px rgba(17,82,212,0.25); }}
        50%       {{ box-shadow: 0 0 0 6px rgba(17,82,212,0.0); }}
    }}

    /* Hero title */
    .lp-title {{
        font-size: clamp(2.2rem, 4vw, 3.8rem);
        font-weight: 900; line-height: 1.1; letter-spacing: -0.02em;
        color: {colors["text_primary"]}; margin-bottom: 1.25rem;
    }}
    .lp-title-accent {{ color: #1152d4; font-style: italic; }}
    .lp-subtitle {{ font-size: clamp(1.4rem, 2.5vw, 2.4rem); font-weight: 700; color: #1152d4; font-style: italic; line-height: 1.2; margin-top: 0 !important; margin-bottom: 1.25rem; }}

    /* Hero description */
    .lp-desc {{
        font-size: 1.05rem; color: {colors["text_muted"]};
        line-height: 1.7; margin-bottom: 1.75rem;
    }}

    /* API key link */
    .lp-api-link {{ margin-top: 0.75rem; }}
    .lp-api-link a {{
        color: #1152d4; font-size: 0.85rem; font-weight: 500; text-decoration: none;
    }}
    .lp-api-link a:hover {{ text-decoration: underline; }}
    .lp-api-note {{
        display: block; margin-top: 0.35rem; font-size: 0.8rem;
        color: #b45309; font-weight: 500;
    }}

    /* Right column: browser mockup */
    .lp-mockup-wrapper {{
        position: relative; padding: 3rem 0 2rem 1rem;
    }}
    .lp-mockup-glow {{
        position: absolute; inset: -4px; border-radius: 18px;
        background: linear-gradient(135deg, rgba(17,82,212,0.25), rgba(37,99,235,0.25));
        filter: blur(8px); opacity: 0.4;
    }}
    .lp-mockup {{
        position: relative; background: #ffffff; border: 1px solid #e2e8f0;
        border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.12);
        overflow: hidden; aspect-ratio: 16/10;
    }}
    .lp-mockup-chrome {{
        display: flex; align-items: center; justify-content: space-between;
        padding: 0.6rem 1rem;
        background: #f8fafc; border-bottom: 1px solid #e2e8f0;
    }}
    .lp-mockup-chrome-only {{
        display: flex; align-items: center; justify-content: space-between;
        padding: 0.6rem 1rem;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-bottom: none;
        border-radius: 16px 16px 0 0;
    }}
    .lp-mockup-dots {{ display: flex; gap: 5px; }}
    .lp-mockup-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
    .lp-mockup-title {{
        font-size: 0.6rem; letter-spacing: 0.15em; color: #94a3b8;
        text-transform: uppercase; font-family: monospace;
    }}
    .lp-mockup-body {{ display: flex; height: calc(100% - 36px); }}
    .lp-mockup-sidebar {{
        width: 48px; background: #f8fafc; border-right: 1px solid #e2e8f0;
        display: flex; flex-direction: column; align-items: center;
        padding: 0.75rem 0; gap: 1rem;
    }}
    .lp-mockup-icon {{
        width: 28px; height: 28px; border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.9rem;
    }}
    .lp-mockup-icon.active {{ background: rgba(17,82,212,0.1); color: #1152d4; }}
    .lp-mockup-icon.inactive {{ color: #94a3b8; }}
    .lp-mockup-content {{
        flex: 1; position: relative; overflow: hidden;
        background: #0f172a;
    }}
    .lp-mockup-chart-bg {{
        position: absolute; inset: 0; width: 100%; height: 100%;
        object-fit: cover; opacity: 0.35;
    }}
    .lp-mockup-overlay {{
        position: absolute; inset: 0; display: flex; flex-direction: column;
        justify-content: center; padding: 1rem; gap: 0.75rem;
    }}
    .lp-mockup-card {{
        background: rgba(255,255,255,0.92); border-radius: 10px;
        border: 1px solid rgba(17,82,212,0.2); padding: 0.75rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2); max-width: 75%;
    }}
    .lp-mockup-card-header {{
        display: flex; align-items: center; gap: 0.4rem;
        margin-bottom: 0.5rem;
        font-size: 0.6rem; font-weight: 700; text-transform: uppercase; color: #1e293b;
    }}
    .lp-mockup-card-dot {{ color: #1152d4; font-size: 0.7rem; }}
    .lp-mockup-bar {{
        height: 5px; border-radius: 3px; margin-bottom: 4px;
    }}
    .lp-mockup-confidence {{
        background: #1152d4; color: white; border-radius: 8px;
        padding: 0.5rem 0.75rem; font-size: 0.6rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.1em;
        text-align: center; align-self: flex-end; max-width: 100px;
    }}

    /* Features section */
    .lp-features-section {{
        padding: 4rem 1rem; background: transparent;
    }}
    .lp-features-eyebrow {{
        color: #1152d4; font-size: 0.75rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem;
    }}
    .lp-features-heading {{
        font-size: clamp(1.75rem, 3vw, 2.75rem); font-weight: 900;
        color: {colors["text_primary"]}; letter-spacing: -0.02em; line-height: 1.15;
        margin-bottom: 0.75rem; max-width: 600px;
    }}
    .lp-features-desc {{
        font-size: 1rem; color: {colors["text_muted"]}; line-height: 1.7;
        max-width: 600px; margin-bottom: 2.5rem;
    }}
    .lp-cards-grid {{
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;
    }}
    .lp-card {{
        background: {colors["card_bg"]}; border: 1px solid {colors["border"]}; border-radius: 16px;
        padding: 2rem 1.75rem; transition: border-color 0.2s, box-shadow 0.2s;
    }}
    .lp-card:hover {{
        border-color: rgba(17,82,212,0.3);
        box-shadow: 0 12px 40px rgba(17,82,212,0.06);
    }}
    .lp-card-icon {{
        width: 48px; height: 48px; border-radius: 12px;
        background: rgba(17,82,212,0.1); color: #1152d4;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem; margin-bottom: 1.25rem;
    }}
    .material-symbols-outlined {{ font-size: 1.5rem !important; }}
    .lp-card-title {{
        font-size: 1.05rem; font-weight: 700; color: {colors["text_primary"]}; margin-bottom: 0.5rem;
    }}
    .lp-card-desc {{ font-size: 0.9rem; color: {colors["text_muted"]}; line-height: 1.65; }}

    /* Video inside mockup frame */
    .lp-mockup-wrapper + div [data-testid="stVideo"],
    .lp-mockup-wrapper ~ div [data-testid="stVideo"] {{
        border-radius: 0 0 16px 16px !important;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        border-top: none;
        box-shadow: 0 20px 60px rgba(0,0,0,0.12);
        margin-top: 0 !important;
    }}
    .lp-mockup-wrapper ~ div [data-testid="stVideo"] video {{
        display: block;
    }}

    /* Footer */
    .lp-footer {{
        border-top: 1px solid {colors["border"]}; padding: 2.5rem 1rem 1.5rem;
        text-align: center;
    }}
    .lp-footer-logo {{
        display: flex; align-items: center; justify-content: center;
        gap: 0.5rem; margin-bottom: 1rem;
    }}
    .lp-footer-logo-icon {{
        background: #1152d4; color: white; border-radius: 8px;
        width: 28px; height: 28px; display: flex; align-items: center; justify-content: center;
        font-size: 1rem;
    }}
    .lp-footer-logo-text {{ font-weight: 700; color: {colors["text_primary"]}; }}
    .lp-footer-copy {{
        font-size: 0.75rem; color: {colors["text_muted"]}; font-weight: 500;
        text-transform: uppercase; letter-spacing: 0.08em;
    }}
    .lp-footer-disclosure {{
        margin-top: 1.5rem; text-align: left;
        border-top: 1px solid {colors["border"]}; padding-top: 1.5rem;
    }}
    .lp-footer-disclosure-title {{
        font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.1em; color: {colors["text_muted"]}; margin-bottom: 0.75rem;
    }}
    .lp-footer-disclosure-items {{
        display: flex; flex-direction: column; gap: 0.4rem;
    }}
    .lp-footer-disclosure-item {{
        font-size: 0.75rem; color: {colors["text_muted"]}; line-height: 1.6;
    }}
    .lp-footer-disclosure-label {{
        font-weight: 700; color: {colors["text_primary"]};
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
