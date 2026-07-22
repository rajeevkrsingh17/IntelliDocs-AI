# Technology Stack — Finalized

This document details the complete technology stack used in **IntelliDocs-AI** for PDF ingestion, semantic search, generative synthesis, and user interfaces.

## 🛠️ Production Technology Stack

| Component Layer | Technology | Specification / Version | Rationale & Usage |
|-----------------|------------|-------------------------|-------------------|
| **Core Runtime** | Python | 3.12 | Primary language for data pipelines, AI models, and REST API. |
| **PDF Extraction** | PyMuPDF (`fitz`) | 1.23+ | Extract text and structures from PDFs. Converts structural tables into clean Markdown tables via `find_tables()`. |
| **Text Segmentation** | Custom Recursive Chunker | 500 chars / 50 overlap | Retains cohesive paragraph context while preventing semantic dilution during embedding search. |
| **Dense Embeddings** | Google Gemini API | `gemini-embedding-001` | Generates 768-dimensional dense vectors via the official `google-genai` SDK. |
| **Vector DB** | ChromaDB | 1.5.9 | Local persistent HNSW vector store with metadata filtering. Uses `/tmp/chroma_db` in cloud mode. |
| **Sparse Index** | Rank-BM25 | 0.2.2 | BM25 sparse index for exact alphanumeric and keyword matching. |
| **Rank Fusion** | Reciprocal Rank Fusion | RRF ($k=60$) | Fuses dense vector and sparse keyword results into a single ranked output. |
| **Primary LLM** | Google Gemini API | `gemini-3.1-flash-lite` | Generates context-aware, grounded responses. Configured as `PRIMARY_MODEL`. |
| **Fallback LLM Cascade**| Google Gemini Cascade | `gemini-2.0-flash`, `gemini-1.5-flash` | Automated fallback sequence to prevent rate-limit errors (HTTP 429). |
| **Offline Fallback** | Local Mock Extractor | Custom built-in | Graceful offline response that extracts text snippets if cloud services are unreachable. |
| **Backend REST API** | FastAPI + Uvicorn | 0.109+ | Async API server with endpoints: `/upload`, `/query`, `/compare`, `/collections`, `/status`. |
| **Prototype UI** | Streamlit | 1.30+ | Rapid prototype interface for local testing and developer demos. |
| **Web Frontend** | React + Vite | React 19 / Vite 8 | Modern Single Page Application (SPA) with Lucide icons and TailwindCSS styling. |
| **Testing Suite** | Pytest | 9.1+ | Automated verification framework checking chunkers, retrievers, and LLM utilities. |

---

## 💻 Development Environment

- **Operating System:** Windows (local development), Linux (Render runtime environment)
- **Editor / IDE:** Visual Studio Code
- **Package Manager:** pip (virtual environments managed via `venv`)
- **Version Control:** Git & GitHub

---

## 🚀 Cloud Deployment Architecture

1. **Frontend Hosting (React SPA):**
   - Deployed on **Vercel** (`https://intellidocs-ai.vercel.app`)
   - Configured with rewrite rules in `vercel.json` to handle client-side routing.
   
2. **Backend Hosting (FastAPI REST API):**
   - Deployed on **Render** (`https://intellidocs-api.onrender.com`)
   - Uses `render.yaml` to build and launch with `uvicorn`.
   - Utilizes persistent storage directories inside `/tmp` due to Render's read-only runtime file system.