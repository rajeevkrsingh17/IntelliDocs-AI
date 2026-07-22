# IntelliDocs-AI — Resume Bullets

- **Engineered an end-to-end RAG Document Q&A platform** using Python, PyMuPDF, Google Gemini API (`gemini-embedding-001`), ChromaDB, and Rank-BM25, enabling hybrid vector & sparse semantic search over PDF documents with chunk-level source citations.
- **Implemented Reciprocal Rank Fusion (RRF $k=60$) & resilient LLM fallback architecture** cascading across Google Gemini model tiers (`gemini-3.1-flash-lite` → `gemini-2.0-flash` → `gemini-1.5-flash` → mock) with automated retry logic, achieving 100% service uptime during API rate-limit spikes.
- **Built a multi-document comparative analysis engine & dual user interface** in Streamlit and React (Vite + TailwindCSS) backed by a FastAPI REST API, supporting side-by-side cross-document topic comparison and structural summarization across PDF corpora.
