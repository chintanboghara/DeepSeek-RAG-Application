import streamlit as st
import logging
import tempfile
import re

from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import ollama

# Configure logging
logging.basicConfig(
    filename="chatbot_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set the model ID for Ollama
MODEL_ID = "deepseek-r1:8b"


def process_pdf(uploaded_file):
    """
    Process an uploaded PDF file:
      - Save the file temporarily.
      - Load the PDF using PyMuPDFLoader.
      - Split the document into chunks.
      - Create a vectorstore using Ollama embeddings.
    
    Returns:
      tuple: (text_splitter, vectorstore, retriever) or (None, None, None) on error.
    """
    if uploaded_file is None:
        return None, None, None

    try:
        # Use a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        logging.info("PDF uploaded and saved successfully to temporary file.")

        # Load PDF and split into chunks
        loader = PyMuPDFLoader(tmp_file_path)
        data = loader.load()
        logging.info("PDF loaded successfully.")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        chunks = text_splitter.split_documents(data)
        logging.info(f"PDF split into {len(chunks)} chunks.")

        # Create vectorstore from document chunks
        embeddings = OllamaEmbeddings(model=MODEL_ID)
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        retriever = vectorstore.as_retriever()
        logging.info("Vectorstore created and retriever initialized.")

        return text_splitter, vectorstore, retriever

    except Exception as e:
        logging.error(f"Error in processing PDF: {e}")
        return None, None, None


def combine_docs(docs):
    """
    Combine document chunks into a single string.
    """
    return "\n\n".join(doc.page_content for doc in docs)


def ollama_llm_streaming(question, context):
    """
    Send a question and context to the Ollama LLM in streaming mode.
    Yields each token received from the stream.

    The response is filtered to remove any <think> tags.
    """
    system_prompt = (
        "You are an AI assistant specialized in answering questions concisely. "
        "Provide clear and direct responses, keeping answers as brief as possible while maintaining accuracy. "
        "If necessary, limit your response to 2-3 sentences."
    )

    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    logging.info("Sending request to Ollama LLM...")

    try:
        response_stream = ollama.chat(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": formatted_prompt}
            ],
            stream=True
        )

        final_answer = ""
        for chunk in response_stream:
            content = chunk["message"]["content"]
            final_answer += content
            yield content  # Stream token to the UI

        # Clean final answer if necessary
        final_answer = re.sub(r"<think>.*?</think>", "", final_answer, flags=re.DOTALL).strip()
        logging.info("Ollama response received successfully.")

    except Exception as e:
        logging.error(f"Error in Ollama LLM response: {e}")
        yield "Error in generating response."


def rag_chain_streaming(question, retriever):
    """
    Retrieve relevant document chunks for the question and stream the response from the LLM.
    """
    logging.info(f"Retrieving context for question: {question}")
    retrieved_docs = retriever.invoke(question)
    formatted_context = combine_docs(retrieved_docs)
    logging.info(f"Retrieved {len(retrieved_docs)} relevant documents.")
    return ollama_llm_streaming(question, formatted_context)


def display_streaming_response(response_generator):
    """
    Display the streaming response in a Streamlit placeholder.
    
    Returns:
      The full response text once streaming is complete.
    """
    full_response = ""
    placeholder = st.empty()  # Placeholder for dynamic updates

    for token in response_generator:
        full_response += token
        placeholder.markdown(full_response)

    return full_response


# --------------------- Streamlit UI ---------------------
st.set_page_config(page_title="PDF Q&A Chatbot", layout="wide")
st.title("Ask Questions About Your PDF 📄🤖")

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Processing PDF..."):
        text_splitter, vectorstore, retriever = process_pdf(uploaded_file)
    if text_splitter and retriever:
        st.session_state["retriever"] = retriever
        st.success("✅ PDF processed successfully!")
    else:
        st.error("❌ Failed to process PDF. Please check the file or try again.")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages (if any)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process new chat input
question = st.chat_input("Ask a question...")
if question:
    if "retriever" in st.session_state:
        # Append user message and display it
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Get and stream assistant response
        with st.chat_message("assistant"):
            response_generator = rag_chain_streaming(question, st.session_state["retriever"])
            response_text = display_streaming_response(response_generator)

        st.session_state.messages.append({"role": "assistant", "content": response_text})
    else:
        st.warning("⚠️ Please upload and process a PDF first.")
