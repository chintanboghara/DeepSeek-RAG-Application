[![CodeQL Advanced](https://github.com/chintanboghara/DeepSeek-RAG-Application/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/chintanboghara/DeepSeek-RAG-Application/actions/workflows/codeql.yml)
[![Dependency review](https://github.com/chintanboghara/DeepSeek-RAG-Application/actions/workflows/dependency-review.yml/badge.svg)](https://github.com/chintanboghara/DeepSeek-RAG-Application/actions/workflows/dependency-review.yml)

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
- A **GPU-enabled AWS EC2 instance** with a large amount of storage for handling large language models

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/chintanboghara/DeepSeek-RAG-Application.git
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

1. **Set Up a GPU-Enabled EC2 Instance**
   - Choose an AWS EC2 instance with a GPU (e.g., `g4dn.xlarge`, `p3.2xlarge`, or higher depending on your needs).
   - Allocate sufficient storage (at least **100GB** recommended).
   - Configure security settings to allow SSH and necessary ports for Streamlit.

2. **Connect to EC2**

   - SSH into your EC2 instance:
     ```bash
     ssh -i your-key.pem ubuntu@your-ec2-instance-ip
     ```

3. **Install Dependencies**

   - Update system packages:
     ```bash
     sudo apt update
     ```
   - Install GPU drivers (for NVIDIA instances):
     ```bash
     sudo apt install -y nvidia-driver-470
     reboot
     ```
   - Verify GPU availability:
     ```bash
     nvidia-smi
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

   - Clone the repository and install the Python dependencies:
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

## Testing the Model API using Postman

### 1. Testing with a POST Request

- **Step 1:** Open Postman and create a new **POST** request.
- **Step 2:** Set the request URL to:
  ```
  http://localhost:11434/api/chat
  ```
- **Step 3:** Click on the **Body** tab, select **raw**, and choose **JSON** from the dropdown.
- **Step 4:** Enter the following JSON:
  ```json
  {
    "model": "deepseek-r1:8b",
    "messages": [{ "role": "user", "content": "Write python script for hello world" }],
    "stream": false
  }
  ```
- **Step 5:** Click **Send** and review the response from the API.

### 2. Testing with a GET Request

*Note:* The main chat endpoint is designed to accept POST requests. However, if the API server provides a GET endpoint (such as a health or status check), you can test it as follows:

- **Step 1:** Create a new **GET** request in Postman.
- **Step 2:** Set the request URL to (example):
  ```
  http://localhost:11434/api/health
  ```
  *Replace `/api/health` with the actual GET endpoint if available.*
- **Step 3:** Click **Send** and check the response to verify that the API server is running.
