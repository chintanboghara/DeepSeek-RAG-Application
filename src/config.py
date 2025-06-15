import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from repo root
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# Ollama model
MODEL_ID: str = os.getenv("OLLAMA_MODEL_ID", "deepseek-r1:8b")

# PDF chunking
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 100))

# Persistence paths
CHROMA_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
LOG_FILE: str = os.getenv("LOG_FILE", "chatbot_logs.log")

# Streamlit
PAGE_TITLE: str = os.getenv("PAGE_TITLE", "PDF Q&A Chatbot")
