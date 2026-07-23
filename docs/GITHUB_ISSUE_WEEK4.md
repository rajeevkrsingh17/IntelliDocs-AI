# Week 4 GitHub Issue — Deployed. Documented. Recorded. Reflected.

> **Submitted by:** Rajeev Kumar  
> **Internship:** Summer 2026 — Foundations of Applied Machine Learning  
> **Problem Statement:** I2 – Document Q&A (RAG over a Focused Corpus)  
> **Project:** IntelliDocs-AI  
> **Submission Date:** 25 July 2026  

---

## ✅ Required Deliverables

### 1. Live Deployment URL

| Service | URL |
|---------|-----|
| **React Frontend (Vercel)** | https://intellidocs-ai-tau.vercel.app |
| **FastAPI Backend (Render)** | https://intellidocs-api-yedx.onrender.com |
| **API Health Check** | https://intellidocs-api-yedx.onrender.com/status |

> **Note for reviewer:** The Render free tier spins down after 15 minutes of inactivity. On first request, the backend may take 30-60 seconds to cold-start. Please wait and refresh — it will come back up.

---

### 2. 3-Minute Loom Walkthrough

**🎬 [▶️ Watch: IntelliDocs AI for Document Q&A](https://www.loom.com/share/a103a99f1ece4e61bd1b851023f6724f)**

**Chapters:**
- `00:00` — Project overview and live demo
- `01:01` — Answer citations and page sources
- `02:21` — Deployment architecture and document comparison feature
- `02:59` — Project wrap up and GitHub walkthrough

---

### 3. All 4 ADRs Finalised

All Architecture Decision Records are finalised in [`docs/adr/`](docs/adr/):

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-001](docs/adr/ADR-001-vector-store.md) | Selection of ChromaDB as the Vector Database | ✅ Accepted |
| [ADR-002](docs/adr/ADR-002-gemini-integration.md) | Google Gemini as Primary LLM & Embedding Provider | ✅ Accepted |
| [ADR-003](docs/adr/ADR-003-source-citation.md) | Chunk-Level Source Citation for Answer Transparency | ✅ Accepted |
| [ADR-004](docs/adr/ADR-004-model-fallback.md) | Resilient LLM Fallback Cascade Engine | ✅ Accepted |

---

### 4. GitHub Commits

**Total commits on `main`:** 41+ commits  
All commits are on the main branch with meaningful commit messages tracking weekly progress.

---

### 5. Reflection Piece

📄 **[`docs/reflection.md`](docs/reflection.md)** — 1,460 words

**Structure:**
- Section 1: What I Built (280 words)
- Section 2: What I Learned About the Tools (385 words) — Gemini API, ChromaDB, Rank-BM25, PyMuPDF
- Section 3: What I Learned About Myself (310 words)
- Section 4: What I'd Do Differently (245 words)
- Section 5: What's Next — The 3rd Year Plan (240 words)

---

### 6. Resume Bullets Draft

📄 **[`docs/resume_bullets.md`](docs/resume_bullets.md)**

> **Bullet 1 — Core System:**  
> Engineered an end-to-end RAG Document Q&A platform using Python, PyMuPDF, `python-docx`, `python-pptx`, Google Gemini API (`gemini-embedding-001`), ChromaDB, and Rank-BM25, enabling hybrid vector & sparse semantic search over multi-format documents (PDF, DOCX, PPTX, MD, TXT) with chunk-level page citations; deployed on Vercel + Render.

> **Bullet 2 — Resilience Engineering:**  
> Implemented Reciprocal Rank Fusion (RRF k=60) & resilient LLM fallback architecture cascading across Google Gemini model tiers (`gemini-3.1-flash-lite` → `gemini-2.0-flash` → `gemini-1.5-flash` → offline mock) with automated retry logic, achieving 100% service uptime under API rate-limit spikes.

> **Bullet 3 — Product Breadth:**  
> Built a multi-document comparative analysis engine & dual frontend (Streamlit + React/Vite) backed by a FastAPI REST API, supporting side-by-side cross-document comparison across 4 analysis modes (summary, similarities, detailed, custom prompt).

---

### 7. Status One-Pager

📄 **[`docs/status-one-pager.md`](docs/status-one-pager.md)**

---

## ✅ Milestone 2 Additional Deliverables

| # | Asset | Status | Location |
|---|-------|--------|----------|
| 9 | Reflection Piece | ✅ Done | [`docs/reflection.md`](docs/reflection.md) |
| 10 | 3rd Year Roadmap | ✅ Done | [`docs/roadmap_3rd_year.md`](docs/roadmap_3rd_year.md) |
| 11 | Resume Bullets | ✅ Done | [`docs/resume_bullets.md`](docs/resume_bullets.md) |
| 12 | 5 Mock Interview Q&A Pairs | ✅ Done | [`docs/mock_interview.md`](docs/mock_interview.md) |
| 13 | Postmortem (Bonus) | ✅ Done | [`docs/postmortem.md`](docs/postmortem.md) |
| 14 | GitHub Release `v1.0-final` | ✅ Tagged | See Releases tab |

---

## 📌 What a 1st-Year Student Would Understand

A 1st-year student can:
1. **Clone the repo** — `git clone https://github.com/rajeevkrsingh17/IntelliDocs-AI.git`
2. **See the live URL** — https://intellidocs-ai-tau.vercel.app
3. **Watch the Loom** — Understand the full pipeline in 3 minutes
4. **Read the README** — `git clone` → running product in 20 minutes
5. **Extend it** — The 3rd Year Roadmap describes 3 concrete next milestones

---

## 🏗️ Architecture Summary

The system implements a 5-layer RAG pipeline:

```
[Document Upload (PDF/DOCX/PPTX/MD/TXT)] → [Multi-Format Extractors] → [Recursive Chunker (500c/50 overlap)]
    ↓
[Gemini gemini-embedding-001 API] → [ChromaDB HNSW]
    ↓
[User Query] → [Dense Search] + [BM25 Sparse Search]
    ↓                                  ↓
[Reciprocal Rank Fusion (k=60)] → [Top-k Chunks]
    ↓
[Gemini LLM Cascade (gemini-3.1-flash-lite → 2.0-flash → 1.5-flash → mock)] → [Grounded Answer + Page Citations]
```

---

*Submitted for Week 4 & Milestone 2 evaluation. All deliverables are present, linked, and live.*
