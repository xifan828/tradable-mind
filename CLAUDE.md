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
├── app.py                    # Main entry point
├── components/
│   ├── chart.py              # Plotly candlestick charts with indicators
│   ├── chat.py               # Chat interface with streaming agent display
│   └── sidebar.py            # Settings panel (API key, symbol, indicators)
├── services/
│   ├── agent_service.py      # Agent streaming with StreamEvent handling
│   └── data_service.py       # TwelveData API client with caching
└── utils/
    └── styles.py             # CSS styles and chart color config
```

### Key Features

- **Interactive Charts**: Plotly-based candlestick charts with EMA, BB, RSI, MACD, ATR overlays
- **AI Chat Interface**: Streams orchestrator agent responses with real-time tool visualization
- **Tool Display**: Shows think_tool, write_todos, and task delegations with results in expandable sections
- **Session State**: Manages chat history, pending tasks (keyed by tool_call_id), and chart data

### Streaming Architecture

`agent_service.py` emits `StreamEvent` objects with types:
- `thinking` - Reflection from think_tool
- `tool_call` - Tool invocations (write_todos, etc.)
- `task` - Task delegations to Chart/Quant agents
- `tool_result` - Results matched to calls via `tool_call_id`
- `text` - Final agent response (extracted from `content[0]["text"]`)

`chat.py` renders events with visual separators and tracks pending tasks to display results in their corresponding sections.
