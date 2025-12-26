# 📄 Multi-Modal Document Intelligence (RAG-Based QA System)

This project implements a **multi-modal Retrieval-Augmented Generation (RAG) system** capable of answering questions grounded in complex real-world documents such as financial reports, policy papers, and research PDFs.

The system handles **text, tables, and images (via OCR)** and produces context-aware answers using semantic retrieval and a large language model.

---

## ✨ Key Features

- **Multi-modal document ingestion**

  - Text extraction from PDFs
  - Table extraction
  - Image OCR support

- **Smart chunking**

  - Modality-aware chunking for text, tables, and OCR output

- **Vector-based retrieval**

  - Dense embeddings with FAISS for semantic search

- **LLM-powered question answering**

  - Grounded, uncertainty-aware responses

- **Interactive UI**

  - Streamlit-based chat interface for document upload and Q&A

---

## 🏗️ Architecture Overview

PDF Document
↓
Ingestion (text / tables / images + OCR)
↓
Chunking (modality-aware)
↓
Embeddings
↓
Vector Store (FAISS)
↓
Retriever
↓
LLM (Gemini Flash Lite)
↓
Context-grounded Answer

---

## 📁 Project Structure

multi-modal-document-intelligence/
│
├── ingestion/ # pdf parsing, text, table, image extraction
├── chunking/ # modality-aware chunking logic
├── embeddings/ # embedding model wrapper
├── retrieval/ # vector store and retriever
├── qa/ # answer generation using llm
├── app/ # streamlit chat application
├── data/ # sample documents
├── main.py # end-to-end pipeline test
├── requirements.txt
├── README.md
└── .gitignore

---

## 🚀 Setup

### Clone the repository

git clone <repository-url>
cd multi-modal-document-intelligence

---

### (Optional) Create a virtual environment

python -m venv venv
source venv/bin/activate

# windows: venv\Scripts\activate

---

### Install dependencies

pip install -r requirements.txt

---

### Configure environment variables

Create a `.env` file in the project root:

GEMINI_API_KEY=your_api_key_here

---

## ▶️ Usage

### Run the full pipeline (CLI)

python main.py

This will:

- ingest a document
- chunk and embed content
- build a vector index
- retrieve relevant context
- generate a grounded answer

---

### Run the Streamlit chat application

streamlit run app/chat_app.py

Features:

- upload a document
- ask questions interactively
- receive answers grounded in retrieved context

---

## 🧠 LLM Configuration

The system uses **Gemini 2.5 Flash Lite** via the official Google GenAI Python client.

- fast and cost-efficient
- strong numeric and table reasoning
- suitable for document question answering

---

## 🔍 Design Notes

- Tables are preserved as structured context
- OCR text is chunked separately to reduce noise
- Retrieval precedes generation to minimize hallucinations
- Answers are generated with uncertainty-aware language when evidence is partial

---

## 🧪 Limitations & Future Work

- Cross-modal reranking
- Hybrid search (BM25 + dense retrieval)
- Explicit citation formatting
- Evaluation metrics and dashboards

---

## 📌 Purpose

This project serves as a **document intelligence prototype** demonstrating:

- multi-modal data handling
- retrieval-based QA pipelines
- safe integration of large language models

---

## 📜 License

For educational and evaluation purposes only.
