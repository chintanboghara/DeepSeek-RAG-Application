import streamlit as st

from src.config import PAGE_TITLE
from src.logger import setup_logging
from src.ingest import load_and_split_pdf
from src.vectorstore import build_chroma_store
from src.llm import stream_response
from src.ui import display_streamlit_ui, show_streaming_answer

# Initialize logging once
setup_logging()

def main():
    display_streamlit_ui(PAGE_TITLE)

    uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded:
        with st.spinner("Processing PDF…"):
            splitter, chunks = load_and_split_pdf(uploaded.read())
            retriever = build_chroma_store(chunks)
        st.success("✅ PDF processed successfully!")
        st.session_state.retriever = retriever

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask a question…")
    if question:
        if retr := st.session_state.get("retriever"):
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                context_docs = retr(question)
                context = "\n\n".join(d.page_content for d in context_docs)
                gen = stream_response(question, context)
                answer = show_streaming_answer(gen)

            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.warning("Please upload and process a PDF first.")

if __name__ == "__main__":
    main()
