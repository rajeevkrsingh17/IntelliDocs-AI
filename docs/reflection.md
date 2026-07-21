# Internship Reflection — Foundations of Applied Machine Learning

**Author:** Rajeev Kumar  
**Degree & Specialization:** B.Tech CSE (Artificial Intelligence & Data Engineering)  
**Institution:** Lovely Professional University  
**Internship Duration:** 22 June 2026 – 26 July 2026  
**Problem Statement Code:** I2 – Document Q&A (RAG over a Focused Corpus)  
**Project:** IntelliDocs-AI  

---

## Section 1: What I Built (280 words)

Over the past 5 weeks, I built **IntelliDocs-AI**, an end-to-end Retrieval-Augmented Generation (RAG) platform that lets users upload PDF documents, ask natural-language questions, and receive accurate, citation-backed answers. The core problem it solves is simple: reading long PDF documents to find specific information is time-consuming. Instead of manually scrolling through pages, users can ask a question and the system retrieves the most relevant document passages using hybrid vector and sparse BM25 similarity search, then uses Google Gemini to generate a grounded answer.

The technical pipeline works like this: PyMuPDF extracts text and formats tables into Markdown from uploaded PDFs, a recursive character chunker splits text into 500-character segments with 50-character overlap, Sentence Transformers (`all-MiniLM-L6-v2`) converts each chunk into a 384-dimensional dense vector, ChromaDB stores vectors in a persistent HNSW index, Rank-BM25 indexes keywords, Reciprocal Rank Fusion (RRF $k=60$) merges dense and sparse results, and the top-k chunks are passed as context to Google Gemini for answer generation. Every answer includes source citations showing which document, page, and chunk the information came from.

As my **mini-extension**, I built two major features: a **Multi-Document Comparative Analysis Engine** that lets users upload multiple PDFs and compare them side-by-side across 4 modes (`summary`, `similarities`, `detailed`, `custom`), and a **Resilient LLM Fallback Chain** that automatically switches across Gemini model tiers (`gemini-2.0-flash` → `gemini-1.5-flash` → offline mock engine) when API rate limits are hit. I chose these because real-world document analysis often involves multiple files, and production systems need to handle API failures gracefully — both go far beyond what a standard single-file RAG tutorial covers.

---

## Section 2: What I Learned About the Tools (380 words)

I worked with four core tools during this internship:

**1. Sentence Transformers (`all-MiniLM-L6-v2`):** Before this project, I thought embedding models were just black boxes that convert text to numbers. Building the pipeline taught me what they actually do — they map text into a semantic space where conceptually similar content sits close together. I was surprised by how much chunk size affects embedding quality. If chunks are too large, the embedding gets diluted; too small, and you lose context. The 500-character sweet spot with 50-character overlap was something I discovered through experimentation.

**2. ChromaDB & Rank-BM25:** I chose ChromaDB as my vector database because it runs locally in persistent client mode without any external infrastructure. What surprised me was how fast the HNSW-based indexing is — even with hundreds of chunks, retrieval takes milliseconds. Combining Rank-BM25 keyword search alongside dense vectors taught me how sparse and dense representations complement each other: BM25 catches exact technical codes and page numbers, while dense vectors capture broad semantic meaning.

**3. PyMuPDF (`fitz`):** I picked this for PDF text extraction after trying alternatives. The key insight was that PDFs don't store text as readable paragraphs — they store glyph positions. PyMuPDF handles text reconstruction well, and its structural table finder (`find_tables()`) allowed me to format tables as clean Markdown tables. It's fast (C-extension under the hood), but output needs post-processing before chunking.

**4. Google Gemini API:** Working with Gemini taught me that the quality of LLM-generated answers depends more on retrieval quality than on the model itself. Even a powerful model produces bad answers if the context you feed it is noisy or irrelevant. I also learned the hard way about rate limiting — hitting HTTP 429 errors during testing is what motivated me to build the resilient model fallback chain.

If I were advising a friend starting with these tools, I'd say: *"Don't start with the LLM. Start with your data pipeline — chunking, embedding, and retrieval. If your retrieval is good, almost any LLM will produce good answers."*

---

## Section 3: What I Learned About Myself (360 words)

This internship taught me as much about my working style as it did about technology.

**What was easier than expected:** Writing clean, modular Python code. Breaking the project into separate files (`chunker.py`, `vector_store.py`, `llm.py`, `search.py`, `pdf_reader.py`, `api.py`) felt natural. I also found the vector math concepts (cosine similarity, Reciprocal Rank Fusion) intuitive once I stopped overthinking them.

**What was harder than expected:** Production edge cases. Rate limiting, handling uploaded files of different sizes, ensuring ChromaDB collections reset cleanly, and making both Streamlit and React UIs responsive — these "small" issues consumed more time than the core RAG logic. The gap between "it works on my machine with a sample PDF" and "it works reliably for any user" was much larger than I anticipated.

**What kind of work I enjoyed most:** I genuinely enjoyed the backend architecture work — designing the fallback chain, structuring the vector store helpers, writing the hybrid RRF search logic, and creating REST endpoints with FastAPI. There's something satisfying about building a system that handles failures gracefully. I also liked writing tests — seeing green checkmarks after running pytest gives a real sense of confidence.

**What kind of work I disliked:** UI styling and layout tweaking. Getting components to align properly and look clean was tedious. I respect frontend developers more now.

**Schedule discipline:** I'll be honest — in Week 2, I procrastinated on writing ADRs and pushed them to the weekend, which caused unnecessary last-minute stress. Starting Week 3, I adopted a "push something every day" habit, even if it was just a README update or a small fix. This completely changed my stress levels. The difference between "I'll do it all on Friday" and "I'll do a little each day" is massive.

**What this tells me:** I'm naturally drawn to backend/systems work in the ML space. The 3rd year internship path that excites me most involves building production ML infrastructure — not just training models, but making them reliable, observable, and maintainable.

---

## Section 4: What I'd Do Differently (240 words)

If I started IntelliDocs-AI from scratch, three things would change:

**1. Use Structural Chunking Instead of Fixed-Size:** My chunker uses a fixed 500-character window with 50-character overlap. This works, but it sometimes cuts sentences in half or splits a paragraph across two chunks. A smarter approach would chunk based on document structure — headings, paragraphs, bullet points — preserving semantic boundaries naturally.

**2. Set Up Automated RAG Evaluation Early:** I initially tested Q&A quality manually by asking questions and eyeballing answers. Setting up a formal evaluation framework (like the 22-question test suite in `docs/eval_report.md`) earlier in Week 1 would have allowed me to measure retrieval precision quantitatively from the beginning.

**3. Implement Asynchronous Indexing:** Currently, processing a 50-page PDF blocks the upload request until embedding generation completes. Offloading indexing to a background queue (e.g., Celery or FastAPI background tasks) would make the user experience much smoother.

**What I wish my mentor had told me on Day 1:** *"Get a bare-minimum end-to-end pipeline deployed by Day 3. A working ugly demo is worth infinitely more than a perfect local script you never ship."*

---

## Section 5: What's Next — The 3rd Year Plan (250 words)

IntelliDocs-AI is my foundation project. Over the next 12 months, I plan to extend it into a production-grade Document Intelligence Platform.

**Phase 1 (Aug–Oct 2026):** Add Redis embedding caching, multi-format document support (DOCX, PPTX, Markdown, HTML), and OCR for scanned PDFs using Tesseract.

**Phase 2 (Nov 2026–Jan 2027):** Implement agentic RAG workflows — the system should be able to break complex questions into sub-queries, retrieve from multiple sources, and self-verify its answers using LangGraph. Add multi-turn conversation memory using Redis.

**Phase 3 (Feb–May 2027):** Containerize the application with Docker, add CI/CD with GitHub Actions, implement observability with Prometheus/Grafana, and deploy on cloud infrastructure (AWS/GCP free tier or Railway).

By May 2027, this project will be ready for the 3rd-year internship under **Problem Code E3: Enterprise RAG over Dirty Data & Multi-Source Corpus**. The foundation I built this summer — PDF ingestion, vector search, LLM integration, fallback resilience — will be the starting point, not the starting-from-zero experience.

The most important thing I learned this month: **shipping a working thing teaches you more than planning a perfect thing.** I plan to keep that mindset through 3rd year.
