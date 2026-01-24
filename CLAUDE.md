# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

```bash
uv sync                                  # Install dependencies
uv run python main.py                    # Run the orchestrator agent (CLI)
uv run streamlit run streamlit_app/app.py # Run the Streamlit web app
```

Package manager: `uv` (lock file: `uv.lock`)

## Environment Setup

Requires `.env` file with:
- `TD_API_KEY` - TwelveData API key for market data
- `GEMINI_API_KEY` - Google Gemini API key

## Architecture

**Tradable Mind** is an AI-powered technical analysis platform using an **Orchestrator + Subagents** multi-agent framework built with LangGraph, LangChain and Google Gemini.

### Agent Hierarchy

```
Orchestrator Agent (Strategic Planner)
├── Chart Description Agent (Objective visual analysis)
├── Chart Analysis Agent (Technical interpretation)
└── Quant Agent (Data-driven quantitative analysis)
```

### 4-Phase Workflow

1. **Investigation Design**: Orchestrator decomposes trading query, creates TODO plan
2. **Agent Delegation**: Parallel task execution to Chart/Quant agents
3. **Adaptive Planning**: Reflection via `think_tool`, dynamic TODO updates after each agent response
4. **Knowledge Synthesis**: Integrate findings, resolve conflicts, provide actionable output

### Key Components

**Agents** (`src/agents/`)
- `orchestrator.py` - Master coordinator with TODO, think, and task tools
- `chart_agent.py` - Two vision agents for chart description and analysis
- `quant_agent.py` - Quantitative agent with data download and code execution

**Tools** (`src/tools/`)
- `task_tool.py` - Delegates to Chart or Quant agents
- `quant_tools.py` - `download_market_data()` and `write_code()` (sandboxed Python)
- `todo_tools.py` - `write_todos()` and `read_todos()` for investigation tracking
- `think_tool.py` - Strategic reflection checkpoint

**States & Contexts** (`src/states_and_contexts/`)
- `technical_analysis.py` - State schemas (OrchestratorState, QuantAgentState) and context configs

**Prompts** (`src/prompts/`)
- `technical_analysis.py` - System prompts for all agents (Orchestrator, Chart, Quant)
- `technical_analysis_prompts.py` - Legacy indicator-specific prompts (deprecated)

**Services**
- `src/services/technical/technical_indicator.py` - OHLC data fetching and chart generation
- `src/services/asset_metadata.py` - Asset metadata management with caching
- `src/services/scenario/` - Hypothesis testing modules (backtesting scenarios)

**Utilities**
- `src/utils/twelve_data.py` - TwelveData market data client
- `src/utils/charts.py` - Matplotlib/mplfinance chart generation
- `src/utils/technical_context.py` - Technical indicator context extraction
- `src/utils/llm.py` - Gemini API integration

### Supported Indicators

EMA, RSI, MACD, ATR, Bollinger Bands, Pivot Points, Fibonacci Levels

## Streamlit Web Application

Interactive web interface for technical analysis at `streamlit_app/`.

### App Structure

```
streamlit_app/
├── app.py                    # Main entry point with front page and main app flow
├── token_counter.py          # Standalone token counting utility (tiktoken-based)
├── components/
│   ├── chart.py              # Plotly candlestick charts with indicators
│   ├── chat.py               # Chat interface with streaming and iteration grouping
│   └── sidebar.py            # Settings panel (symbol, interval, indicators)
├── services/
│   ├── agent_service.py      # Agent streaming with StreamEvent handling
│   └── data_service.py       # TwelveData API client with caching
└── utils/
    └── styles.py             # CSS styles (light theme) and chart color config
```

### Key Features

- **Front Page Flow**: Landing page with API key input, transitions to main app on entry
- **Interactive Charts**: Plotly-based candlestick charts with EMA, BB, RSI, MACD, ATR, Volume overlays
- **Pivot Points Display**: Inline price header showing R1-R3/S1-S3 levels when enabled
- **Daily Change**: Shows daily price change (not interval change) in the header
- **Weekend Filtering**: Automatically filters out Saturday/Sunday data from charts
- **Agent Configuration**: Configurable min/max research iterations and parallel task limits
- **Conversation Threading**: Maintains `thread_id` for conversation continuity across messages
- **Streaming UI Lock**: Disables sidebar controls during agent streaming with pending action queue

### Streaming Architecture

`agent_service.py` emits `StreamEvent` objects with types:
- `thinking` - Reflection from think_tool
- `tool_call` - Tool invocations (write_todos, etc.)
- `task` - Task delegations to Chart/Quant agents
- `tasks_collected` - Signal that all task calls in a batch are collected
- `tool_result` - Results matched to calls via `tool_call_id`
- `todos` - TODO list updates
- `text` - Final agent response
- `done` - Stream completion signal
- `error` - Error events

### Investigation Rounds

`chat.py` groups task delegations into "Investigation Rounds" with:
- Real-time iteration headers showing agent counts (📊 Chart, 🔢 Quant)
- Completion tracking (e.g., "2/4 Complete")
- Expandable details with task descriptions and results
- Results update in-place as agents complete

### Session State

Key session state variables managed in `app.py`:
- `chart_data`, `current_symbol`, `current_interval` - Chart state
- `current_indicators` - Selected indicators (passed to AI context)
- `gemini_api_key` - API key from front page
- `min/max_research_iterations`, `max_concurrent_tasks` - Agent config
- `thread_id` - Unique conversation thread ID
- `is_streaming` - Lock flag during agent execution
- `pending_*` - Queued actions (load chart, clear conversation, prompt)
