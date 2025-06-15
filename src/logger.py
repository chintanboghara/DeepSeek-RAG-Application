import logging
from .config import LOG_FILE

def setup_logging() -> None:
    """Configure root logger once."""
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    logging.getLogger("chromadb").setLevel(logging.WARNING)
