# Tradable Mind

AI-powered technical analysis platform for currency trading signals using LangGraph and Google Gemini.

## Overview

Tradable Mind analyzes financial charts using computer vision and generates trading signals on a quantitative scale from -1.0 (Strong Sell) to +1.0 (Strong Buy). The system uses a LangGraph-based agentic workflow that processes multiple technical indicators in parallel.

## Features

- **Multi-timeframe analysis** - Analyze across different intervals (1h, 4h, daily, etc.)
- **Multiple technical indicators** - EMA, RSI, MACD, ATR analysis
- **Vision-based interpretation** - Charts processed by Gemini's multimodal capabilities
- **Parallel processing** - Indicators analyzed concurrently for efficiency
- **Multi-asset support** - Forex, crypto, and commodities via TwelveData

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- TwelveData API key
- Google Gemini API key(s)

## Installation

```bash
uv sync
```

## Configuration

Create a `.env` file in the project root:

```env
TD_API_KEY=your_twelvedata_api_key
GEMINI_API_KEY_1=your_gemini_api_key
```

Multiple Gemini API keys are supported for key rotation (e.g., `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3`).

## Usage

```python
from src.services.technical.technical_analysis_graph import technical_analysis_graph
from src.models.technical_analysis_model import TechnicalAnalysisInput
from src.models.currency import Currency, CurrencyPair

pair = CurrencyPair(base=Currency.BTC, quote=Currency.USD)
input_data = TechnicalAnalysisInput(
    currency_pair=pair,
    intervals=["1h", "4h"],
    size=48,
    analysis_types=["ema", "rsi", "macd", "atr"]
)

config = {
    "configurable": {
        "model_type": "3_flash",
        "include_paid_key": True
    }
}

state = technical_analysis_graph.invoke(
    {"input": input_data},
    config=config
)

print("Signal values:", state.get("signal_values"))
print("Final signal:", state.get("final_signal"))
```

Run the demo:

```bash
uv run python main.py
```

## Project Structure

```
src/
├── models/                 # Pydantic models
│   ├── currency.py         # Currency and CurrencyPair definitions
│   └── technical_analysis_model.py
├── prompts/                # LLM prompts
│   └── technical_analysis_prompts.py
├── services/
│   └── technical/
│       └── technical_analysis_graph.py  # LangGraph workflow
└── utils/
    ├── charts.py           # Chart generation with mplfinance
    ├── llm.py              # Gemini API with key rotation
    ├── technical_context.py # Indicator context extraction
    └── twelve_data.py      # TwelveData market data client
```

## How It Works

1. **Data Fetch & Chart Generation** - Fetches OHLC data from TwelveData and generates candlestick charts with technical indicators using mplfinance

2. **Parallel Analysis** - Multiple analysis nodes run concurrently, each focusing on a specific indicator (EMA, RSI, MACD, ATR)

3. **Vision-Based Analysis** - Charts are base64-encoded and sent to Gemini for AI interpretation using specialized prompts

4. **Signal Aggregation** - Individual indicator signals are combined into a final signal ranging from -1.0 (Strong Sell) to +1.0 (Strong Buy)
