# Mock Interview Q&A — IntelliDocs-AI

5 questions a 3rd-year internship interviewer might ask, with answers.

---

### Q1: Walk me through the architecture of your RAG system. How does data flow from PDF upload to answer generation?

**Answer:**  
The data flow has 5 stages:
1. **PDF Ingestion**: When a user uploads a PDF, PyMuPDF extracts the raw text page by page.
2. **Chunking**: The extracted text is split into 500-character chunks with 50-character overlap using a recursive character splitter, so no sentence gets cut off at a boundary without some context carrying over.
3. **Embedding**: Each chunk is converted into a 384-dimensional dense vector using the `all-MiniLM-L6-v2` Sentence Transformer model.
4. **Vector Storage**: The vectors and their metadata (source filename, chunk index) are stored in ChromaDB using persistent client mode with HNSW indexing.
5. **Retrieval + Generation**: When a user asks a question, the query is embedded into the same vector space, ChromaDB returns the top-k most similar chunks via cosine similarity, and these chunks are injected into a structured prompt sent to Google Gemini (with model fallback). The answer includes source citations showing which file and chunk the information came from.

---

### Q2: Why did you choose ChromaDB over other vector databases like Pinecone or Qdrant?

**Answer:**  
I chose ChromaDB for three reasons: (1) it runs entirely locally in persistent embedded mode — no external server or cloud account needed, which kept my setup simple and free; (2) it uses HNSW-based indexing which gives fast approximate nearest-neighbor search even with hundreds of chunks; (3) it supports metadata filtering natively, which was essential for implementing chunk-level source citations. Pinecone would require a cloud account and API key for a hosted service, and Qdrant, while excellent, adds deployment complexity I didn't need at this stage. For the 3rd year extension, I'd evaluate Qdrant or pgvector for production-scale workloads.

---

### Q3: How do you handle LLM API failures and rate limits in production?

**Answer:**  
I built an automated model fallback cascade in `scripts/llm.py`. The system tries models in this order:
1. `gemini-2.0-flash` (primary model)
2. `gemini-1.5-flash` (secondary Gemini model tier with separate quota pool)
3. Offline mock extraction (last resort local fallback)

For HTTP 429 (quota exhausted), it skips immediately to the next model — no wasted time retrying an exhausted quota. For HTTP 503 (service unavailable), it retries the same model up to 3 times with 5-second delays since the issue is usually transient. This differentiation is important: sleeping on a quota error wastes time, but sleeping on a transient error often succeeds.

---

### Q4: What is your mini-extension and what does it demonstrate beyond the basic requirement?

**Answer:**  
My mini-extension has two parts:

First, a **multi-document comparison engine** — instead of just querying a single PDF, users can upload multiple PDFs and the system retrieves context from both documents to generate comparative analysis: summaries, similarities, differences, and topic breakdowns. This demonstrates multi-document reasoning, which is a step up from single-doc RAG.

Second, a **resilient LLM fallback chain** — the system automatically cascades across Google Gemini model tiers when rate limits are hit, falling back to an offline mock mode if all cloud services are unavailable. This demonstrates production resilience thinking. Together, these show I can build beyond a tutorial — handling real-world scenarios like multi-source retrieval and API failure.

---

### Q5: If you had 2 more weeks, what single improvement would have the biggest impact on answer quality?

**Answer:**  
I'd implement **hybrid search combining BM25 keyword matching with dense vector retrieval**, merged using Reciprocal Rank Fusion (RRF). Right now I use pure dense vector search, which works well for semantic/conceptual queries ("explain the concept of inheritance") but can miss exact keyword matches ("what is on page 42" or "find function calculate_tax"). BM25 excels at exact matching while vectors excel at semantic understanding. Combining both would cover both query types, and research shows hybrid search typically improves retrieval precision by 20-30% on technical corpora. This would directly improve answer quality because better retrieval = better answers.
