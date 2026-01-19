# Tradable Mind

AI-powered technical analysis platform using an **Orchestrator + Subagents** multi-agent framework built with LangGraph, LangChain, and Google Gemini.

## Overview

Tradable Mind is an intelligent trading assistant that analyzes financial charts and market data through coordinated AI agents. The system uses a multi-agent architecture where an Orchestrator Agent decomposes complex trading queries and delegates tasks to specialized Chart and Quant agents.

## Features

- **Multi-agent architecture** - Orchestrator coordinates Chart and Quant agents for comprehensive analysis
- **Vision-based chart analysis** - Gemini's multimodal capabilities for objective chart interpretation
- **Quantitative analysis** - Data-driven analysis with sandboxed Python code execution
- **Multiple technical indicators** - EMA, RSI, MACD, ATR, Bollinger Bands, Pivot Points, Fibonacci Levels
- **Interactive web interface** - Streamlit app with real-time chart visualization and AI chat
- **Multi-asset support** - Forex, crypto, and commodities via TwelveData

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- TwelveData API key
- Google Gemini API key

## Installation

```bash
uv sync
```

## Configuration

Create a `.env` file in the project root:

```env
TD_API_KEY=your_twelvedata_api_key
GEMINI_API_KEY=your_gemini_api_key
```

## Usage

### CLI

```bash
uv run python main.py
```

### Streamlit Web App

```bash
uv run streamlit run streamlit_app/app.py
```

The web app provides:
- Interactive Plotly candlestick charts with indicator overlays
- AI chat interface with streaming agent responses
- Real-time visualization of agent thinking, todos, and task delegations

## Architecture

### Agent Hierarchy

```
Orchestrator Agent (Strategic Planner)
├── Chart Description Agent (Objective visual analysis)
├── Chart Analysis Agent (Technical interpretation)
└── Quant Agent (Data-driven quantitative analysis)
```

### 4-Phase Workflow

1. **Investigation Design** - Orchestrator decomposes trading query, creates TODO plan
2. **Agent Delegation** - Parallel task execution to Chart/Quant agents
3. **Adaptive Planning** - Reflection via think_tool, dynamic TODO updates after each agent response
4. **Knowledge Synthesis** - Integrate findings, resolve conflicts, provide actionable output

## Project Structure

```
src/
├── agents/                     # Agent definitions
│   ├── orchestrator.py         # Master coordinator with TODO, think, and task tools
│   ├── chart_agent.py          # Vision agents for chart description and analysis
│   └── quant_agent.py          # Quantitative agent with data and code execution
├── tools/                      # Agent tools
│   ├── task_tool.py            # Delegates to Chart or Quant agents
│   ├── quant_tools.py          # download_market_data() and write_code()
│   ├── todo_tools.py           # write_todos() and read_todos()
│   └── think_tool.py           # Strategic reflection checkpoint
├── states_and_contexts/        # State schemas and context configs
│   └── technical_analysis.py
├── prompts/                    # System prompts for all agents
│   └── technical_analysis.py
├── services/
│   ├── asset_metadata.py       # Asset metadata with caching
│   ├── scenario/               # Hypothesis testing modules
│   └── technical/
│       └── technical_indicator.py  # OHLC data and chart generation
└── utils/
    ├── charts.py               # Matplotlib/mplfinance chart generation
    ├── llm.py                  # Gemini API integration
    ├── technical_context.py    # Technical indicator context extraction
    └── twelve_data.py          # TwelveData market data client

streamlit_app/
├── app.py                      # Main entry point
├── components/
│   ├── chart.py                # Plotly candlestick charts with indicators
│   ├── chat.py                 # Chat interface with streaming agent display
│   └── sidebar.py              # Settings panel
├── services/
│   ├── agent_service.py        # Agent streaming with StreamEvent handling
│   └── data_service.py         # TwelveData API client with caching
└── utils/
    └── styles.py               # CSS styles and chart colors
```

## Supported Indicators

- **EMA** - Exponential Moving Average
- **RSI** - Relative Strength Index
- **MACD** - Moving Average Convergence Divergence
- **ATR** - Average True Range
- **Bollinger Bands**
- **Pivot Points**
- **Fibonacci Levels**

## License

This project is licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE).

You are free to use, modify, and distribute this software for **personal and non-commercial purposes** only. Commercial use requires a separate license from the author.
