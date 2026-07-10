# IntelliDocs-AI

An AI-powered document intelligence system that extracts text from PDF documents, generates semantic embeddings, stores them in a vector database, and performs semantic search as the foundation of a Retrieval-Augmented Generation (RAG) based Question Answering application.

---

# 📌 Project Information

**Problem Statement Code:** I2 – Document Q&A (RAG over a Focused Corpus)

**Segment:** Foundations of Applied Machine Learning

**Student Name:** Rajeev Kumar

---

# 📖 Project Overview

IntelliDocs-AI is being developed as part of the Summer Internship 2026. The objective of this project is to build an AI-powered document question answering system capable of understanding PDF documents and retrieving relevant information using semantic search.

During **Week 1**, the focus was on:

- Setting up the project repository
- Preparing project documentation
- Finalizing the technology stack
- Organizing the project structure
- Implementing PDF text extraction using PyMuPDF

During **Week 2**, the project was extended by implementing:

- Document chunking
- Semantic embedding generation using Sentence Transformers
- ChromaDB vector database integration
- Semantic search over document content
- Basic Streamlit user interface

Future work will focus on integrating a Large Language Model (LLM) to generate context-aware answers using Retrieval-Augmented Generation (RAG).

---

# 🎯 Objectives

- Extract text from PDF documents.
- Generate semantic embeddings from document content.
- Store embeddings in a vector database.
- Retrieve relevant document chunks using semantic search.
- Build a Retrieval-Augmented Generation (RAG) based Question Answering system.

---

# ✨ Current Features

- PDF Text Extraction using PyMuPDF
- Document Chunking
- Semantic Embedding Generation
- ChromaDB Vector Storage
- Semantic Document Search
- Basic Streamlit Interface
- Organized Project Structure
- Git Version Control

---

# 📂 Project Structure

```text
IntelliDocs-AI/
│
├── data/
│   ├── raw/
│   └── processed/
│       └── chroma_db/
│
├── docs/
│   ├── design_doc.md
│   └── tech_stack.md
│
├── scripts/
│   ├── pdf_reader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── search.py
│   └── app.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 🛠 Tech Stack

| Component | Technology |
|------------|------------|
| Programming Language | Python |
| PDF Processing | PyMuPDF |
| Embedding Model | Sentence Transformers |
| Vector Database | ChromaDB |
| User Interface | Streamlit |
| Version Control | Git & GitHub |

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/rajeevkrsingh17/IntelliDocs-AI.git
```

Move into the project directory:

```bash
cd IntelliDocs-AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Project

Run the Streamlit application:

```bash
python -m streamlit run scripts/app.py
```

---

# 📊 Current Progress

| Task | Status |
|------|--------|
| Repository Created | ✅ |
| README | ✅ |
| Design Document | ✅ |
| Tech Stack Documentation | ✅ |
| PDF Text Extraction | ✅ |
| Document Chunking | ✅ |
| Embedding Generation | ✅ |
| ChromaDB Integration | ✅ |
| Semantic Search | ✅ |
| Streamlit Interface | ✅ |
| LLM Integration | ⏳ Planned |

---

# 📚 What I Learned

### Week 1

- Learned how to organize a professional AI project repository.
- Learned PDF text extraction using PyMuPDF.
- Improved my Git workflow with meaningful commits.
- Understood the basic workflow of a Retrieval-Augmented Generation (RAG) system.

### Week 2

- Learned how document chunking improves semantic retrieval.
- Generated document embeddings using Sentence Transformers.
- Stored embeddings using ChromaDB.
- Built semantic search over PDF documents.
- Developed a basic Streamlit interface for document retrieval.

---

# 💡 What Surprised Me

I was surprised to see how much the quality of semantic search depends on proper document chunking and embedding generation. Even without using a Large Language Model, semantic search was able to retrieve relevant document sections based on meaning rather than exact keyword matching.

---

# 🎯 Goals for Week 3

- Integrate a Large Language Model (LLM).
- Generate context-aware answers from retrieved document chunks.
- Improve retrieval quality.
- Support dynamic PDF uploads.
- Enhance the Streamlit user interface.

---

# 🔗 GitHub Repository

**Repository:**  
https://github.com/rajeevkrsingh17/IntelliDocs-AI
