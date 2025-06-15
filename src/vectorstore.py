import logging
from typing import Any
from langchain.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from .config import MODEL_ID, CHROMA_DIR

logger = logging.getLogger(__name__)

def build_chroma_store(chunks: list[Any]):
    """
    Given a list of Document chunks, persists or loads a ChromaDB store
    and returns a retriever.
    """
    embeddings = OllamaEmbeddings(model=MODEL_ID)
    store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    logger.info("Chroma store initialized at %s", CHROMA_DIR)
    return store.as_retriever()
