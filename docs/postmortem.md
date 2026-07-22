# Postmortem: Render Deployment OOM & Embedding Migration

## Summary
During the initial deployment of the FastAPI backend to Render's free tier, the application repeatedly crashed on startup. The root cause was an Out-Of-Memory (OOM) exception triggered by loading the `SentenceTransformers` library and its local PyTorch model (`all-MiniLM-L6-v2`) into a memory-constrained container (512MB RAM).

---

## Timeline

| Time | Event |
|------|-------|
| Week 3, Day 5 | First successful local test of the FastAPI backend. |
| +2 hours | Deployed the backend to Render's free tier. |
| +5 min | Deployment marked as "Failed". Render logs indicated the process was killed by the OS (OOM-killer). |
| +30 min | Attempted fix: Reduced worker count in Uvicorn to `workers=1` — failed, still OOM'd. |
| +2 hours | Diagnosed memory footprint: `SentenceTransformers` and PyTorch were consuming ~800MB RAM at startup. |
| +4 hours | Architected migration plan: Move from local embeddings to an external API (`gemini-embedding-001`). |
| +6 hours | Refactored `vector_store.py` and `search.py` to use the `google-genai` client for embedding generation. |
| +8 hours | Redeployed to Render. Application started successfully with ~150MB RAM usage. |

---

## Root Cause
1. The application relied on `SentenceTransformers` (`all-MiniLM-L6-v2`) for generating dense vectors locally.
2. Local deep learning models require loading the model weights into system RAM. PyTorch and the model combined required approximately 800MB of RAM.
3. Render's free tier imposes a strict 512MB RAM limit. When the application attempted to load the model into memory, the OS terminated the process to protect system stability.

---

## What I Fixed
1. **Migrated to Cloud Embeddings**: Removed `SentenceTransformers` and `PyTorch` from `requirements.txt`.
2. **Integrated Google Gemini API**: Updated the embedding pipeline to use `gemini-embedding-001` via the `google-genai` SDK.
3. **Persisted ChromaDB**: Since Render's free tier filesystem is ephemeral, I configured ChromaDB to persist in the `/tmp` directory, which is the standard location for temporary state on serverless platforms.

---

## Lessons Learned
- **Know your deployment constraints**: Designing a system that works locally on a 16GB RAM laptop doesn't mean it will work in a constrained production environment. Always profile memory usage before deploying.
- **Architectural Trade-offs**: Moving embeddings to the cloud saved memory but introduced network latency (API calls) for every chunking operation. In this case, the trade-off was necessary to fit within hosting constraints, but it highlighted the push-and-pull of system design.
- **Cloud Ephemerality**: Learning how to manage persistent state (like a vector database) in ephemeral containers requires careful path mapping (`/tmp/chroma_db`).
