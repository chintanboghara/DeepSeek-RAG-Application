import streamlit as st
from typing import Generator

def display_streamlit_ui(page_title: str) -> None:
    """Configure page and layout."""
    st.set_page_config(page_title=page_title, layout="wide")
    st.title(page_title)

def show_streaming_answer(gen: Generator[str, None, None]) -> str:
    """Render a streaming generator into the chat UI and return the full answer."""
    placeholder = st.empty()
    full = ""
    for token in gen:
        full += token
        placeholder.markdown(full)
    return full
