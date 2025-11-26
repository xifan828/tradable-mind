from src.services.technical.technical_analysis_graph import technical_analysis_graph
from src.models.technical_analysis_model import TechnicalAnalysisInput
from src.models.currency import Currency, CurrencyPair

pair = CurrencyPair(base=Currency.EUR, quote=Currency.USD)
input_data = TechnicalAnalysisInput(
    currency_pair=pair,
    interval="1h",
    size=96,
    analysis_types=["ema", "rsi", "macd", "atr"]
)

state = technical_analysis_graph.invoke(
    {"input": input_data}
)

#print(state["final_analysis"])