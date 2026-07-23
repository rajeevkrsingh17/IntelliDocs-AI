# IntelliDocs-AI — Final Showcase Slide Content

*Use this text to build your 1-page presentation slide (e.g., in Canva, PowerPoint, or Google Slides).*

---

### **TITLE:**
**IntelliDocs-AI: Resilient, Hybrid RAG Document Q&A**

### **SUBTITLE:**
*Ask your PDFs anything. Get grounded answers with page citations — not hallucinations.*

---

### **THE PROBLEM:**
Standard LLMs hallucinate when asked about proprietary documents. Basic RAG systems fail at exact keyword searches ("Error code 404X") and crash in production under memory constraints or API rate limits.

---

### **THE SOLUTION:**
An end-to-end Document Q&A platform with:

1. **Hybrid Search Engine**
   - ChromaDB (semantic meaning) + Rank-BM25 (exact keywords)
   - Fused via Reciprocal Rank Fusion (k=60) for best-of-both-worlds retrieval

2. **Resilient LLM Cascade**
   - Auto-fails over across Gemini model tiers on 429 rate limits
   - `gemini-2.0-flash` → `gemini-1.5-flash` → offline mock
   - 100% uptime even when primary API is quota-exhausted

3. **Production Deployment**
   - Migrated from local PyTorch (~800MB RAM) → Gemini Embeddings API (~150MB)
   - Enables free-tier cloud hosting on Render within 512MB constraint

4. **Multi-Document Comparison Engine**
   - Side-by-side analysis across multiple PDFs
   - 4 modes: Summary · Similarities · Detailed · Custom prompt

---

### **TECH STACK:**

| Layer | Technology |
|-------|-----------|
| Frontend | React 19 + Vite (Vercel) |
| Backend | FastAPI + Uvicorn (Render) |
| PDF Parsing | PyMuPDF (`fitz`) |
| Embeddings | Google Gemini `gemini-embedding-001` |
| Vector DB | ChromaDB (HNSW) |
| Sparse Index | Rank-BM25 |
| LLM | Google Gemini (multi-tier cascade) |
| Testing | Pytest (10 tests passed) |

---

### **LIVE LINKS:**

- 🌐 **Frontend:** https://intellidocs-ai-tau.vercel.app
- ⚙️ **Backend:** https://intellidocs-api-yedx.onrender.com
- 🎬 **Loom Demo:** https://www.loom.com/share/a103a99f1ece4e61bd1b851023f6724f

---

### **KEY ACHIEVEMENT:**
*Reduced backend memory footprint from ~800MB to ~150MB, enabling production deployment on free-tier cloud while maintaining full hybrid search accuracy with page-level source citations.*

---

> **Slide design tip:** Place a screenshot of the React UI on the right half, and the architecture diagram in the bottom-left corner.
