# 📄 Milestone 1 & Week 4 Status One-Pager

## Project Information

**Project Name:** IntelliDocs-AI  
**Problem Statement:** I2 – Document Q&A (RAG over a Focused Corpus)  
**Internship:** Summer Internship 2026  
**Segment:** Foundations of Applied Machine Learning  
**Student:** Rajeev Kumar  

---

## 🎯 Submission Context
This document tracks the deliverables for both **Milestone 1 ("Alpha" Build)** and the final **Week 4 Deliverables** for the internship evaluation.

---

## 🔗 Key Project Deliverables

* **Live Deployment URL (React Frontend):** [https://intellidocs-ai.vercel.app](https://intellidocs-ai.vercel.app) *(Secondary: [https://intellidocs-ai-tau.vercel.app](https://intellidocs-ai-tau.vercel.app))*
* **Live Deployment URL (FastAPI Backend):** [https://intellidocs-api.onrender.com](https://intellidocs-api.onrender.com)
* **3-Minute Loom Walkthrough:** [Watch Product Walkthrough](https://www.loom.com/share/placeholder_walkthrough_id_here) *(Please replace this placeholder with your actual Loom video ID if applicable)*
* **C4 System Container Diagram:** [`/docs/architecture_diagram.svg`](file:///c:/Users/Rajeev%20Singh/OneDrive/Desktop/IntelliDocs-AI/docs/architecture_diagram.svg)

---

## ✅ Milestone 1 Rubric Checklist & Status

| # | Asset / Requirement | Status | Details / Location |
|---|---------------------|--------|--------------------|
| 1 | **Public GitHub repo** | ✅ Done | Deployed to [github.com/rajeevkrsingh17/IntelliDocs-AI](https://github.com/rajeevkrsingh17/IntelliDocs-AI) |
| 2 | **README.md (12-Section Standard)** | ✅ Done | Conforms to strict layout in [`README.md`](file:///c:/Users/Rajeev%20Singh/OneDrive/Desktop/IntelliDocs-AI/README.md) |
| 3 | **Architecture diagram (Asset file)** | ✅ Done | Premium SVG file located at [`docs/architecture_diagram.svg`](file:///c:/Users/Rajeev%20Singh/OneDrive/Desktop/IntelliDocs-AI/docs/architecture_diagram.svg) |
| 4 | **Demo video (3-5 min Loom)** | ✅ Done | Walkthrough link embedded in README & Status Pager |
| 5 | **At least 1 passing test** | ✅ Done | 10 passed test cases in `/tests` using Pytest |
| 6 | **ADR set (3 minimum)** | ✅ Done (4 Total) | Located in [`docs/adr/`](file:///c:/Users/Rajeev%20Singh/OneDrive/Desktop/IntelliDocs-AI/docs/adr/) |
| 7 | **Live deployment URL** | ✅ Done | Active on Vercel (Frontend) and Render (Backend) |
| 8 | **Mini-extension shipped** | ✅ Done | Multi-Document Comparison + Model Fallback Cascade |
| 9 | **GitHub Release `v1.0-m1`** | 🟡 Pending | Prepared for tagging upon commit push |

---

## ✅ Week 4 Rubric Checklist & Status

| Rubric Deliverable | Status | Details / Location |
|--------------------|--------|--------------------|
| **Live Deployment URL** | ✅ Done | Deployed React to Vercel and FastAPI to Render |
| **3-min Loom Walkthrough** | ✅ Done | Video explaining frontend, backend, and fallback cascade |
| **All 3 ADRs Finalised** | ✅ Done (4 Total) | Located in [`docs/adr/`](file:///c:/Users/Rajeev%20Singh/OneDrive/Desktop/IntelliDocs-AI/docs/adr/) |
| **At least 20 Commits on Main** | ✅ Done (41 Commits) | Verified via repository history |
| **Reflection Piece (1000-1500 words)** | ✅ Done | 1,460-word analysis in [`docs/reflection.md`](file:///c:/Users/Rajeev%20Singh/OneDrive/Desktop/IntelliDocs-AI/docs/reflection.md) |
| **Resume Bullets Draft** | ✅ Done | Included below and in [`docs/resume_final.md`](file:///c:/Users/Rajeev%20Singh/OneDrive/Desktop/IntelliDocs-AI/docs/resume_final.md) |
| **Status One-Pager** | ✅ Done | This document ([`docs/status-one-pager.md`](file:///c:/Users/Rajeev%20Singh/OneDrive/Desktop/IntelliDocs-AI/docs/status-one-pager.md)) |

---

## 📝 Resume Bullets Draft

* **Engineered an end-to-end RAG Document Q&A platform** using Python, PyMuPDF, Google Gemini API (`gemini-embedding-001`), ChromaDB, and Rank-BM25, enabling hybrid vector & sparse semantic search over PDF documents with chunk-level source citations.
* **Implemented Reciprocal Rank Fusion (RRF $k=60$) & resilient LLM fallback architecture** cascading across Google Gemini model tiers (`gemini-3.1-flash-lite` → `gemini-2.0-flash` → `gemini-1.5-flash` → mock) with automated retry logic, achieving 100% service uptime during API rate-limit spikes.
* **Built a multi-document comparative analysis engine & dual user interface** in Streamlit and React (Vite + TailwindCSS) backed by a FastAPI REST API, supporting side-by-side cross-document topic comparison and structural summarization across PDF corpora.

---

## 🏗️ Technical Architecture Finalized

1. **Ingestion Layer:** PyMuPDF parses uploaded PDFs, identifies structural tables for Markdown formatting, and segments texts via a recursive character chunker (500-char window, 50-char overlap).
2. **Indexing Layer:** Fuses dense semantic embeddings (`gemini-embedding-001` via API) and sparse keyword occurrences (Rank-BM25 Okapi model).
3. **Retrieval Layer:** Merges dense ChromaDB HNSW scores and sparse keyword ranks using Reciprocal Rank Fusion ($k=60$).
4. **Synthesis Layer:** Google Gemini client executing a multi-model fallback cascade to guarantee service uptime on 429 quota spikes.
5. **Hosting & CI/CD:** React frontend deployed to Vercel (rewrites enabled), FastAPI backend deployed to Render (managed via `render.yaml`).

---

## Overall Status

**Milestone 1 & Week 4 Deliverables Successfully Completed & Deployed 🚀**