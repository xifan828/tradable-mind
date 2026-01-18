"""Simple token counting app."""

import streamlit as st

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


def count_tokens(text: str, encoding_name: str) -> int:
    """Count tokens in text using specified encoding."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


def main():
    st.set_page_config(
        page_title="Token Counter",
        page_icon="🔢",
        layout="centered",
    )

    st.title("Token Counter")
    st.write("Paste text below to count the number of tokens.")

    if not TIKTOKEN_AVAILABLE:
        st.error(
            "tiktoken is not installed. Please run: `uv add tiktoken`"
        )
        return

    # Encoding selection
    encoding_options = {
        "cl100k_base": "GPT-4, GPT-3.5-turbo, text-embedding-ada-002",
        "o200k_base": "GPT-4o, GPT-4o-mini",
        "p50k_base": "Codex models, text-davinci-002/003",
    }

    selected_encoding = st.selectbox(
        "Select tokenizer encoding",
        options=list(encoding_options.keys()),
        format_func=lambda x: f"{x} ({encoding_options[x]})",
        index=0,
    )

    # Text input
    text = st.text_area(
        "Enter your text",
        height=300,
        placeholder="Paste your text here...",
    )

    # Count and display
    if text:
        token_count = count_tokens(text, selected_encoding)
        char_count = len(text)
        word_count = len(text.split())

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tokens", f"{token_count:,}")
        with col2:
            st.metric("Characters", f"{char_count:,}")
        with col3:
            st.metric("Words", f"{word_count:,}")

        # Show tokens breakdown (optional)
        with st.expander("View individual tokens"):
            encoding = tiktoken.get_encoding(selected_encoding)
            tokens = encoding.encode(text)
            decoded_tokens = [encoding.decode([t]) for t in tokens]

            # Display tokens as a list with indices
            token_display = []
            for i, (token_id, token_text) in enumerate(zip(tokens, decoded_tokens)):
                token_display.append(f"{i}: `{repr(token_text)}` (ID: {token_id})")

            st.text("\n".join(token_display[:100]))
            if len(tokens) > 100:
                st.info(f"Showing first 100 of {len(tokens)} tokens")
    else:
        st.info("Enter some text to see the token count.")


if __name__ == "__main__":
    main()
