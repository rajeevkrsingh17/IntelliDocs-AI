# Internship Reflection — Foundations of Applied Machine Learning

**Author:** Rajeev Kumar  
**Degree & Specialization:** B.Tech CSE (Artificial Intelligence & Data Engineering)  
**Institution:** Lovely Professional University  
**Internship Duration:** 22 June 2026 – 26 July 2026  
**Problem Statement Code:** I2 – Document Q&A (RAG over a Focused Corpus)  
**Project:** IntelliDocs-AI  

---

## Section 1: What I Built (280 words)

Over the past 5 weeks of this internship, I built **IntelliDocs-AI**, an end-to-end Retrieval-Augmented Generation (RAG) platform that enables users to upload PDF documents, ask complex questions in natural language, and receive accurate, citation-backed answers. The system addresses a widespread business problem: manual document search and extraction in unstructured data (such as legal contracts, research papers, and technical guides) is slow, resource-heavy, and error-prone. By combining semantic search with generative language models, the tool allows users to immediately extract factual answers grounded directly in their uploaded files. The pipeline is designed for professionals and researchers who deal with dense document corpora on a daily basis.

The underlying architecture relies on a series of steps: PyMuPDF parses uploaded PDFs and extracts text alongside structural tables; a recursive text chunker splits the text into 500-character segments with 50-character overlap; Google Gemini's `gemini-embedding-001` model converts each chunk into a 768-dimensional dense vector; ChromaDB indexes these vectors in a local HNSW database; Rank-BM25 establishes a parallel sparse keyword index; Reciprocal Rank Fusion (RRF with $k=60$) combines dense and sparse search results; and the top retrieved passages are sent as context to the Gemini API to synthesize grounded answers with chunk-level page citations.

For my mini-extension, I built two key enhancements: a **Multi-Document Comparative Analysis Engine** that allows users to run cross-document analysis in four formats (summaries, similarities, details, or custom prompts), and a **Resilient LLM Fallback Cascade Engine** that dynamically switches models (`gemini-3.1-flash-lite` → `gemini-2.0-flash` → `gemini-1.5-flash` → local mock) on 429 quota exhaustion. I chose these extensions because real-world Q&A requires synthesizing insights across multiple files, and API failures are a critical vulnerability in production RAG systems.

---

## Section 2: What I Learned About the Tools (385 words)

During the project lifecycle, I worked with four key technologies:

**1. Google Gemini API (`gemini-embedding-001` & Generative Models):**
Initially, I used local Sentence Transformers (`all-MiniLM-L6-v2`) for embeddings. However, during cloud deployment on Render's free tier, the application suffered out-of-memory (OOM) failures due to PyTorch and model weights exceeding the 512MB RAM threshold. This forced me to switch to Google Gemini's cloud-based `gemini-embedding-001` API, which outputs 768-dimensional vectors. Working with Gemini taught me that LLM output is heavily dependent on context quality. If retrieval returns irrelevant chunks, even advanced models produce low-quality answers. I also learned to manage rate limits; experiencing HTTP 429 errors during concurrent API calls drove me to build the fallback cascade. For anyone learning Gemini, my advice is: focus heavily on input sanitization and prompt structure, and always design a fallback wrapper to catch rate-limit events.

**2. ChromaDB:**
I utilized ChromaDB as the primary vector store. What it actually does is handle local, high-speed vector retrieval using HNSW indexing and metadata filtering. I was surprised by its low-overhead setup in client-only mode, which requires no active database server process. The primary surprise was how metadata updates (such as matching session IDs and page numbers) could be dynamically filtered at query-time. I would tell a friend learning ChromaDB to be careful with persistent paths, clean up collections regularly to prevent lock file issues, and always structure metadata early.

**3. Rank-BM25:**
Rank-BM25 is a lightweight, pure-Python library implementing the Okapi BM25 ranking algorithm. Rather than relying on semantic meaning, it computes exact keyword match frequency across document chunks. I was surprised by how much BM25 improved overall search retrieval: while semantic vectors handle conceptual matching (e.g., "financial health"), BM25 is crucial for catching exact numeric terms, codes, or specific names. The key is combining the two via Reciprocal Rank Fusion (RRF). I would tell a friend that hybrid retrieval is not optional for business data — BM25 is essential to prevent the vector search from missing alphanumeric IDs.

**4. PyMuPDF (`fitz`):**
PyMuPDF is a fast, C-based PDF library. It does not parse text as clean strings, but rather extracts glyph coordinates from the PDF page. It was surprising how much cleanup is needed to reconstruct paragraphs and how table extraction (`find_tables()`) needs manual parsing to format as Markdown. For anyone starting with it, I'd say: treat PDF text as raw data that needs extensive cleaning before it ever reaches the chunker.

---

## Section 3: What I Learned About Myself (310 words)

Building IntelliDocs-AI forced me to face my technical preferences and work habits.

**What was easier than expected:**
Designing the backend architecture and implementing FastAPI endpoints felt very natural. I enjoyed structuring the utility modules (like the search fuse engine, chunker, and LLM cascade wrapper) and writing clean, async Python code. The mathematics behind Reciprocal Rank Fusion (RRF) also seemed much easier to implement and test than I had anticipated.

**What was harder than expected:**
Deploying to the cloud and managing hosting edge cases was challenging. Resolving the memory bottleneck on Render (debugging the PyTorch OOM, switching to API embeddings) took a full day of trial and error. I also spent a lot of time getting CORS headers to work reliably across Vercel and Render, ensuring the React frontend could talk to the API even when backend endpoints returned 500 errors.

**What kind of work I enjoyed/hated:**
I loved backend systems engineering — designing the fallback cascades, tracking rate limit parameters, and organizing session isolations. Writing tests using `pytest` was also rewarding because passing tests provided a strong guarantee of code health. On the other hand, I disliked writing CSS and tweaking the UI layout in the React frontend; aligning components, fixing responsive sidebars, and debugging styling issues felt tedious and repetitive compared to backend logic.

**Schedule and discipline:**
During Week 2, I procrastinated on documenting my architecture decisions, which led to a hectic weekend of writing ADRs. Recognizing this pattern, I forced myself in Weeks 3 and 4 to adopt a "continuous integration" mindset: committing code daily, documenting changes in real-time, and updating task sheets. This shift significantly reduced stress and kept the project on track. This taught me that I work best in structured, daily cycles rather than long, high-pressure sessions.

---

## Section 4: What I'd Do Differently (245 words)

If I were to rebuild IntelliDocs-AI from the ground up, I would make three major architectural adjustments:

First, I would implement **structural, document-aware chunking** instead of a fixed character window. Fixed-size chunking (like 500 characters) occasionally splits a sentence in half, separating key subjects from their verbs and diluting semantic embeddings. A layout-aware parser that respects headings, paragraphs, and lists would preserve logical boundaries and improve retrieval accuracy.

Second, I would build a **background task worker** (using Celery or FastAPI's `BackgroundTask` class) for document ingestion. Currently, when a user uploads a PDF, the main HTTP thread blocks while the system extracts text, generates embeddings via the Gemini API, and updates ChromaDB. For large files, this blocks the client and risks timeout errors. Decoupling ingestion to run asynchronously would make the user interface much more responsive.

Third, I would introduce **automated RAG evaluation frameworks** (like Ragas) on Day 1. Manual QA verification of 20+ sample questions is time-consuming and subjective. A quantitative pipeline to track faithfulness and answer relevance would have accelerated prompt iteration.

**What I wish my mentor had told me on Day 1:**
*"Don't spend days trying to design the perfect local architecture. Build a simple end-to-end prototype, deploy it immediately, and then iterate. Production deployment is where the real bottlenecks and constraints reveal themselves."*

---

## Section 5: What's Next — The 3rd Year Plan (240 words)

IntelliDocs-AI serves as the foundation for my 3rd-year portfolio. I intend to expand it into an enterprise-ready Document Intelligence platform over the next year.

**Phase 1 (August - October 2026): Ingestion & OCR Expansion**
I will integrate Tesseract OCR/EasyOCR to handle scanned PDFs and image-based documents. I will also add support for DOCX, PPTX, HTML, and Markdown formats, expanding the system's ingestion utility beyond raw PDF text.

**Phase 2 (November 2026 - January 2027): Agentic Retrieval**
I plan to implement agentic RAG workflows using LangGraph. The agent will analyze complex user queries, break them down into sub-questions, query separate data stores, and run an autonomous self-correction loop to verify if the retrieved context actually answers the query before compiling the final response. I will also add multi-turn conversation memory backed by Redis.

**Phase 3 (February - May 2027): Enterprise Scaling & MLOps**
I will containerize the app using Docker Compose, set up CI/CD workflows using GitHub Actions, and deploy the services on cloud infrastructure (AWS or GCP). I will also add Prometheus metrics to monitor query latency, system memory usage, and API drift.

By May 2027, this project will be positioned for the 3rd-year internship under **Problem Statement E3: Enterprise RAG over Dirty Data & Multi-Source Corpus**. The baseline architecture established this summer will give me a significant head start.
