from src.prompts.technical_analysis_prompts import (ema_agent_system_prompt_template, 
                                                    rsi_agent_system_prompt_template, 
                                                    macd_agent_system_prompt_template, 
                                                    atr_agent_system_prompt_template,
                                                    user_prompt_template,
                                                    synthesize_agent_system_prompt_template
                                                    )
from src.services.technical.technical_indicator import TechnicalIndicatorService
from src.models.technical_analysis_model import TechnicalAnalysisInput
from src.utils.technical_context import TechnicalIndicators
from src.utils.llm import invoke_gemini_model, parse_langchain_ai_message
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from typing_extensions import TypedDict, Annotated
import operator
from langchain_core.messages import SystemMessage, HumanMessage
from src.utils.constants import DECIMAL_PLACES
import pandas as pd
from langgraph.config import get_config


system_prompts_map = {
    "ema": ema_agent_system_prompt_template,
    "macd": macd_agent_system_prompt_template,
    "rsi": rsi_agent_system_prompt_template,
    "atr": atr_agent_system_prompt_template
}

# graph state
class TechnicalAnalysisState(TypedDict):
    input: TechnicalAnalysisInput
    current_price: float
    contexts: list[str]
    encoded_images: list[str]
    completed_analysis: Annotated[
        list[str], operator.add
    ]
    final_analysis: str

# worker state
class SingleTechnicalAnalysisState(TypedDict):
    asset: str
    analysis_type: str
    current_price: float
    interval: str
    context: str
    encoded_image: str
    completed_analysis:  Annotated[
        list[str], operator.add
    ]

# node
def create_technical_analysis_charts_and_contexts(state: TechnicalAnalysisState):
    # fetch time series data with technical indicators
    input_data = state["input"]
    asset = input_data.currency_pair.slash_format
    service = TechnicalIndicatorService(
        currency_pair=asset,
        interval=input_data.interval
    )
    df = service.prepare_data(data_source="TwelveData", outputsize=input_data.size)

    # get current price
    try:
        
        current_price = df["Close"].round(DECIMAL_PLACES[asset]).iloc[-1]
    except:
        current_price = df["Close"].iloc[-1]
    
    # prepare charts and contexts
    encoded_images = []
    contexts = []
    for analysis_type in input_data.analysis_types:
        encoded_chart = service.prepare_chart(
            df=df,
            size=input_data.size,
            analysis_type=analysis_type
        )
        encoded_images.append(encoded_chart)

        context = TechnicalIndicators.get_context(df, decimal_places=DECIMAL_PLACES[asset], analysis_type=analysis_type)
        contexts.append(context)
    
    return {"current_price": current_price, "encoded_images": encoded_images, "contexts": contexts}

def create_single_technical_analysis(state: SingleTechnicalAnalysisState):
    config = get_config()
    analysis_type = state["analysis_type"]

    # prepare system message
    if analysis_type in system_prompts_map:
        system_prompt = system_prompts_map[analysis_type].format(
            interval=state["interval"], asset=state["asset"]
        )
        system_message = SystemMessage(content=system_prompt)
    else:
        raise ValueError(f"Unsupported analysis type: {analysis_type}")
    
    # prepare human message
    text_prompt = user_prompt_template.format(
            asset=state["asset"],
            current_price=state["current_price"],
            context=state["context"]
    )
    human_message = HumanMessage(
        content=[
            {"type": "text", "text": text_prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{state['encoded_image']}"},
            },
        ]
    )

    # invoke LLM
    model_type = config["configurable"].get("model_type", "2.5_flash")
    include_paid_key = config["configurable"].get("include_paid_key", False)

    ai_msg = invoke_gemini_model(
        input=[system_message, human_message],
        model_type=model_type,
        include_paid_key=include_paid_key,
    )
    answer = parse_langchain_ai_message(ai_msg)

    return {"completed_analysis": [answer]}

def synthesize_final_technical_analysis(state: TechnicalAnalysisState):
    if len(state["completed_analysis"]) == 1:
        return {"final_analysis": state["completed_analysis"][0]}
    
    if len(state["completed_analysis"]) == 0:
        return {"final_analysis": "No technical analysis was performed."}

    # get config
    config = get_config()
    model_type = config["configurable"].get("model_type", "2.5_flash")
    include_paid_key = config["configurable"].get("include_paid_key", False)

    # prepare system message and human message
    analysis_types = state["input"].analysis_types
    completed_analyses = state["completed_analysis"]
    analyses = ""
    for analysis_type, completed_analysis in zip(analysis_types, completed_analyses):
        # create xml like block with analysis as root, then analysis type and content as children
        analyses += f"<analysis>\n<agent>{analysis_type.upper()} Agent</agent>\n<content>{completed_analysis}</content>\n</analysis>\n"

    system_prompt = synthesize_agent_system_prompt_template.format(
        number=len(analysis_types),
        analysis_types=", ".join(analysis_types),
        asset=state["input"].currency_pair.slash_format,
        interval=state["input"].interval,
        analyses=analyses,
        size=state["input"].size
    )

    system_message = SystemMessage(content=system_prompt)
    human_message = HumanMessage(content="Start your synthesis of the above analyses.")

    # invoke LLM
    ai_msg = invoke_gemini_model(
        input=[system_message, human_message],
        model_type=model_type,
        include_paid_key=include_paid_key,
    )
    answer = parse_langchain_ai_message(ai_msg)

    return {"final_analysis": answer}

# conditional edge 
def assign_technical_analysis(state: TechnicalAnalysisState):
    sends = []
    analysis_types = state["input"].analysis_types
    contexts = state["contexts"]
    encoded_images = state["encoded_images"]
    for analysis_type, context, encoded_image in zip(analysis_types, contexts, encoded_images):
        sends.append(
            Send(
                "create_single_technical_analysis",
                {
                    "asset": state["input"].currency_pair.slash_format,
                    "analysis_type": analysis_type,
                    "current_price": state["current_price"],
                    "interval": state["input"].interval,
                    "context": context,
                    "encoded_image": encoded_image,
                },
            )
        )
    return sends

# build workflow graph
technical_analysis_builder = StateGraph(TechnicalAnalysisState)

# add nodes
technical_analysis_builder.add_node(
    "create_technical_analysis_charts_and_contexts",
    create_technical_analysis_charts_and_contexts,
)
technical_analysis_builder.add_node(
    "create_single_technical_analysis",
    create_single_technical_analysis,
)
technical_analysis_builder.add_node(
    "synthesize_final_technical_analysis",
    synthesize_final_technical_analysis,
)

# add edges
technical_analysis_builder.add_edge(START, "create_technical_analysis_charts_and_contexts")
technical_analysis_builder.add_conditional_edges(
    "create_technical_analysis_charts_and_contexts",
    assign_technical_analysis,
    ["create_single_technical_analysis"]
)
technical_analysis_builder.add_edge("create_single_technical_analysis", "synthesize_final_technical_analysis")
technical_analysis_builder.add_edge("synthesize_final_technical_analysis", END)

# compile graph
technical_analysis_graph = technical_analysis_builder.compile()


