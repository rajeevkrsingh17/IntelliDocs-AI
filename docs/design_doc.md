# IntelliDocs-AI Design Document

## Project Information

**Project Name:** IntelliDocs-AI

**Problem Statement Code:** I2 – Document Q&A (RAG over a Focused Corpus)

**Developer:** Rajeev Kumar

---

# Project Overview

IntelliDocs-AI is an AI-powered document question answering system designed to help users interact with PDF documents using natural language. Instead of manually searching through lengthy documents, users will be able to ask questions and receive relevant answers extracted from the document.

The project follows the Retrieval-Augmented Generation (RAG) approach, where relevant document content is retrieved before generating a response using a Large Language Model (LLM).

---

# Problem Statement

Reading long PDF documents to find specific information is time-consuming and inefficient. Users often struggle to locate relevant sections quickly.

This project aims to simplify document understanding by automatically extracting document content and building the foundation for an intelligent question answering system.

---

# Objectives

- Extract text from PDF documents.
- Organize the extracted content for future processing.
- Build the foundation of a RAG-based application.
- Maintain a clean and modular project structure.
- Develop an AI-powered document assistant.

---

# System Workflow

```
PDF Document
      │
      ▼
PyMuPDF Text Extraction
      │
      ▼
Extracted Text
      │
      ▼
(Week 2)
Generate Embeddings
      │
      ▼
(Week 2)
Store in ChromaDB
      │
      ▼
(Future)
Retrieve Relevant Context
      │
      ▼
LLM
      │
      ▼
Generated Answer
```

---

# Week 1 Progress

The following tasks have been completed during Week 1:

- Created a public GitHub repository.
- Prepared project documentation.
- Selected the technology stack.
- Organized the project folder structure.
- Implemented PDF text extraction using PyMuPDF.
- Successfully tested the extraction process with a sample PDF.

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| PDF Processing | PyMuPDF |
| AI Framework | LangChain *(Planned)* |
| Vector Database | ChromaDB *(Planned)* |
| User Interface | Streamlit *(Planned)* |
| Version Control | Git & GitHub |

---

# Future Development

The next stages of the project will focus on:

- Generating document embeddings.
- Integrating ChromaDB.
- Building semantic document retrieval.
- Implementing the Retrieval-Augmented Generation (RAG) pipeline.
- Developing an interactive Streamlit application.
- Improving response quality using modern embedding models.