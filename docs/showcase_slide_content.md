# IntelliDocs-AI — Final Showcase Slide Content

*Use this text to build your 1-page presentation slide (e.g., in Canva, PowerPoint, or Google Slides).*

---

### **TITLE:** 
**IntelliDocs-AI: Resilient, Hybrid RAG Platform**

### **SUBTITLE:** 
*Chat with your PDFs without hallucination.*

### **THE PROBLEM:**
Standard LLMs hallucinate when asked about proprietary documents. Basic RAG systems fail when asked for exact keywords (e.g., "Error code 404X") and often crash under rate limits or memory constraints in production.

### **THE SOLUTION:**
An end-to-end Document Q&A platform featuring:
1. **Hybrid Search Engine:** Combines ChromaDB (semantic meaning) with Rank-BM25 (exact keyword matching) using Reciprocal Rank Fusion ($k=60$).
2. **Resilient Cascade:** Automatically fails over across Gemini model tiers (`3.1-flash-lite` → `2.0-flash` → `mock`) to guarantee 100% uptime during API rate limits.
3. **Optimized Infrastructure:** Migrated from local PyTorch models to Gemini Embeddings to successfully deploy within a strict 512MB RAM constraint on Render.

### **THE TECH STACK:**
- **Frontend:** React 19 + Vite + TailwindCSS (Deployed on Vercel)
- **Backend:** FastAPI + Uvicorn (Deployed on Render)
- **AI/Data:** PyMuPDF, ChromaDB, Rank-BM25, Google Gemini API

### **KEY METRIC / HIGHLIGHT:**
*Reduced backend memory footprint from ~800MB to ~150MB, allowing seamless deployment on free-tier cloud infrastructure while maintaining hybrid search accuracy.*

---
*(Note: Add a screenshot of your React UI on the right side of the slide, and perhaps a small graphic of your architecture diagram!)*
