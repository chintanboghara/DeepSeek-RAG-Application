import tempfile
import logging
from typing import List, Tuple
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .config import CHUNK_SIZE, CHUNK_OVERLAP

logger = logging.getLogger(__name__)

def load_and_split_pdf(
    file_bytes: bytes
) -> Tuple[RecursiveCharacterTextSplitter, List[Document]]:
    """
    Save incoming PDF bytes to a temp file, load it, and split into chunks.
    """
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    logger.info("Saved PDF to %s", tmp_path)

    loader = PyMuPDFLoader(tmp_path)
    docs = loader.load()
    logger.info("Loaded %d pages from PDF", len(docs))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)
    logger.info("Split into %d chunks", len(chunks))
    return splitter, chunks
