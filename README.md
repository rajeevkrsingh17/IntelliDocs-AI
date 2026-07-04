# IntelliDocs-AI

An AI-powered Document Question Answering system that extracts information from PDF documents and enables users to ask questions using Retrieval-Augmented Generation (RAG).

---

## 📌 Problem Statement

**Problem Statement Code:** I2 – Document Q&A (RAG over a Focused Corpus)

**Segment:** Artificial Intelligence

---

## 👨‍💻 Student Details

**Name:** Rajeev Kumar

**University:** Lovely Professional University

**Program:** B.Tech CSE (Artificial Intelligence & Data Engineering)

**Internship Duration:** 22 June 2026 – 26 July 2026

---

## 📖 Project Overview

IntelliDocs-AI is an AI-based document intelligence system that allows users to upload PDF documents and ask questions in natural language. The application extracts text from documents, converts the content into embeddings, stores them in a vector database, retrieves the most relevant context, and generates accurate answers using a Large Language Model (LLM).

The objective of this project is to simplify document understanding and information retrieval through Retrieval-Augmented Generation (RAG).

---

## ✨ Features

- PDF Document Upload
- Text Extraction using PyMuPDF
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- AI-powered Question Answering
- Modular Project Structure
- Easy to Extend and Maintain

---

## 📂 Project Structure

```
IntelliDocs-AI/
│
├── data/
│   ├── raw/
│   │   └── sample_document.pdf
│   └── processed/
│
├── docs/
│   ├── design_doc.md
│   └── tech_stack.md
│
├── scripts/
│   └── pdf_reader.py
│
├── README.md
├── .gitignore
└── requirements.txt
```

### Folder Description

| Folder | Description |
|---------|-------------|
| data/raw | Stores original PDF documents |
| data/processed | Stores processed data (future use) |
| docs | Project documentation |
| scripts | Python scripts for project functionality |
| README.md | Project overview and instructions |

---

## 🛠 Tech Stack

| Component | Technology |
|------------|------------|
| Programming Language | Python |
| PDF Processing | PyMuPDF (fitz) |
| AI Framework | LangChain |
| Vector Database | ChromaDB |
| User Interface | Streamlit |
| Version Control | Git & GitHub |

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/rajeevkrsingh17/IntelliDocs-AI.git
```

Navigate to the project folder:

```bash
cd IntelliDocs-AI
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

Run the PDF reader script:

```bash
python scripts/pdf_reader.py
```

---

## 📊 Current Progress

| Task | Status |
|------|--------|
| Repository Created | ✅ Completed |
| README Documentation | ✅ Completed |
| Design Document | ✅ Completed |
| Tech Stack Documentation | ✅ Completed |
| PDF Reader | ✅ Completed |
| Sample PDF Tested | ✅ Completed |
| Embedding Generation | ⏳ In Progress |
| ChromaDB Integration | ⏳ Planned |
| Retrieval Pipeline | ⏳ Planned |
| Streamlit Interface | ⏳ Planned |

---

## 📚 What I Learned This Week

- Learned how PyMuPDF extracts text from PDF documents efficiently.
- Understood the importance of organizing an AI project before implementation.
- Learned how GitHub repositories and meaningful commits improve project management.
- Improved my understanding of the Retrieval-Augmented Generation (RAG) workflow.
- Learned the importance of documenting project architecture and technical decisions.

---

## 🚀 Future Enhancements

- Generate document embeddings.
- Integrate ChromaDB for semantic search.
- Implement Retrieval-Augmented Generation (RAG).
- Build an interactive Streamlit interface.
- Support multiple document uploads.
- Improve answer accuracy using advanced embedding models.

---

## 📅 Week 1 Progress

### ✅ Completed

- Created public GitHub repository.
- Prepared project documentation.
- Designed project architecture.
- Selected technology stack.
- Implemented PDF text extraction.
- Successfully tested with sample PDF.

### 🚧 Current Challenges

- Integrating vector database.
- Selecting the best embedding model.
- Building the retrieval pipeline.

### 🎯 Goals for Week 2

- Generate embeddings.
- Integrate ChromaDB.
- Build semantic search.
- Connect the retrieval pipeline.
- Develop the Streamlit interface.

---

## 📄 License

This project is developed for academic and internship purposes under the Summer Internship Program 2026.

---

## ⭐ Repository

GitHub Repository:

https://github.com/rajeevkrsingh17/IntelliDocs-AI
