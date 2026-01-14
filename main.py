# from src.services.technical.technical_analysis_graph import technical_analysis_graph
# from src.models.technical_analysis_model import TechnicalAnalysisInput
# from src.models.currency import Currency, CurrencyPair

# pair = CurrencyPair(base=Currency.EUR, quote=Currency.USD)
# input_data = TechnicalAnalysisInput(
#     currency_pair=pair,
#     intervals=["15min", "1h", "4h", "1day"],
#     size=80,
#     #end_date="2025-12-24 14:00:00",
#     analysis_types=["ema"]
#     #analysis_types=["pivot", "fibonacci", "ema", "rsi", "macd", "atr", "bb"]
# )

# config = {
#     "configurable": {
#         "model_type": "3_flash",
#         "include_paid_key": True
#     }
# }


# state = technical_analysis_graph.invoke(
#     {"input": input_data},
#     config=configI wan
# )
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

from langchain_core.messages import HumanMessage

from src.agents.orchestrator import orchestrator_agent
from src.states_and_contexts.technical_analysis import OrchestratorContext
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

context = OrchestratorContext(
    api_key=os.getenv("GEMINI_API_KEY"),
    min_research_iterations=2,
    max_research_iterations=10,
    max_concurrent_tasks=4
)

async def main(query: str):
    human_message = HumanMessage(content=query)
    result = await orchestrator_agent.ainvoke(
        {"messages": [human_message]},
        context=context
    )
    return result

query = "I'm considering a short position for a day trade for EUR/USD. What's the setup quality and what should I watch for?"
#query = "I'm looking at AAPL on the 1-hour chart. What Should I do?"
query = (
    "I am long term for AI stocks. But NVIDIA seems bumpy recently.",
    "Give me a comprehensive technical analysis on the daily and weekly intervals.",
)
query = "What will be the most successful strategy for trading USD/JPY for the last 3 months. As a day trader. The symbol is USD/JPY."
asyncio.run(main(query=query))
