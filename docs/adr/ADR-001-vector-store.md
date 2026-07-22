# ADR-001: Selection of ChromaDB as the Vector Database

## Status

**Accepted** — Implemented in production

## Date

2026-07-05

## Context

IntelliDocs-AI requires a vector database to:
1. Store 768-dimensional dense embeddings for each text chunk extracted from uploaded PDFs.
2. Perform approximate nearest-neighbour (ANN) similarity search at query time to retrieve the top-k most semantically relevant chunks.
3. Store and filter chunk-level metadata (document name, page number, chunk index, upload time) alongside each vector.

The selection had to satisfy the following constraints for this internship project:
- **Free and self-hosted** — no API keys or recurring service costs.
- **Python-native** — must integrate directly with the FastAPI backend without a separate database process or container.
- **Persistent** — embeddings should survive application restarts so re-indexing is not required on every startup.
- **Cloud-compatible** — must work within the constraints of Render's free tier (512 MB RAM, read-only filesystem outside `/tmp`).

## Decision

**ChromaDB** (`chromadb==1.5.9`) is selected as the vector database for IntelliDocs-AI.

ChromaDB operates in a **client-only embedded mode**, meaning it runs in-process with no separate server daemon required. It uses HNSW (Hierarchical Navigable Small World) indexing for approximate nearest-neighbour search and supports rich metadata storage and filtering on every collection.

**Critical deployment note:** Because Render's filesystem is ephemeral and read-only outside `/tmp`, the ChromaDB persistence path is conditionally set:
```python
DB_PATH = Path("/tmp/chroma_db") if _IS_CLOUD else BASE_DIR / "data" / "processed" / "chroma_db"
```
This is handled in [`scripts/vector_store.py`](../scripts/vector_store.py).

## Alternatives Considered

### FAISS (Facebook AI Similarity Search)
- **Strengths:** Extremely fast ANN search, battle-tested at scale, good GPU support.
- **Why rejected:** FAISS does not support metadata storage natively — you must maintain a parallel ID mapping yourself. Additionally, FAISS requires a custom serialization strategy for persistence; it does not handle this out of the box. Adding these layers would increase implementation complexity disproportionately for a 5-week internship.

### Pinecone (Managed Cloud)
- **Strengths:** Managed, scalable, enterprise-grade with strong uptime SLAs.
- **Why rejected:** Requires a paid API key after the free tier limit. API dependency for every search query would add network latency and a single point of external failure. Counter to the goal of a locally resilient system.

### Weaviate / Qdrant
- **Strengths:** Production-grade, support both dense and sparse vector indexing, very good horizontal scaling stories.
- **Why rejected:** Both require a running server (Docker container or managed cloud instance), which exceeds the complexity budget of this project. They are, however, the targeted migration path for the 3rd-year extension roadmap.

## Consequences

### Positive
- **Zero overhead setup:** No external process or credentials required. A single `chromadb.PersistentClient(path=...)` call initialises the entire database.
- **Metadata filtering at query time:** Every chunk's `document_name`, `page`, `chunk` index, and `upload_time` are stored as metadata and can be filtered during similarity search — enabling session isolation and per-document retrieval.
- **Hybrid-ready:** ChromaDB's collection model integrates cleanly alongside the Rank-BM25 sparse index for the Reciprocal Rank Fusion (RRF) hybrid search pipeline.
- **Render-compatible:** The `/tmp` path adaptation allows the system to function normally on ephemeral cloud containers.

### Negative
- **Not suitable for large-scale production:** ChromaDB's embedded mode is not designed for multi-process writes or horizontal scaling. For thousands of concurrent users or millions of document chunks, a managed vector database (Qdrant, Pinecone, Weaviate) would be required.
- **Ephemeral state on free cloud tiers:** On Render's free tier, `/tmp` is wiped between deploys, meaning all indexed documents must be re-uploaded after each new deployment. This is an acceptable limitation for a demo deployment but would not be acceptable in production.

## Related ADRs

- **ADR-002** — Google Gemini integration (provides the `gemini-embedding-001` embeddings stored in this ChromaDB instance).
- **ADR-004** — LLM Fallback Cascade (ChromaDB retrieval results are the context fed into the LLM synthesis layer).