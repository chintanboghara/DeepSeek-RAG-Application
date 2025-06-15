import re
import logging
from typing import Generator
import ollama
from .config import MODEL_ID

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "You are an AI assistant specialized in answering questions concisely. "
    "Provide clear and direct responses, keeping answers as brief as possible while maintaining accuracy."
)

def stream_response(
    question: str, context: str
) -> Generator[str, None, None]:
    """
    Calls Ollama in streaming mode, yields tokens as they arrive.
    """
    messages = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": f"Question: {question}\n\nContext: {context}"}
    ]
    logger.info("Calling Ollama model %s", MODEL_ID)
    stream = ollama.chat(model=MODEL_ID, messages=messages, stream=True)

    full = ""
    try:
        for chunk in stream:
            token = chunk["message"]["content"]
            full += token
            yield token
    except Exception as e:
        logger.error("Ollama streaming error: %s", e, exc_info=True)
        yield "⚠️ Error generating response."

    # Final cleanup (not streamed)
    cleaned = re.sub(r"<think>.*?</think>", "", full, flags=re.DOTALL).strip()
    return cleaned
