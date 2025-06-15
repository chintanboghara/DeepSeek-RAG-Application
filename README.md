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














Below is a refined version of the provided README.md file for the **DeepSeek RAG Application**. The improvements focus on clarity, structure, and user-friendliness while ensuring all necessary information is included for setup, usage, and troubleshooting. The content has been reorganized for better flow, and additional sections have been added to make the documentation more comprehensive.

---

# DeepSeek RAG Application

A powerful **Streamlit**-based chatbot that leverages **Retrieval-Augmented Generation (RAG)** to answer questions about uploaded PDFs using natural language processing. It allows users to upload a PDF, processes its content, and provides real-time responses to queries about the document.

Under the hood, the application uses:
- **LangChain** for document loading and splitting.
- **ChromaDB** as a vector store for semantic retrieval.
- **Ollama** to serve the `deepseek-r1` LLM model in streaming mode.

## Features

- **PDF Processing**  
  - Upload any PDF; it’s automatically split into overlapping text chunks for efficient semantic indexing.
- **Semantic Retrieval**  
  - Utilizes ChromaDB and OllamaEmbeddings for fast and accurate semantic search over the document.
- **Streaming Responses**  
  - Get real-time, token-by-token answers from the `deepseek-r1` model for a smooth user experience.
- **Configurable**  
  - Easily tweak settings like chunk size, overlap, model ID, and persistence paths via a `.env` file.
- **Extensible**  
  - Modular design (ingest, vectorstore, LLM, UI) allows for easy integration of new features or models.

## Architecture

The application follows a modular architecture, as illustrated below:

```mermaid
graph TD
    A[Streamlit UI] -->|Upload PDF| B[ingest.py]
    B -->|Split into chunks| C[vectorstore (ChromaDB)]
    A -->|Ask question| D[Retriever]
    C --> D
    D -->|Retrieve relevant chunks| E[llm.py (Ollama API)]
    E -->|Generate answer| A
```

## Prerequisites

- **Python 3.8+**
- **Ollama CLI** installed and the `deepseek-r1` model pulled.
- (Recommended) A GPU-enabled machine for optimal performance (e.g., AWS `g4dn.xlarge` or local NVIDIA GPU).

## Quickstart (Local)

1. **Clone the repository**

   ```bash
   git clone https://github.com/chintanboghara/DeepSeek-RAG-Application.git
   cd DeepSeek-RAG-Application
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare your `.env` file**
   - Copy `.env.example` to `.env`.
   - Edit the values in `.env` to match your configuration (e.g., model ID, chunk size).

5. **Ensure the Ollama server is running**
   - Pull the model and start the server:

     ```bash
     ollama pull deepseek-r1:7b
     ollama serve &
     ```

6. **Launch the Streamlit app**

   ```bash
   streamlit run app.py
   ```

7. **Visit** `http://localhost:8501` in your browser to start using the application.

## Configuration

All runtime settings are managed via the `.env` file and loaded by `src/config.py`. Below is a table of configurable variables:

| Variable             | Description                                | Default            | Example              |
| -------------------- | ------------------------------------------ | ------------------ | -------------------- |
| `OLLAMA_MODEL_ID`    | Ollama model identifier                    | `deepseek-r1:7b`   | `deepseek-r1:8b`     |
| `CHUNK_SIZE`         | Maximum characters per text chunk          | `500`              | `1000`               |
| `CHUNK_OVERLAP`      | Overlap characters between adjacent chunks | `100`              | `200`                |
| `CHROMA_PERSIST_DIR` | Directory for ChromaDB persistence         | `./chroma_db`      | `/path/to/chroma_db` |
| `LOG_FILE`           | Path to the application log file           | `chatbot_logs.log` | `logs/app.log`       |
| `PAGE_TITLE`         | Streamlit page title                       | `PDF Q&A Chatbot`  | `My Custom Chatbot`  |

## AWS Deployment

To deploy the application on AWS, follow these steps:

1. **Launch a GPU-enabled EC2 instance** (e.g., `g4dn.xlarge`) with at least 100 GB of storage.
2. **SSH into the instance** and install necessary dependencies:

   ```bash
   sudo apt update && sudo apt install -y nvidia-driver-470 docker.io
   curl -fsSL https://ollama.com/install.sh | sh
   ```

3. **Pull the model and start the Ollama server**

   ```bash
   ollama pull deepseek-r1:7b
   ollama serve &
   ```

4. **Clone the repository and install dependencies**

   ```bash
   git clone https://github.com/chintanboghara/DeepSeek-RAG-Application.git
   cd DeepSeek-RAG-Application
   pip3 install -r requirements.txt
   ```

5. **Run the Streamlit app on a public port**

   ```bash
   streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   ```

6. **Open** `http://<EC2_PUBLIC_IP>:8501` in your browser to access the application.

**Note**: Ensure that your EC2 security group allows inbound traffic on port 8501.

## Testing the Ollama API

You can test the Ollama API directly using the following commands:

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
2. **Ask** your question in the chat input (e.g., "What is the main topic of this document?").
3. **Watch** the answer stream in real time as the model processes your query.

### Example

- **Question**: "Summarize the key points of the document."
- **Answer**: (The model will generate a summary based on the PDF content.)

## Troubleshooting

- **“Failed to process PDF”**  
  - Ensure the PDF is not encrypted or consists only of scanned images (OCR may be required).
- **Ollama connection errors**  
  - Verify that the Ollama server is running on `localhost:11434` by checking the process or logs.
- **Slow responses**  
  - Try reducing `CHUNK_SIZE` in the `.env` file or use a machine with better compute resources (e.g., GPU).
- **Port conflicts**  
  - If port 8501 is in use, specify a different port when running Streamlit (e.g., `--server.port 8502`).
