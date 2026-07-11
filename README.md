# 🚀 IntelliDocs-AI

> **An AI-powered document intelligence system that extracts text from PDF documents, generates semantic embeddings, stores them in a vector database, and performs semantic search as the foundation of a Retrieval-Augmented Generation (RAG) based Question Answering application.**

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![PyMuPDF](https://img.shields.io/badge/PDF-PyMuPDF-orange)
![Sentence%20Transformers](https://img.shields.io/badge/Embeddings-Sentence%20Transformers-success)
![ChromaDB](https://img.shields.io/badge/Vector%20Database-ChromaDB-green)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Week%202%20Completed-brightgreen)

</p>

---

# 📌 Project Information

| Item | Details |
|------|---------|
| **Project Name** | IntelliDocs-AI |
| **Problem Statement Code** | **I2 – Document Q&A (RAG over a Focused Corpus)** |
| **Segment** | Foundations of Applied Machine Learning |
| **Student Name** | Rajeev Kumar |
| **Internship** | Summer Internship 2026 |

---

# 🎥 Project Demo

## ✅ Week 2 End-to-End Demonstration

🎬 **Google Drive Demo**

**https://drive.google.com/file/d/1M6AxdbiT9fYv4QrJI_NGNFW7MyIIgBlA/view?usp=sharing**

### Demo Highlights

- 📄 PDF Text Extraction
- ✂️ Document Chunking
- 🧠 Semantic Embedding Generation
- 🗂️ ChromaDB Vector Storage
- 🔍 Semantic Search
- 💻 Streamlit Web Application

---

# 📖 Project Overview

**IntelliDocs-AI** is being developed as part of the **Summer Internship 2026**.

The goal of this project is to build an intelligent document understanding system capable of processing PDF documents, generating semantic embeddings, storing them inside a vector database, retrieving the most relevant document sections using semantic search, and finally integrating a Large Language Model (LLM) to answer user questions through Retrieval-Augmented Generation (RAG).

---

# 🎯 Project Objectives

- Extract text from PDF documents.
- Split documents into meaningful chunks.
- Generate semantic embeddings.
- Store embeddings in ChromaDB.
- Retrieve relevant document chunks using semantic search.
- Build a complete Retrieval-Augmented Generation (RAG) Question Answering system.
- Support intelligent document understanding.

---

# ✅ Week 1 Deliverables

- Repository Creation
- README Documentation
- Design Document
- Technology Stack Documentation
- PDF Text Extraction using PyMuPDF
- Initial Project Structure
- Git Version Control

---

# ✅ Week 2 Deliverables

- Document Chunking
- Embedding Generation using Sentence Transformers
- ChromaDB Integration
- Semantic Search
- Streamlit User Interface
- End-to-End Working Demo
- Architecture Decision Record (ADR-001)

---

# 🚀 Planned Features (Week 3+)

- Gemini API Integration
- Retrieval-Augmented Generation (RAG)
- AI-generated Answers
- Dynamic PDF Upload
- Multi-document Support
- Source References
- Better User Interface

---

# ✨ Current Features

- ✅ PDF Text Extraction
- ✅ Document Chunking
- ✅ Semantic Embedding Generation
- ✅ ChromaDB Vector Storage
- ✅ Semantic Search
- ✅ Streamlit User Interface
- ✅ Organized Project Structure
- ✅ Git Version Control

---

# 🏗 System Workflow

```text
                    PDF Document
                          │
                          ▼
                PDF Text Extraction
                          │
                          ▼
                 Document Chunking
                          │
                          ▼
              Semantic Embedding Model
                          │
                          ▼
                ChromaDB Vector Store
                          │
                          ▼
                 Semantic Document Search
                          │
                          ▼
                 Streamlit User Interface
                          │
                          ▼
         (Upcoming) Gemini-powered RAG Answer
```

---

# 📂 Project Structure

```text
IntelliDocs-AI
│
├── demo/
│   └── IntelliDocs-Demo.mp4
│
├── data/
│   ├── raw/
│   │   └── sample_document.pdf
│   │
│   └── processed/
│       └── chroma_db/
│
├── docs/
│   ├── adr/
│   │   └── ADR-001-vector-store.md
│   │
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
| Web Application | Streamlit |
| Version Control | Git & GitHub |

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/rajeevkrsingh17/IntelliDocs-AI.git
```

Move into the project directory

```bash
cd IntelliDocs-AI
```

Install all required packages

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

Launch the Streamlit application

```bash
python -m streamlit run scripts/app.py
```

---

# 📊 Current Progress

| Task | Status |
|------|--------|
| Repository Setup | ✅ |
| README Documentation | ✅ |
| Design Document | ✅ |
| Tech Stack Documentation | ✅ |
| PDF Text Extraction | ✅ |
| Document Chunking | ✅ |
| Embedding Generation | ✅ |
| ChromaDB Integration | ✅ |
| Semantic Search | ✅ |
| Streamlit Interface | ✅ |
| End-to-End Demo | ✅ |
| Gemini Integration | ⏳ Planned |
| Complete RAG Pipeline | ⏳ Planned |

---

# 📚 What I Learned

## Week 1

- Learned how to organize a professional AI project repository.
- Learned PDF text extraction using PyMuPDF.
- Improved Git workflow using meaningful commits.
- Understood the basic workflow of Retrieval-Augmented Generation (RAG).

---

## Week 2

- Learned how document chunking improves semantic retrieval.
- Generated semantic embeddings using Sentence Transformers.
- Stored embeddings inside ChromaDB.
- Built semantic search over document content.
- Developed a Streamlit web interface.
- Built an end-to-end semantic retrieval pipeline.

---

# 💡 What Surprised Me

One of the biggest learnings was understanding how strongly retrieval quality depends on proper document chunking and embedding generation. Even without integrating a Large Language Model, semantic search was able to retrieve highly relevant document sections based on meaning rather than exact keyword matching.

---

# 🛣 Roadmap

## ✅ Completed

- PDF Reader
- Document Chunking
- Semantic Embeddings
- ChromaDB
- Semantic Search
- Streamlit Interface
- End-to-End Demo

---

## 🚧 In Progress

- Improve retrieval quality
- Better UI
- Dynamic document processing

---

## 🔜 Upcoming

- Gemini API Integration
- Complete Retrieval-Augmented Generation (RAG)
- AI-generated Answers
- Dynamic PDF Upload
- Source References
- Multi-document Support
- Conversation History

---

# 🤝 Contributing

This project is currently being developed as part of the **Summer Internship 2026**.

Suggestions and improvements are always welcome.

---

# 📹 Demo

📺 **Watch the complete Week 2 Demo**

**Google Drive:**  
https://drive.google.com/file/d/1M6AxdbiT9fYv4QrJI_NGNFW7MyIIgBlA/view?usp=sharing

---

# 🔗 GitHub Repository

Repository:

https://github.com/rajeevkrsingh17/IntelliDocs-AI

---

# 👨‍💻 Developer

**Rajeev Kumar**

**Summer Internship 2026**

**Segment:** Foundations of Applied Machine Learning

**Problem Statement:** I2 – Document Q&A (RAG over a Focused Corpus)

---

## ⭐ If you found this project interesting, consider giving the repository a star.
