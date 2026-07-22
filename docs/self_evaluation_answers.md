# IntelliDocs-AI — Self Evaluation Answers

*Use this document to quickly copy and paste your answers into the final Google Form.*

**1. Segment chosen, problem chosen, why.**
*Answer:* I chose the Applied Machine Learning segment, specifically focusing on building a Retrieval-Augmented Generation (RAG) Document Q&A system. I chose this because I wanted to move beyond just calling LLM APIs and actually learn how to ground GenAI responses in proprietary data using vector databases and hybrid search architectures.

**2. What tool/concept felt like a breakthrough this month.**
*Answer:* Reciprocal Rank Fusion (RRF). Realizing that dense vectors (which understand meaning) often fail at exact keyword matches, and seeing how combining ChromaDB with a sparse BM25 index fixed my retrieval issues felt like a massive architectural breakthrough. It taught me that real AI engineering is about combining classical techniques with deep learning.

**3. What was the hardest week and why.**
*Answer:* Week 3 was the hardest. That's when I tried to deploy the FastAPI backend to Render's free tier (512MB RAM). Loading SentenceTransformers and PyTorch locally caused continuous Out-of-Memory (OOM) crashes. I had to rip out the local embedding models and rewrite the ingestion pipeline to use the Google Gemini Embedding API, which finally allowed it to run within the memory constraints.

**4. Rate your comfort (1-5) on: SQL, Python, Git, Docker, the core tech of your segment, the cloud platform you used, written communication.**
*Answer:*
- SQL: 3
- Python: 4
- Git: 4
- Docker: 2
- Core Tech (RAG/Embeddings/LLMs): 4
- Cloud Platform (Render/Vercel): 4
- Written Communication: 5

**5. What would you build next if you had 2 more weeks.**
*Answer:* I would implement a distributed task queue (Celery + Redis) for document ingestion. Currently, processing large PDFs blocks the FastAPI HTTP thread. Moving ingestion to an asynchronous background worker would make the system scalable and production-ready for massive documents.

**6. Which 3rd year internship segment are you now best positioned for?**
*Answer:* Applied AI Engineering / Backend Engineering (AI focus).

**7. Which 2-3 companies would you apply to first, for a 3rd year internship or pre-placement?**
*Answer:* (Insert your top 3 companies here, e.g., Postman, BrowserStack, or a Series A/B AI-focused startup).

**8. The 30-day post-internship plan: what you'll do in the next 30 days to keep the momentum.**
*Answer:* I will spend the next 30 days learning SQLAlchemy and PostgreSQL to add user authentication (OAuth) and persistent chat session history to IntelliDocs-AI, transforming it from a stateless prototype into a stateful, user-centric web application.

**9. (Optional) Anything you want the internship lead to know.**
*Answer:* Thank you for the strict focus on deployment and documentation. The architectural decisions forced by the 512MB RAM constraint on Render taught me more about production engineering than any tutorial ever has.
