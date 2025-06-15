# DeepSeek RAG Application

A **Streamlit**-based Retrieval‑Augmented Generation (RAG) chatbot that lets you upload a PDF and ask natural‑language questions about its contents. Under the hood it uses:

- **LangChain** for document loading & splitting  
- **ChromaDB** as a vector store for semantic retrieval  
- **Ollama** to serve the `deepseek-r1` LLM model in streaming mode  

## Features

- **PDF Processing**  
  - Upload any PDF; it’s split into overlapping text chunks for semantic indexing.  
- **Semantic Retrieval**  
  - ChromaDB & OllamaEmbeddings create a retriever over your document.  
- **Streaming Responses**  
  - Get real‑time, token‑by‑token answers from the `deepseek-r1` model.  
- **Configurable**  
  - Tweak chunk size, overlap, model ID, and persistence paths via `.env`.  
- **Extensible**  
  - Modular codebase (ingest, vectorstore, LLM, UI) ready for testing & CI.

## Architecture

```text
┌────────────┐    PDF file     ┌──────────────┐
│  Streamlit │ ──────────────> │  ingest.py   │
│     UI     │                 └──────────────┘
└─────┬──────┘                       │
      │ chunks                      ▼
      │                      ┌──────────────┐
      │                      │ vectorstore  │
      │                      │  (ChromaDB)  │
      │                      └──────────────┘
      │                              │
      │ retrieve                     ▼
      │                      ┌──────────────┐
      │                      │  llm.py      │
      │                      │ (Ollama API) │
      │                      └──────────────┘
      │                              │
      └──────────────────────────────┘
                   answer (streamed)
````

## Prerequisites

* **Python 3.7+**
* **Ollama CLI** installed & your `deepseek-r1` model pulled
* (Recommended) GPU-enabled machine for best performance

## Quickstart (Local)

1. **Clone & enter repo**

   ```bash
   git clone https://github.com/chintanboghara/DeepSeek-RAG-Application.git
   cd DeepSeek-RAG-Application
   ```

2. **Create & activate venv**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare your `.env`**
   Copy `.env.example` to `.env`, then edit values as needed.

5. **Ensure Ollama server is running**

   ```bash
   ollama pull deepseek-r1:7b
   ollama serve &
   ```

6. **Launch the Streamlit app**

   ```bash
   streamlit run app.py
   ```

7. **Visit** `http://localhost:8501` in your browser.

## Configuration

All runtime settings live in the `.env` file (loaded by `src/config.py`).

| Variable             | Description                                | Default            |
| -------------------- | ------------------------------------------ | ------------------ |
| `OLLAMA_MODEL_ID`    | Ollama model identifier                    | `deepseek-r1:8b`   |
| `CHUNK_SIZE`         | Maximum characters per text chunk          | `500`              |
| `CHUNK_OVERLAP`      | Overlap characters between adjacent chunks | `100`              |
| `CHROMA_PERSIST_DIR` | Directory for ChromaDB persistence         | `./chroma_db`      |
| `LOG_FILE`           | Path to the application log file           | `chatbot_logs.log` |
| `PAGE_TITLE`         | Streamlit page title                       | `PDF Q&A Chatbot`  |

## AWS Deployment

1. **Launch** a GPU EC2 instance (e.g. `g4dn.xlarge`) with at least 100 GB storage.
2. **SSH in** and install NVIDIA drivers, Docker, and Ollama:

   ```bash
   sudo apt update && sudo apt install -y nvidia-driver-470 docker.io
   curl -fsSL https://ollama.com/install.sh | sh
   ```
3. **Pull model & start server**

   ```bash
   ollama pull deepseek-r1:7b
   ollama serve &
   ```
4. **Clone & install**

   ```bash
   git clone https://github.com/chintanboghara/DeepSeek-RAG-Application.git
   cd DeepSeek-RAG-Application
   pip3 install -r requirements.txt
   ```
5. **Run Streamlit on public port**

   ```bash
   streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   ```
6. **Open** `http://<EC2_PUBLIC_IP>:8501` in your browser.

## Testing the Ollama API

### POST `/api/chat`

```bash
curl -X POST http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-r1:7b","messages":[{"role":"user","content":"Hello"}],"stream":false}'
```

### GET `/api/tags`

```bash
curl http://localhost:11434/api/tags
```

## Usage

1. **Upload** your PDF via the Streamlit sidebar.
2. **Ask** your question in the chat input.
3. **Watch** the answer stream in real time.

## Troubleshooting

* **“Failed to process PDF”**

  * Check if the file is encrypted or scanned images only.
* **Ollama connection errors**

  * Ensure `ollama serve` is running on `localhost:11434`.
* **Slow responses**

  * Try reducing `CHUNK_SIZE` or increasing compute resources.
