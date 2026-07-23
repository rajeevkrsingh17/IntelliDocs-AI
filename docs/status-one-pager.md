# 📄 Week 4 & Milestone 2 Status One-Pager

## Project Information

**Project Name:** IntelliDocs-AI  
**Problem Statement:** I2 – Document Q&A (RAG over a Focused Corpus)  
**Internship:** Summer Internship 2026 (22 June – 26 July 2026)  
**Segment:** Foundations of Applied Machine Learning  
**Student:** Rajeev Kumar  
**Institution:** Lovely Professional University, Punjab  

---

## 🔗 Key Project Links

| Resource | Link |
|----------|------|
| **Live Frontend (React + Vercel)** | [https://intellidocs-ai-tau.vercel.app](https://intellidocs-ai-tau.vercel.app) |
| **Live Backend (FastAPI + Render)** | [https://intellidocs-api-yedx.onrender.com](https://intellidocs-api-yedx.onrender.com) |
| **3-Min Loom Walkthrough** | [▶️ Watch Loom Demo](https://www.loom.com/share/a103a99f1ece4e61bd1b851023f6724f) |
| **GitHub Repository** | [github.com/rajeevkrsingh17/IntelliDocs-AI](https://github.com/rajeevkrsingh17/IntelliDocs-AI) |
| **Architecture Diagram** | [`/docs/architecture_diagram.png`](architecture_diagram.png) |

---

## ✅ Milestone 1 — Alpha Build Checklist

| # | Asset / Requirement | Status | Details / Location |
|---|---------------------|--------|---------------------|
| 1 | **Public GitHub repo** | ✅ Done | [github.com/rajeevkrsingh17/IntelliDocs-AI](https://github.com/rajeevkrsingh17/IntelliDocs-AI) |
| 2 | **README.md (12-Section Standard)** | ✅ Done | Full README with all mandatory sections in [`README.md`](../README.md) |
| 3 | **Architecture diagram** | ✅ Done | PNG + Mermaid in [`docs/architecture_diagram.png`](architecture_diagram.png) |
| 4 | **Demo video (3-5 min Loom)** | ✅ Done | [▶️ Loom Walkthrough](https://www.loom.com/share/a103a99f1ece4e61bd1b851023f6724f) |
| 5 | **At least 1 passing test** | ✅ Done | 12 tests passing across 8 suites in `/tests/` via Pytest |
| 6 | **ADR set (3 minimum)** | ✅ Done (4 ADRs) | [`docs/adr/`](adr/) — ADR-001 through ADR-004 finalised |
| 7 | **Live deployment URL** | ✅ Done | Frontend: Vercel · Backend: Render (both live) |
| 8 | **Mini-extension shipped** | ✅ Done | Multi-Document Comparison Engine + LLM Fallback Cascade |
| 9 | **GitHub Release `v1.0-m1`** | ✅ Tagged | Release tagged on main branch |

---

## ✅ Week 4 Deliverables Checklist

| Rubric Deliverable | Status | Details / Location |
|--------------------|--------|---------------------|
| **Live Deployment URL** | ✅ Done | React on Vercel · FastAPI on Render (both live) |
| **3-min Loom Walkthrough** | ✅ Done | [▶️ Watch on Loom](https://www.loom.com/share/a103a99f1ece4e61bd1b851023f6724f) |
| **All 3+ ADRs Finalised** | ✅ Done (4 Total) | [`docs/adr/`](adr/) |
| **At least 20 Commits on Main** | ✅ Done (41+ Commits) | Verified via repository commit history |
| **Reflection Piece (1000-1500 words)** | ✅ Done | [`docs/reflection.md`](reflection.md) |
| **Resume Bullets Draft** | ✅ Done | [`docs/resume_bullets.md`](resume_bullets.md) |
| **Status One-Pager** | ✅ Done | This document |

---

## ✅ Milestone 2 — Final Build Checklist

| # | Asset / Requirement | Status | Details / Location |
|---|---------------------|--------|---------------------|
| 9  | **Reflection Piece** | ✅ Done | [`docs/reflection.md`](reflection.md) — 1,460 words |
| 10 | **3rd Year Roadmap** | ✅ Done | [`docs/roadmap_3rd_year.md`](roadmap_3rd_year.md) |
| 11 | **Resume Bullets** | ✅ Done | [`docs/resume_bullets.md`](resume_bullets.md) |
| 12 | **5 Mock Interview Q&A Pairs** | ✅ Done | [`docs/mock_interview.md`](mock_interview.md) |
| 13 | **Postmortem (Bonus)** | ✅ Done | [`docs/postmortem.md`](postmortem.md) — OOM bug & embedding migration |
| 14 | **GitHub Release `v1.0-final`** | ✅ Done | Tagged on main branch |

---

## 📝 Resume Bullets Draft

- **Engineered an end-to-end RAG Document Q&A platform** using Python, PyMuPDF, `python-docx`, `python-pptx`, Google Gemini API (`gemini-embedding-001`), ChromaDB, and Rank-BM25, enabling hybrid semantic + keyword search over multi-format documents (PDF, DOCX, PPTX, MD, TXT) with chunk-level page citations deployed on Vercel + Render.
- **Implemented Reciprocal Rank Fusion (RRF $k=60$) & resilient LLM fallback architecture** cascading across Google Gemini model tiers (`gemini-3.1-flash-lite` → `gemini-2.0-flash` → `gemini-1.5-flash` → offline mock) with automated retry logic, achieving 100% API uptime under rate-limit spikes.
- **Built a multi-document comparative analysis engine & dual frontend** (Streamlit + React/Vite) backed by a FastAPI REST API, supporting side-by-side cross-document comparison across 4 analysis modes (summary, similarities, detailed, custom).

---

## 🏗️ Technical Architecture Summary

| Layer | Technology | Role |
|-------|-----------|------|
| **Ingestion** | PyMuPDF + python-docx + python-pptx | Multi-format parsing (PDF, DOCX, PPTX, MD, TXT), table extraction (PDFs), 500-char / 50-overlap segmentation |
| **Embeddings** | `gemini-embedding-001` (API) | 768-dim dense vector generation (migrated from local SentenceTransformers to fit Render RAM) |
| **Vector Store** | ChromaDB (HNSW) | Persistent local vector index with metadata filtering |
| **Sparse Index** | Rank-BM25 | Exact keyword retrieval for numeric IDs / acronyms |
| **Rank Fusion** | Reciprocal Rank Fusion (k=60) | Combines dense + sparse scores into unified ranking |
| **LLM Synthesis** | Google Gemini Cascade | Context-grounded answer generation with 3-tier fallback |
| **Backend API** | FastAPI + Uvicorn | Async REST: `/upload`, `/query`, `/compare`, `/collections`, `/status` |
| **Frontend** | React + Vite (Vercel) | SPA with document management, Q&A, and comparison UI |
| **Hosting** | Vercel (FE) + Render (BE) | Fully deployed, publicly accessible |

---

## Overall Status

**✅ Milestone 1 (Alpha), Week 4, and Milestone 2 (Final) — All Deliverables Complete 🚀**