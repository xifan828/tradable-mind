from langchain_google_genai import ChatGoogleGenerativeAI
import os
import random
from langchain_core.messages import AnyMessage, AIMessage
from typing import Literal

free_keys = [
    os.getenv("GEMINI_API_KEY_XIFAN_1"),
    os.getenv("GEMINI_API_KEY_XIFAN_2"),
    os.getenv("GEMINI_API_KEY_XIFAN_3"),
    os.getenv("GEMINI_API_KEY_XIFAN_4"),
    os.getenv("GEMINI_API_KEY_CONG_1"),
    os.getenv("GEMINI_API_KEY_CONG_2"),
]

paid_keys = [
    os.getenv("GEMINI_API_KEY"),
]

gemini_model_map = {
    "2.5_pro": "models/gemini-2.5-pro",
    "2.5_flash": "models/gemini-flash-latest",
    "3_pro": "models/gemini-3-pro-preview",
}

async def invoke_gemini_model(
    input: str | list[AnyMessage] | list[tuple[str, str]],
    model_type: Literal["2.5_pro", "2.5_flash", "3_pro"],
    include_paid_key: bool = False,
    **llm_kwargs,
) -> AIMessage:
    
    if model_type not in gemini_model_map:
        raise ValueError(f"Unsupported model type: {model_type}")

    free_pool = [key for key in free_keys if key]
    random.shuffle(free_pool)

    keys_to_try = list(free_pool)
    if include_paid_key:
        keys_to_try.extend(key for key in paid_keys if key)

    last_error: Exception | None = None

    for key in keys_to_try:
        llm = ChatGoogleGenerativeAI(
            model=gemini_model_map[model_type],
            api_key=key,
            max_retries=0,
            **llm_kwargs,
        )

        try:
            response = await llm.ainvoke(input)
            return response
        except Exception as exc:
            last_error = exc

    if last_error is not None:
        raise RuntimeError("All configured Gemini API keys failed") from last_error

    raise RuntimeError("No Gemini API keys configured")














