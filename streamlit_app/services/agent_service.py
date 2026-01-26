"""Agent service for handling orchestrator agent streaming."""

import asyncio
from typing import AsyncGenerator, Any
from dataclasses import dataclass

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from src.agents.orchestrator import orchestrator_agent
from src.states_and_contexts.technical_analysis import OrchestratorContext


@dataclass
class StreamEvent:
    """Represents a streaming event from the agent."""
    event_type: str  # "tool_call", "tool_result", "text", "thinking", "todos", "task", "done"
    content: Any
    tool_name: str | None = None
    tool_call_id: str | None = None  # For matching task results to task calls


async def stream_agent_response(
    query: str,
    context: OrchestratorContext,
    thread_id: str,
) -> AsyncGenerator[StreamEvent, None]:
    """
    Stream agent responses with tool calls and results.

    Args:
        query: User's question
        context: OrchestratorContext with API key and config
        thread_id: Unique identifier for the conversation thread

    Yields:
        StreamEvent objects for each event (tool calls, results, text)
    """
    human_message = HumanMessage(content=query)

    try:
        # Use stream_mode="updates" to get step-by-step updates
        async for event in orchestrator_agent.astream(
            {"messages": [human_message]},
            config={"configurable": {"thread_id": thread_id}},
            context=context,
            stream_mode="updates"
        ):
            # Process each node's output
            for node_name, node_output in event.items():
                if "messages" in node_output:
                    for msg in node_output["messages"]:
                        for event in process_message(msg, node_name):
                            yield event

                # Handle todo updates
                if "todos" in node_output:
                    yield StreamEvent(
                        event_type="todos",
                        content=node_output["todos"]
                    )

        yield StreamEvent(event_type="done", content=None)

    except Exception as e:
        yield StreamEvent(
            event_type="error",
            content=str(e)
        )


def process_message(msg: Any, node_name: str) -> list[StreamEvent]:
    """Process a message and yield appropriate events."""
    events = []
    has_task_calls = False

    if isinstance(msg, AIMessage):
        # Check for tool calls
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tool_call in msg.tool_calls:
                tool_name = tool_call.get("name", "unknown")
                tool_args = tool_call.get("args", {})
                tool_call_id = tool_call.get("id")  # Get tool call ID for matching

                # Categorize tool calls
                if tool_name == "think_tool":
                    events.append(StreamEvent(
                        event_type="thinking",
                        content=tool_args.get("reflection", ""),
                        tool_name=tool_name,
                        tool_call_id=tool_call_id
                    ))
                elif tool_name == "write_todos":
                    events.append(StreamEvent(
                        event_type="tool_call",
                        content=tool_args,
                        tool_name=tool_name,
                        tool_call_id=tool_call_id
                    ))
                elif tool_name == "read_todos":
                    # Skip read_todos - don't show in UI
                    pass
                elif tool_name == "task":
                    has_task_calls = True
                    events.append(StreamEvent(
                        event_type="task",
                        content=tool_args,
                        tool_name=tool_name,
                        tool_call_id=tool_call_id
                    ))
                else:
                    events.append(StreamEvent(
                        event_type="tool_call",
                        content=tool_args,
                        tool_name=tool_name,
                        tool_call_id=tool_call_id
                    ))

            # After all tool calls processed, if we had task calls, emit a signal
            if has_task_calls:
                events.append(StreamEvent(
                    event_type="tasks_collected",
                    content=None
                ))

        # Check for text content (final response)
        if msg.content and not msg.tool_calls:
            events.append(StreamEvent(
                event_type="text",
                content=msg.content
            ))

    elif isinstance(msg, ToolMessage):
        # Tool result - skip results for think_tool, write_todos, read_todos
        tool_name = msg.name if hasattr(msg, "name") else None
        tool_call_id = msg.tool_call_id if hasattr(msg, "tool_call_id") else None
        if tool_name not in ["think_tool", "write_todos", "read_todos"]:
            events.append(StreamEvent(
                event_type="tool_result",
                content=msg.content,
                tool_name=tool_name,
                tool_call_id=tool_call_id
            ))

    return events


def run_agent_sync(
    query: str,
    context: OrchestratorContext,
    thread_id: str,
    event_callback: callable
) -> str:
    """
    Run agent synchronously with callback for streaming events.

    This bridges async streaming to Streamlit's sync context.

    Args:
        query: User's question
        context: OrchestratorContext
        thread_id: Unique identifier for the conversation thread
        event_callback: Function to call with each StreamEvent

    Returns:
        Final response text
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    final_response = ""

    async def run():
        nonlocal final_response
        async for event in stream_agent_response(query, context, thread_id):
            event_callback(event)
            if event.event_type == "text":
                final_response = event.content

    try:
        loop.run_until_complete(run())
    finally:
        loop.close()

    return final_response


def create_context(
    gemini_api_key: str,
    min_research_iterations: int = 2,
    max_research_iterations: int = 6,
    max_concurrent_tasks: int = 4,
    asset_type: str | None = None,
) -> OrchestratorContext:
    """Create an OrchestratorContext with the given API key and settings."""
    return OrchestratorContext(
        api_key=gemini_api_key,
        min_research_iterations=min_research_iterations,
        max_research_iterations=max_research_iterations,
        max_concurrent_tasks=max_concurrent_tasks,
        asset_type=asset_type,
    )
