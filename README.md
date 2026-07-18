# 🚀 IntelliDocs-AI

> **An AI-powered Retrieval-Augmented Generation (RAG) based Document Question Answering System that enables users to upload PDF documents, retrieve semantically relevant information using vector search, and generate context-aware answers with Google Gemini.**

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?logo=streamlit)
![PyMuPDF](https://img.shields.io/badge/PDF-PyMuPDF-orange)
![Sentence Transformers](https://img.shields.io/badge/Embeddings-SentenceTransformers-success)
![ChromaDB](https://img.shields.io/badge/Vector%20Database-ChromaDB-green)
![Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-blueviolet)
![Pytest](https://img.shields.io/badge/Testing-Pytest-yellow)
![GitHub](https://img.shields.io/badge/Version%20Control-Git%20%26%20GitHub-black)
![Status](https://img.shields.io/badge/Status-Week%203%20Completed-brightgreen)

</p>

---

## 🌟 Key Highlights

- 📄 Upload PDF documents
- ✂️ Automatic document chunking
- 🧠 Semantic embeddings using Sentence Transformers
- 🗂️ ChromaDB Vector Database
- 🔍 Semantic Search
- 🤖 Gemini-powered AI Answers
- 📚 Retrieval-Augmented Generation (RAG)
- 📌 Source Citation
- 🧪 Unit Testing using Pytest
- 💻 Streamlit Web Interface
 
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

# 🎥 Project Demonstration

## 📹 Demo Video

**Google Drive Demo**

https://drive.google.com/file/d/1M6AxdbiT9fYv4QrJI_NGNFW7MyIIgBlA/view?usp=sharing

### Demonstrated Features

- PDF Upload
- PDF Text Extraction
- Intelligent Chunking
- Semantic Embedding Generation
- ChromaDB Vector Search
- Gemini AI Answer Generation
- Source Citation
- Streamlit Interface

---

# 📖 Project Overview

IntelliDocs-AI is an AI-powered document intelligence application developed as part of the **Summer Internship 2026** under the **Foundations of Applied Machine Learning** segment. The project is based on the problem statement **"I2 – Document Q&A (RAG over a Focused Corpus)"** and aims to simplify document understanding through Retrieval-Augmented Generation (RAG).

The application enables users to upload PDF documents, automatically extract their contents, split the extracted text into meaningful chunks, generate semantic embeddings using **Sentence Transformers**, and store those embeddings in **ChromaDB**, enabling efficient semantic retrieval.

When a user asks a question, the system performs **semantic search** to retrieve the most relevant document chunks rather than relying solely on keyword matching. These retrieved chunks are then provided as context to **Google Gemini**, allowing the model to generate accurate, context-aware responses while reducing hallucinations.

To improve transparency and trustworthiness, the application also displays the **source document** and **chunk number** associated with the retrieved information, allowing users to verify where the generated answer originated.

The project demonstrates the complete workflow of a modern **Retrieval-Augmented Generation (RAG)** system—from **PDF ingestion**, **intelligent text chunking**, **embedding generation**, **vector storage**, **semantic retrieval**, and **AI-powered question answering**—through an interactive **Streamlit** web application.

Finally, this project provides a strong foundation for building scalable enterprise document intelligence systems. Future enhancements include **multi-document retrieval**, **hybrid search**, **conversation history**, **authentication**, and **cloud deployment**.

---

# 🎯 Project Objectives

The primary objectives of IntelliDocs-AI are:

- 📄 Extract text from PDF documents efficiently.
- ✂️ Split large documents into meaningful semantic chunks.
- 🧠 Generate high-quality vector embeddings using Sentence Transformers.
- 🗂️ Store document embeddings in ChromaDB.
- 🔍 Retrieve the most relevant document chunks using semantic search.
- 🤖 Generate accurate answers using Google Gemini.
- 📚 Implement a complete Retrieval-Augmented Generation (RAG) pipeline.
- 📌 Display source citations for retrieved information.
- 💻 Provide an interactive Streamlit-based user interface.
- 🧪 Ensure reliability through unit testing.
---

# 📅 Internship Deliverables

## ✅ Week 1 – Foundation

- Repository Created
- Public GitHub Repository
- README Documentation
- Initial Design Document
- Technology Stack Documentation
- PDF Text Extraction using PyMuPDF
- Initial Project Structure
- Git Version Control
- Data Layer Validation
- 5+ Git Commits

---

## ✅ Week 2 – End-to-End Pipeline

- Document Chunking
- Sentence Transformer Embeddings
- ChromaDB Integration
- Semantic Search
- Streamlit User Interface
- End-to-End Working Demo
- ADR-001
- 10+ Git Commits

---

## ✅ Week 3 – Mini Extension

- Google Gemini Integration
- Retrieval-Augmented Generation (RAG)
- Dynamic PDF Upload
- Source Citation
- Pytest Unit Testing
- README Enhancement
- Mini Extension Demo
- 15+ Git Commits
- ADR-002
- ADR-003
---

# ✨ Current Features

### 📄 Document Processing

- PDF Upload
- PDF Text Extraction
- Intelligent Chunking

### 🧠 Artificial Intelligence

- Sentence Transformer Embeddings
- Semantic Similarity Search
- Google Gemini Integration
- Retrieval-Augmented Generation (RAG)

### 🗂 Vector Database

- ChromaDB Storage
- Fast Vector Retrieval
- Metadata Storage
- Source Citation

### 💻 User Interface

- Streamlit Application
- Interactive PDF Upload
- AI Answer Generation
- Retrieved Context Display

### 🧪 Software Engineering

- Modular Code Structure
- Unit Testing using Pytest
- Git Version Control
- Environment Variable Support

---
# 🏗 System Architecture

```text
                        📄 PDF Upload
                              │
                              ▼
                 ┌─────────────────────────┐
                 │   PDF Text Extraction   │
                 │       (PyMuPDF)         │
                 └───────────┬─────────────┘
                             │
                             ▼
                 ┌─────────────────────────┐
                 │   Intelligent Chunking  │
                 └───────────┬─────────────┘
                             │
                             ▼
                 ┌─────────────────────────┐
                 │ Sentence Transformers   │
                 │   Embedding Generation  │
                 └───────────┬─────────────┘
                             │
                             ▼
                 ┌─────────────────────────┐
                 │ ChromaDB Vector Store   │
                 └───────────┬─────────────┘
                             │
                             ▼
                 ┌─────────────────────────┐
                 │ Semantic Retrieval      │
                 └───────────┬─────────────┘
                             │
                             ▼
                 ┌─────────────────────────┐
                 │ Google Gemini API       │
                 └───────────┬─────────────┘
                             │
                             ▼
                 ┌─────────────────────────┐
                 │ AI Generated Answer     │
                 │ + Source Citation       │
                 └─────────────────────────┘
```

---

# 📂 Project Structure

```text
IntelliDocs-AI
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── uploads/
│
├── docs/
│   ├── adr/
│   │   ├── ADR-001-vector-store.md
│   │   ├── ADR-002-gemini-integration.md
│   │   └── ADR-003-source-citation.md
│   │
│   ├── design_doc.md
│   └── tech_stack.md
│
├── scripts/
│   ├── app.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── pdf_processor.py
│   ├── search.py
│   ├── vector_store.py
│   └── __init__.py
│
├── tests/
│   └── test_chunker.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🛠 Technology Stack

| Layer | Technology |
|--------|------------|
| Programming Language | Python 3.12 |
| PDF Processing | PyMuPDF |
| Text Chunking | LangChain-style Chunking |
| Embedding Model | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector Database | ChromaDB |
| Similarity Search | Cosine Similarity |
| Large Language Model | Google Gemini |
| Frontend | Streamlit |
| Environment Variables | python-dotenv |
| Testing | Pytest |
| Version Control | Git & GitHub |

---

# ⚙️ Quick Start

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/rajeevkrsingh17/IntelliDocs-AI.git
cd IntelliDocs-AI
```

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 3️⃣ Configure Environment Variables

Create a `.env` file inside the `scripts` folder.

```text
GEMINI_API_KEY=YOUR_API_KEY
```

## 4️⃣ Run the Application

```bash
python -m streamlit run scripts/app.py
```

---

# 🧪 Run Unit Tests

```bash
pytest
```

Expected Output

```text
=============================
1 passed
=============================
```

---

# 📊 Project Progress

| Feature | Status |
|----------|--------|
| Repository Setup | ✅ |
| README Documentation | ✅ |
| Design Document | ✅ |
| Tech Stack Documentation | ✅ |
| PDF Upload | ✅ |
| PDF Text Extraction | ✅ |
| Intelligent Chunking | ✅ |
| Sentence Transformer Embeddings | ✅ |
| ChromaDB Integration | ✅ |
| Semantic Search | ✅ |
| Google Gemini Integration | ✅ |
| Retrieval-Augmented Generation (RAG) | ✅ |
| Source Citation | ✅ |
| Streamlit Interface | ✅ |
| Unit Testing | ✅ |
| End-to-End Working Demo | ✅ |

---

# 📚 What I Learned

## Week 1

- Built a structured AI project repository.
- Learned PDF text extraction using PyMuPDF.
- Understood Git version control and project organization.
- Learned the fundamentals of Retrieval-Augmented Generation (RAG).

---

## Week 2

- Learned document chunking strategies.
- Generated semantic embeddings using Sentence Transformers.
- Stored vectors in ChromaDB.
- Implemented semantic similarity search.
- Built an end-to-end retrieval pipeline.
- Developed a Streamlit web interface.

---

## Week 3

- Integrated Google Gemini API for AI-powered answers.
- Implemented a complete Retrieval-Augmented Generation (RAG) pipeline.
- Added source citations for retrieved document chunks.
- Wrote unit tests using Pytest.
- Improved project documentation and repository structure.
- Learned prompt engineering and context-based answer generation.

---

# 💡 What Surprised Me

One of the biggest learnings was discovering how much answer quality depends on retrieval quality. Better chunking and relevant document retrieval significantly improve the accuracy of the Gemini-generated response while reducing hallucinations.

---

# 🔄 What I'd Do Differently

If I started this project again, I would first design the complete project architecture before writing code. I would also implement automated testing earlier and support multiple PDF documents from the beginning to make the system more scalable.

---

# 🚀 Future Roadmap

## ✅ Completed

- PDF Upload
- PDF Text Extraction
- Intelligent Chunking
- Sentence Transformer Embeddings
- ChromaDB Vector Store
- Semantic Search
- Google Gemini Integration
- Retrieval-Augmented Generation
- Source Citation
- Streamlit Interface
- Unit Testing

---

## 🚧 In Progress

- Improve Retrieval Accuracy
- Better UI/UX
- Performance Optimization

---

## 🔜 Planned

- Multi-document Support
- Chat History
- Hybrid Search (Keyword + Vector)
- Cloud Deployment
- Docker Support
- Authentication
- Conversation Memory

---

# 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to fork this repository and submit a pull request.

---

# 📹 Project Demo

🎥 **Watch the complete Week 3 Demo**

https://drive.google.com/file/d/1M6AxdbiT9fYv4QrJI_NGNFW7MyIIgBlA/view?usp=drive_link

---

# 🔗 GitHub Repository

**Repository:**  
https://github.com/rajeevkrsingh17/IntelliDocs-AI

---

# 👨‍💻 Developer

**Rajeev Kumar**

🎓 B.Tech CSE (Artificial Intelligence & Data Engineering)

🏫 Lovely Professional University

💼 Summer Internship 2026

🤖 Segment: Foundations of Applied Machine Learning

📌 Problem Statement: **I2 – Document Q&A (RAG over a Focused Corpus)**

---

# ⭐ Support

If you found this project useful, please ⭐ star the repository.

It motivates me to continue improving the project!
