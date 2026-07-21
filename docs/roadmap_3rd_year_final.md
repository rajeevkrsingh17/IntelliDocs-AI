# IntelliDocs-AI — 3rd Year Extension Roadmap (Final Version)

*Updated post-Milestone 2 review. This is the archived version.*

## What this project is today (2-3 lines)
IntelliDocs-AI is a Retrieval-Augmented Generation (RAG) system built with Python, PyMuPDF, Sentence Transformers (`all-MiniLM-L6-v2`), ChromaDB, and Google Gemini. It supports PDF upload, semantic question answering with source citations, multi-document comparison, and an LLM fallback chain ensuring 100% uptime.

## The arc: where this could be by 3rd year internship (May 2027)
By May 2027, IntelliDocs-AI will be a production-grade **Document Intelligence Platform** with multi-format ingestion, hybrid search, agentic multi-step reasoning, conversation memory, containerized deployment, and automated RAG evaluation. It maps directly to 3rd year Problem Statement **E3: Enterprise RAG over Dirty Data & Multi-Source Corpus**.

---

## 3rd Year Semester Plan (Aug 2026 - Dec 2026)

### Milestone 1 (Aug-Sep 2026): Hybrid Search & Multi-Format Ingestion
- **What I'll add**: BM25 + dense vector hybrid search with Reciprocal Rank Fusion. DOCX/PPTX/HTML/Markdown ingestion. OCR for scanned PDFs.
- **Tools I'll learn**: Rank-BM25, Unstructured.io, Tesseract OCR, Qdrant.
- **Time commitment**: 8-10 hours/week.
- **Done looks like**: System ingests scanned PDFs and Word files, hybrid search improves retrieval precision by ~25% vs pure vector search.

### Milestone 2 (Oct-Nov 2026): Agentic RAG & Conversation Memory
- **What I'll add**: Query decomposition, sub-query retrieval, self-verification loops. Multi-turn conversation memory with Redis. User authentication with JWT.
- **Tools I'll learn**: LangGraph, Redis, PostgreSQL + pgvector, FastAPI, JWT/OAuth2.
- **Time commitment**: 10-12 hours/week.
- **Done looks like**: Users can have multi-turn conversations about documents, with the AI breaking complex questions into sub-queries and verifying citation accuracy.

### Milestone 3 (Nov-Dec 2026): Production MLOps & Cloud Deployment
- **What I'll add**: Docker Compose orchestration. GitHub Actions CI/CD. Prometheus + Grafana monitoring. Automated RAG evaluation with Ragas framework.
- **Tools I'll learn**: Docker, GitHub Actions, Prometheus, Grafana, Ragas, FastAPI microservices.
- **Time commitment**: 8-10 hours/week.
- **Done looks like**: App runs via `docker-compose up`, deploys automatically on push, has live monitoring for retrieval latency and LLM drift.

---

## 3rd Year Internship Plan (Jun-Jul 2027)
This project becomes my submission for **Problem Statement E3: Enterprise RAG over Dirty Data & Multi-Source Corpus**. The 2nd year foundation (PDF ingestion, vector search, LLM integration, fallback chain) will be extended with enterprise-grade features: multi-tenancy, data contracts, fine-tuned embeddings, and production SLA guarantees.

## What I'll need from the placement / mentor ecosystem
- GPU instances (T4/A10G) for local LLM inference and embedding fine-tuning.
- Senior mentorship on agentic RAG frameworks and production MLOps patterns.
- Peer review on Docker/K8s architecture.
- Placement prep resources for AI/ML Engineering roles at product companies (Razorpay, Swiggy, Amazon, Google).

## Risks & open questions
- **Risk**: API costs at scale. *Mitigation*: Redis embedding cache + local model fallback via Ollama/vLLM.
- **Risk**: Retrieval latency degradation beyond 100K chunks. *Mitigation*: Benchmark ChromaDB vs Qdrant vs pgvector; implement sharding.
- **Open question**: How to handle multi-modal documents (images, charts in PDFs) in the RAG pipeline?
