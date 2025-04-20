# DeepSeek RAG Application

[![CodeQL Advanced](https://github.com/chintanboghara/DeepSeek-RAG-Application/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/chintanboghara/DeepSeek-RAG-Application/actions/workflows/codeql.yml)
[![Dependency review](https://github.com/chintanboghara/DeepSeek-RAG-Application/actions/workflows/dependency-review.yml/badge.svg)](https://github.com/chintanboghara/DeepSeek-RAG-Application/actions/workflows/dependency-review.yml)

This repository contains a Streamlit-based chatbot application that allows users to upload a PDF file and ask questions about its contents. The app uses LangChain for document processing, ChromaDB for vector storage, and Ollama to serve the DeepSeek model for question answering. This application leverages Retrieval-Augmented Generation (RAG) to combine the power of large language models with information retrieval from uploaded documents, enabling accurate and contextually relevant responses.

## Features

- **PDF Processing:** Upload a PDF, which is then split into chunks for processing.
- **Retrieval-Augmented Generation (RAG):** Retrieve relevant document chunks based on user questions.
- **Streaming Responses:** Get real-time streaming responses from the DeepSeek model via Ollama.
- **Easy Deployment:** Run the application locally or deploy it on an AWS EC2 instance.

## Setup & Installation

### Local Setup

#### Prerequisites

- Python 3.7 or higher
- [Ollama](https://ollama.com/) installed and running (with the DeepSeek model pulled)
- A machine with a GPU is recommended for handling large language models

#### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/chintanboghara/DeepSeek-RAG-Application.git
   cd DeepSeek-RAG-Application
   ```

2. **Install Dependencies**

   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. **Ensure Ollama is Running**

   - Pull the model: `ollama pull deepseek-r1:7b`
   - Start the server: `ollama serve &`

4. **Run the Application**

   ```bash
   python3 -m streamlit run app.py
   ```

### AWS Deployment

#### Prerequisites

- A GPU-enabled AWS EC2 instance (e.g., `g4dn.xlarge` or higher)
- At least 100GB of storage
- SSH access and appropriate security group settings (allow ports for SSH, Streamlit, etc.)

#### Deployment Steps

1. **Connect to EC2**

   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-instance-ip
   ```

2. **Update System Packages**

   ```bash
   sudo apt update
   ```

3. **Install GPU Drivers**

   ```bash
   sudo apt install -y nvidia-driver-470  # Adjust the driver version as needed
   reboot
   ```

4. **Verify GPU Availability**

   ```bash
   nvidia-smi
   ```

5. **Install Ollama**

   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

6. **Pull the DeepSeek Model**

   ```bash
   ollama pull deepseek-r1:7b
   ```

7. **Start the Ollama Server**

   ```bash
   ollama serve &
   ```

8. **Install Python Dependencies**

   ```bash
   git clone https://github.com/chintanboghara/DeepSeek-RAG-Application.git
   cd DeepSeek-RAG-Application
   python3 -m pip install -r requirements.txt
   ```

9. **Run the Chatbot App**

   ```bash
   python3 -m streamlit run app.py
   ```

   **Note:** Configure Streamlit to run on a specific port and ensure it’s accessible via the EC2 instance’s public IP.

## Testing the Model API using Postman

### 1. Testing with a POST Request

- **Step 1:** Open Postman and create a new **POST** request.
- **Step 2:** Set the request URL to:
  ```
  http://localhost:11434/api/chat
  ```
- **Step 3:** Click on the **Body** tab, select **raw**, and choose **JSON** from the dropdown.
- **Step 4:** Enter the following JSON (ensure the model matches the one pulled, e.g., "deepseek-r1:7b"):
  ```json
  {
    "model": "deepseek-r1:7b",
    "messages": [{ "role": "user", "content": "Write a Python script for hello world" }],
    "stream": false
  }
  ```
- **Step 5:** Click **Send** and review the response from the API.

### 2. Testing with a GET Request

- **Step 1:** Create a new **GET** request in Postman.
- **Step 2:** Set the request URL to:
  ```
  http://localhost:11434/api/tags
  ```
- **Step 3:** Click **Send** and check the response to verify that the API server is running and lists available models.

## Usage

1. **Upload a PDF:** Use the file uploader in the Streamlit app to upload a PDF document.
2. **Processing:** The app will process the PDF, split it into chunks, and index it using ChromaDB.
3. **Ask Questions:** Enter your questions in the chat input. The app will retrieve relevant information from the PDF and generate responses using the DeepSeek model.
4. **Streaming Responses:** Answers will be streamed in real-time as they are generated.
