from pydantic import BaseModel
from src.models.currency import CurrencyPair
from typing import Literal

class TechnicalAnalysisInput(BaseModel):
    currency_pair: CurrencyPair
    interval: Literal["1min", "5min", "1h", "4h", "1day"]
    size: int
    analysis_types: list[Literal["ema", "rsi", "macd", "atr"]]