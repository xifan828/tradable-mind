"""Chat interface component with streaming display and task iteration grouping."""

import uuid
from datetime import datetime
import streamlit as st
from typing import Any
from collections import defaultdict

from streamlit_app.services.agent_service import (
    StreamEvent,
    stream_agent_response,
    create_context,
)


def initialize_chat_state():
    """Initialize chat-related session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "is_streaming" not in st.session_state:
        st.session_state.is_streaming = False
    if "pending_tasks" not in st.session_state:
        st.session_state.pending_tasks = {}  # Keyed by tool_call_id
    if "current_iteration" not in st.session_state:
        st.session_state.current_iteration = None  # Current iteration being built
    if "iteration_count" not in st.session_state:
        st.session_state.iteration_count = 0
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())  # Unique ID for conversation


def extract_text_content(content: Any) -> str:
    """Extract text from content - handles both string and list format."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list) and len(content) > 0:
        # Handle format like [{"text": "..."}]
        first_item = content[0]
        if isinstance(first_item, dict) and "text" in first_item:
            return first_item["text"]
    return str(content) if content else ""


def get_agent_icon(task_type: str) -> str:
    """Get icon for agent type."""
    icons = {
        "chart": "📊",
        "chart_description": "🖼️",
        "chart_analysis": "📈",
        "quant": "🔢",
    }
    return icons.get(task_type.lower(), "🎯")


def get_agent_display_name(task_type: str) -> str:
    """Get display name for agent type."""
    names = {
        "chart": "Chart",
        "chart_description": "Chart Description",
        "chart_analysis": "Chart Analysis",
        "quant": "Quant",
    }
    return names.get(task_type.lower(), task_type.title())


def count_agents_by_type(tasks: list) -> dict:
    """Count tasks by agent type."""
    counts = defaultdict(int)
    for task in tasks:
        task_type = task.get("task_args", {}).get("task_type", "unknown")
        # Normalize chart types
        if "chart" in task_type.lower():
            counts["chart"] += 1
        elif "quant" in task_type.lower():
            counts["quant"] += 1
        else:
            counts["other"] += 1
    return dict(counts)


def count_completed_tasks(tasks: list) -> int:
    """Count completed tasks in iteration."""
    return sum(1 for t in tasks if t.get("result") is not None)


def render_iteration_header(iteration_num: int, tasks: list):
    """Render the iteration header with agent counts."""
    agent_counts = count_agents_by_type(tasks)
    completed = count_completed_tasks(tasks)
    total = len(tasks)

    # Build agent count text
    counts_parts = []
    if agent_counts.get("chart", 0) > 0:
        counts_parts.append(f"📊 Chart: {agent_counts['chart']}")
    if agent_counts.get("quant", 0) > 0:
        counts_parts.append(f"🔢 Quant: {agent_counts['quant']}")
    if agent_counts.get("other", 0) > 0:
        counts_parts.append(f"🎯 Other: {agent_counts['other']}")

    counts_text = " | ".join(counts_parts)

    # Status
    if completed == total:
        status = f"✅ {completed}/{total} Complete"
    else:
        status = f"⏳ {completed}/{total} Complete"

    return f"**🔄 Investigation Round {iteration_num}** ({total} tasks) — {counts_text} — {status}"


def render_iteration_details(tasks: list):
    """Render task details inside an expander."""
    for idx, task in enumerate(tasks):
        task_args = task.get("task_args", {})
        result = task.get("result")
        task_type = task_args.get("task_type", "unknown")
        task_desc = task_args.get("task_description", "No description")
        chart_input = task_args.get("chart_analysis_input")

        icon = get_agent_icon(task_type)
        agent_name = get_agent_display_name(task_type)
        status_icon = "✅" if result else "⏳"

        st.markdown(f"**{icon} {agent_name}** {status_icon}")
        st.markdown(f"*{task_desc}*")

        # Parameters if available
        if chart_input and isinstance(chart_input, dict):
            params = ", ".join(f"{k}: {v}" for k, v in chart_input.items())
            st.caption(f"Parameters: {params}")

        # Result if available
        if result:
            st.markdown(result)

        if idx < len(tasks) - 1:
            st.markdown("---")


def render_iteration_section(iteration_num: int, tasks: list, key_suffix: str = ""):
    """Render complete iteration section with header and expandable details."""
    header = render_iteration_header(iteration_num, tasks)

    with st.expander(header, expanded=False):
        render_iteration_details(tasks)


def render_iteration_streaming(iteration_num: int, tasks: list, container, result_placeholders: dict):
    """
    Render iteration during streaming - shows header immediately.
    Returns placeholders for updating results.
    """
    with container:
        # Show header
        header = render_iteration_header(iteration_num, tasks)
        header_placeholder = st.empty()
        header_placeholder.markdown(header)

        # Create expander for details
        with st.expander("📋 View Details", expanded=False):
            for idx, task in enumerate(tasks):
                task_args = task.get("task_args", {})
                task_type = task_args.get("task_type", "unknown")
                task_desc = task_args.get("task_description", "No description")
                chart_input = task_args.get("chart_analysis_input")
                tool_call_id = task.get("tool_call_id")

                icon = get_agent_icon(task_type)
                agent_name = get_agent_display_name(task_type)

                st.markdown(f"**{icon} {agent_name}** ⏳")
                st.markdown(f"*{task_desc}*")

                if chart_input and isinstance(chart_input, dict):
                    params = ", ".join(f"{k}: {v}" for k, v in chart_input.items())
                    st.caption(f"Parameters: {params}")

                # Placeholder for result
                result_placeholder = st.empty()
                if tool_call_id:
                    result_placeholders[tool_call_id] = {
                        "placeholder": result_placeholder,
                        "task": task
                    }

                if idx < len(tasks) - 1:
                    st.markdown("---")

        st.markdown("---")

    return header_placeholder


def render_message(message: dict):
    """Render a single chat message."""
    role = message.get("role", "assistant")
    content = message.get("content", "")
    msg_type = message.get("type", "text")

    with st.chat_message(role):
        if msg_type == "text":
            text = extract_text_content(content)
            st.markdown(text)
        elif msg_type == "thinking":
            render_thinking_block(content)
        elif msg_type == "tool_call":
            render_tool_call(message.get("tool_name"), content)
        elif msg_type == "iteration":
            # Render iteration from history
            iteration_num = content.get("iteration_num", 0)
            tasks = content.get("tasks", [])
            render_iteration_section(iteration_num, tasks, f"history_{id(message)}")
        elif msg_type == "todos":
            render_todos(content)


def render_thinking_block(reflection: str):
    """Render a thinking/reflection block."""
    st.markdown(f"**💭 Thinking**\n\n{reflection}")
    st.markdown("---")


def render_tool_call(tool_name: str, tool_args: dict):
    """Render a tool call - shows input directly."""
    if tool_name == "write_todos":
        todos = tool_args.get("todos", [])
        lines = ["**📝 Planning**\n"]
        for todo in todos:
            status = todo.get("status", "pending")
            content = todo.get("content", "")
            icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(status, "")
            lines.append(f"- {icon} {content}")
        st.markdown("\n".join(lines))
        st.markdown("---")
    else:
        with st.expander(f"Tool: {tool_name}", expanded=False):
            st.json(tool_args)


def render_todos(todos: list):
    """Render the current todo list."""
    if not todos:
        return

    for todo in todos:
        status = todo.status if hasattr(todo, "status") else todo.get("status", "pending")
        content = todo.content if hasattr(todo, "content") else todo.get("content", "")

        icon = {
            "pending": ":hourglass:",
            "in_progress": ":arrows_counterclockwise:",
            "completed": ":white_check_mark:"
        }.get(status, ":grey_question:")

        st.write(f"{icon} {content}")


def render_chat_history():
    """Render all messages in chat history."""
    for message in st.session_state.messages:
        render_message(message)


def add_message(role: str, content: Any, msg_type: str = "text", **kwargs):
    """Add a message to chat history."""
    message = {
        "role": role,
        "type": msg_type,
        "content": content,
        **kwargs
    }
    st.session_state.messages.append(message)


def show_iteration_immediately(placeholders: dict):
    """Show the current iteration immediately with inputs (before results)."""
    if st.session_state.current_iteration is None:
        return

    iteration = st.session_state.current_iteration
    if iteration.get("displayed"):
        return  # Already displayed

    iteration_num = iteration["iteration_num"]
    tasks = iteration["tasks"]

    if not tasks:
        return

    # Mark as displayed
    iteration["displayed"] = True

    # Render with placeholders for results
    with placeholders["events"]:
        iteration["container"] = st.container()
        iteration["result_placeholders"] = {}
        iteration["header_placeholder"] = render_iteration_streaming(
            iteration_num,
            tasks,
            iteration["container"],
            iteration["result_placeholders"]
        )


def finalize_iteration_to_history():
    """Add current iteration to message history."""
    if st.session_state.current_iteration is None:
        return

    iteration = st.session_state.current_iteration
    tasks = iteration.get("tasks", [])

    if tasks:
        add_message("assistant", {
            "iteration_num": iteration["iteration_num"],
            "tasks": tasks
        }, "iteration")

    st.session_state.current_iteration = None


def handle_stream_event(event: StreamEvent, placeholders: dict):
    """
    Handle a streaming event and update UI accordingly.
    """
    if event.event_type == "thinking":
        # Finalize any pending iteration
        finalize_iteration_to_history()

        with placeholders["events"]:
            render_thinking_block(event.content)
        add_message("assistant", event.content, "thinking", tool_name="think_tool")

    elif event.event_type == "tool_call":
        # Finalize any pending iteration
        finalize_iteration_to_history()

        with placeholders["events"]:
            render_tool_call(event.tool_name, event.content)
        add_message("assistant", event.content, "tool_call", tool_name=event.tool_name)

    elif event.event_type == "task":
        # Start new iteration if needed
        if st.session_state.current_iteration is None:
            st.session_state.iteration_count += 1
            st.session_state.current_iteration = {
                "iteration_num": st.session_state.iteration_count,
                "tasks": [],
                "displayed": False,
                "container": None,
                "header_placeholder": None,
                "result_placeholders": {}
            }

        # Add task to current iteration
        task_data = {
            "task_args": event.content,
            "result": None,
            "tool_call_id": event.tool_call_id
        }
        st.session_state.current_iteration["tasks"].append(task_data)

        # Store for result matching
        if event.tool_call_id:
            st.session_state.pending_tasks[event.tool_call_id] = task_data

    elif event.event_type == "tasks_collected":
        # All task calls collected - show iteration immediately
        show_iteration_immediately(placeholders)

    elif event.event_type == "tool_result":
        if event.tool_name == "task":
            # Update the task with result
            if event.tool_call_id in st.session_state.pending_tasks:
                task_data = st.session_state.pending_tasks.pop(event.tool_call_id)
                task_data["result"] = event.content

                # Update the result placeholder if iteration is displayed
                iteration = st.session_state.current_iteration
                if iteration and iteration.get("displayed"):
                    result_info = iteration["result_placeholders"].get(event.tool_call_id)
                    if result_info:
                        with result_info["placeholder"]:
                            st.markdown(event.content)

                    # Update header with new completion count
                    if iteration.get("header_placeholder"):
                        header = render_iteration_header(
                            iteration["iteration_num"],
                            iteration["tasks"]
                        )
                        iteration["header_placeholder"].markdown(header)

    elif event.event_type == "todos":
        with placeholders["todos"]:
            st.write("**Current Investigation Plan:**")
            render_todos(event.content)

    elif event.event_type == "text":
        # Finalize any pending iteration
        finalize_iteration_to_history()

        text = extract_text_content(event.content)
        placeholders["response"].markdown(text)
        add_message("assistant", event.content, "text")

    elif event.event_type == "error":
        finalize_iteration_to_history()
        st.error(f"Error: {event.content}")
        add_message("assistant", f"Error: {event.content}", "text")


def format_indicators_for_context(indicators: dict) -> str:
    """Format indicators dictionary into a readable string for AI context."""
    if not indicators:
        return "None selected"

    active_indicators = []

    # EMAs
    emas = []
    if indicators.get("ema_10"):
        emas.append("10")
    if indicators.get("ema_20"):
        emas.append("20")
    if indicators.get("ema_50"):
        emas.append("50")
    if indicators.get("ema_100"):
        emas.append("100")
    if emas:
        active_indicators.append(f"EMA ({', '.join(emas)})")

    # Other indicators
    if indicators.get("bb"):
        active_indicators.append("Bollinger Bands")
    if indicators.get("rsi"):
        active_indicators.append("RSI")
    if indicators.get("macd"):
        active_indicators.append("MACD")
    if indicators.get("atr"):
        active_indicators.append("ATR")
    if indicators.get("pivot"):
        active_indicators.append("Pivot Points")
    if indicators.get("fibonacci"):
        active_indicators.append("Fibonacci Levels")

    return ", ".join(active_indicators) if active_indicators else "None selected"


async def process_user_input(
    user_input: str,
    gemini_api_key: str,
    current_symbol: str,
    current_interval: str,
    current_indicators: dict | None = None
):
    """Process user input and stream agent response."""
    # Reset iteration tracking
    st.session_state.current_iteration = None
    st.session_state.iteration_count = 0
    st.session_state.pending_tasks = {}

    indicators_str = format_indicators_for_context(current_indicators or {})
    current_time = datetime.now().strftime("%Y-%m-%d, %H:%M, %A")

    enhanced_query = f"""<context>
- Symbol being analyzed: {current_symbol}. Use THIS symbol when delegating tasks to subagents.
- Chart interval: {current_interval}
- Technical indicators displayed on chart: {indicators_str}
- Current time: {current_time}
</context>

User question: {user_input}"""

    context = create_context(
        gemini_api_key,
        min_research_iterations=st.session_state.min_research_iterations,
        max_research_iterations=st.session_state.max_research_iterations,
        max_concurrent_tasks=st.session_state.max_concurrent_tasks,
    )

    status_placeholder = st.empty()
    todos_placeholder = st.empty()
    events_container = st.container()
    response_placeholder = st.empty()

    placeholders = {
        "status": status_placeholder,
        "todos": todos_placeholder,
        "events": events_container,
        "response": response_placeholder,
    }

    with status_placeholder:
        st.info("Agent is analyzing...", icon=":material/psychology:")

    async for event in stream_agent_response(enhanced_query, context, st.session_state.thread_id):
        handle_stream_event(event, placeholders)

        if event.event_type == "done":
            # Show any remaining iteration and finalize
            show_iteration_immediately(placeholders)
            finalize_iteration_to_history()
            status_placeholder.empty()
