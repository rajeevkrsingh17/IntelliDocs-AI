# IntelliDocs-AI — 3rd Year Extension Roadmap (Final)

## What this project is today (2-3 lines)
IntelliDocs-AI is an end-to-end RAG system capable of ingesting multiple document formats (PDF, DOCX, PPTX, MD, and TXT) and answering questions using a hybrid search mechanism (ChromaDB + Rank-BM25). It uses Google Gemini embeddings and a tiered Gemini LLM cascade (starting with primary model `gemini-3.1-flash-lite`) to guarantee resilience even under rate limits, deployed on Render (Backend) and Vercel (Frontend).

## The arc: where this could be by 3rd year internship (May 2027)
By my 3rd year internship applications, IntelliDocs-AI could evolve from a stateless RAG prototype into an enterprise-grade multimodal research assistant. Instead of just extracting text, it will use Vision-Language Models (VLMs) to semantically index charts and images from PDFs. Based on feedback during Milestone 2, I will also incorporate strict cost-monitoring dashboards, long-term conversational memory (PostgreSQL), and an asynchronous task queue (Celery + Redis) to handle bulk document ingestion without blocking the main API thread.

## 3rd Year Semester Plan (Aug 2026 - Dec 2026)

### Milestone 1 (Aug-Sep 2026): User Auth & Persistent Sessions
- **What I'll add:** OAuth integration (Google/GitHub) and persistent PostgreSQL database for user conversational history.
- **Tools I'll learn:** SQLAlchemy (ORM), JWT authentication, PostgreSQL, Docker Compose.
- **Time commitment:** 10-12 hours/week
- **Done looks like:** A user can log in via Google, view their past chat sessions, and pick up where they left off.

### Milestone 2 (Oct-Nov 2026): Asynchronous Document Processing
- **What I'll add:** A background worker queue for document ingestion so users don't wait for large PDFs to process on the main HTTP thread.
- **Tools I'll learn:** Redis, Celery, WebSockets (for frontend progress bars).
- **Time commitment:** 8-10 hours/week
- **Done looks like:** When a user uploads a 100-page PDF, they instantly get a "Processing... (45%)" progress bar via WebSockets.

### Milestone 3 (Nov-Dec 2026): Multimodal Document Analysis (Images & Charts)
- **What I'll add:** Extracting images and charts from PDFs using PyMuPDF and passing them to Gemini-1.5-Flash for multimodal description/indexing.
- **Tools I'll learn:** Multimodal RAG, ColPali / CLIP (conceptual), image extraction pipelines.
- **Time commitment:** 12-15 hours/week
- **Done looks like:** A user can ask "What is the trend in the revenue chart on page 4?" and get a correct, grounded answer.

## 3rd Year Internship Plan (Jun-Jul 2027)
This project maps directly to applied AI engineering internship roles where teams are building internal tools (like HR knowledge bases or financial document analyzers) using GenAI. The ability to demonstrate a scalable, asynchronous pipeline with real user state is exactly the "day one" value I want to bring to a Series A/B startup or mid-sized tech company.

## What I'll need from the placement / mentor ecosystem
- Mentorship on deploying distributed systems (managing Celery workers and Redis on cloud platforms).
- Access to backend/MLOps developer communities for architectural code reviews on the VLM indexing strategy.
- Guidance on best practices for designing scalable database schemas for conversational AI.

## Risks & open questions
- **Cost Scaling:** Indexing images and maintaining persistent Vector DB/PostgreSQL instances can quickly exceed free tiers. I need to learn strict cost optimization and caching (e.g., Redis Semantic Cache).
- **Complexity:** Moving from a simple FastAPI server to a distributed system (Workers + Queues + DB) vastly increases the surface area for bugs and deployment failures.
