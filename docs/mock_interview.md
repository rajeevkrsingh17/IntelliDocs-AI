# Mock Interview Q&A — IntelliDocs-AI

**1. "I see you used a 'Hybrid Search' approach with ChromaDB and Rank-BM25. Why not just use standard dense vector search? What specific problem did BM25 solve for you?"**

**Answer:** Dense vector embeddings are great for semantic similarity—understanding the "meaning" of a query. But they often struggle with exact keyword matching, acronyms, or specific ID numbers. For example, if a user queries "Error code 404X-B", dense vectors might return generic error troubleshooting sections, whereas BM25 (sparse index) looks at exact term frequencies and instantly finds that precise alphanumeric string. By combining them using Reciprocal Rank Fusion (RRF), I got the best of both worlds: semantic understanding from ChromaDB and exact keyword precision from Rank-BM25.

**2. "You mentioned an OOM (Out of Memory) issue when deploying to Render. Walk me through how you identified the bottleneck and why your solution was the right architectural trade-off."**

**Answer:** When I first deployed the backend to Render's free tier, the FastAPI server kept crashing. Checking the logs, I saw the process was killed by the OS (OOM-killer). I realized that loading `SentenceTransformers` (`all-MiniLM-L6-v2`) and the PyTorch dependencies locally into memory exceeded the strict 512MB RAM limit. To fix this without paying for premium hosting, I migrated the embedding generation from the local model to an external API (`gemini-embedding-001`). The trade-off was increased network latency per document chunk, but the architectural win was a massive reduction in the memory footprint, allowing the app to run perfectly within the constraint.

**3. "Your LLM cascade is interesting. How do you handle situations where all external APIs are unreachable or rate-limited for an extended period?"**

**Answer:** I built the system with a cascading fallback strategy. It attempts `gemini-3.1-flash-lite`, falls back to `gemini-2.0-flash`, and then `gemini-1.5-flash` if 429 Rate Limit errors occur. However, if the entire API goes down or my quota is completely exhausted, the system hits the "Mock Extractor" fallback. Instead of crashing or throwing a 500 server error, the offline fallback simply returns the top retrieved verbatim text chunks from the vector database. It degrades the experience from a "conversational synthesized answer" to an "extractive search engine", but it maintains 100% uptime.

**4. "How did you decide on a chunk size of 500 characters with a 50-character overlap for your PDF ingestion? Did you try other sizes?"**

**Answer:** I experimented with larger chunks (1000+ characters), but I found it led to "lost in the middle" problems during retrieval; the dense vectors got diluted by too many topics in a single chunk. Conversely, very small chunks (100-200 characters) broke sentence context. 500 characters roughly corresponds to a medium-sized paragraph, which creates highly focused embeddings. The 50-character overlap was crucial because it ensures that if a sentence spans the boundary between two chunks, the context isn't severed, ensuring ChromaDB can still surface the relevant text.

**5. "If we hired you, and asked you to scale this system to handle 10,000 PDFs instead of a handful, what is the first architectural change you would make?"**

**Answer:** The very first change would be decoupling the document ingestion process from the HTTP request cycle. Currently, if a user uploads a PDF, the FastAPI thread blocks while extracting text, chunking, hitting the embedding API, and saving to ChromaDB. For 10,000 documents, this would cause massive timeouts. I would implement an asynchronous queue—like Celery backed by Redis. The upload endpoint would drop the PDF into an S3 bucket, push an event to the queue, and immediately return a `202 Accepted` job ID, allowing worker nodes to process the embeddings asynchronously in the background.
