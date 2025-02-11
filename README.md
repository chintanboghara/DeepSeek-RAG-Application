[![CodeQL Advanced](https://github.com/chintanboghara/DeepSeek-RAG-Application/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/chintanboghara/DeepSeek-RAG-Application/actions/workflows/codeql.yml)

# DeepSeek RAG Application

This repository contains a Streamlit-based chatbot application that allows users to upload a PDF file and ask questions about its contents. The app uses LangChain for document processing, ChromaDB for vector storage, and Ollama to serve the DeepSeek model for question answering.

## Features

- **PDF Processing:** Upload a PDF, which is then split into chunks for processing.
- **Retrieval-Augmented Generation (RAG):** Retrieve relevant document chunks based on user questions.
- **Streaming Responses:** Get real-time streaming responses from the DeepSeek model via Ollama.
- **Easy Deployment:** Run the application locally or deploy it on an AWS EC2 instance.

## Setup & Installation

### Prerequisites

- Python 3.7 or higher
- [Ollama](https://ollama.com/) installed and running
- (Optional) An AWS EC2 instance for deployment

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/chintanboghar/DeepSeek-RAG-Application.git
   cd DeepSeek-RAG-Application
   ```

2. **Install Dependencies**

   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. **Run the Application**

   ```bash
   python3 -m streamlit run app.py
   ```

## Deploying DeepSeek on AWS EC2

### Steps

1. **Set Up EC2 Instance**

   - Launch an AWS EC2 instance and configure security settings.

2. **Connect to EC2**

   - SSH into your EC2 instance.

3. **Install Dependencies**

   - Update system packages:
     ```bash
     sudo apt update
     ```
   - Install Ollama:
     ```bash
     curl -fsSL https://ollama.com/install.sh | sh
     ```
   - Download and run the DeepSeek model (for example, `deepseek-r1:7b`):
     ```bash
     ollama run deepseek-r1:7b
     ```
   - Verify the API is serving:
     ```bash
     ollama serve
     ```

4. **Install Python Dependencies**

   - On your EC2 instance, clone this repository and install the Python dependencies:
     ```bash
     git clone https://github.com/chintanboghara/DeepSeek-RAG-Application.git
     cd DeepSeek-RAG-Application
     python3 -m pip install -r requirements.txt
     ```

5. **Run the Chatbot App**

   - Start the Streamlit application:
     ```bash
     python3 -m streamlit run app.py
     ```

## Commands Reference

Below are some useful commands for setting up and testing the model and app:

```sh
# Update System Packages
sudo apt update

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Run the DeepSeek model
ollama run deepseek-r1:7b

# Check API Serving
ollama serve

# Test the model API
curl http://localhost:11434/api/chat -d '{
  "model": "deepseek-r1:8b",
  "messages": [{ "role": "user", "content": "Write python script for hello world" }],
  "stream": false
}'

# To install Python requirements
python3 -m pip install -r requirements.txt

# To run the Streamlit app
python3 -m streamlit run app.py
```
