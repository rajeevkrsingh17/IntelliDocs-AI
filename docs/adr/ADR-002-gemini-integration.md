# ADR-002: Google Gemini as the Primary LLM and Embedding Provider

## Status

**Accepted** — Implemented in production

## Date

2026-07-08

## Context

IntelliDocs-AI requires two distinct AI model capabilities:

1. **Embedding Model** — to convert text chunks into dense vector representations for semantic similarity search.
2. **Generative LLM** — to synthesize grounded, context-aware natural language answers from the top-k retrieved document chunks.

The initial design used **Sentence Transformers** (`all-MiniLM-L6-v2` via PyTorch) for local embeddings and planned to use a cloud LLM for generation. However, during Week 3 cloud deployment to Render's free tier, the local Sentence Transformers model failed to load — PyTorch + model weights consumed approximately 800 MB of RAM, exceeding the 512 MB hard limit of Render's free container.

This triggered a mandatory architectural decision: **migrate the embedding workload from a local model to an external cloud API** that imposes near-zero in-process memory overhead.

The requirements for the replacement:
- Produces high-dimensional dense vectors suitable for semantic similarity search.
- Available via a lightweight Python SDK client (no model weights loaded into process memory).
- Free API tier sufficient for the scale of this internship project.
- The same provider should also offer a production-quality generative LLM to reduce the number of API credentials and SDK clients the system must manage.

## Decision

**Google Gemini API** is selected for both the embedding and generation layers:

| Use | Model | Output |
|-----|-------|--------|
| Dense embeddings | `gemini-embedding-001` | 768-dimensional float vectors |
| Answer generation (Primary) | `gemini-2.0-flash` | Natural language answer from context chunks |
| Answer generation (Fallback 1) | `gemini-1.5-flash` | Same as above on 429 quota exhaustion |

The embedding call is issued once per chunk at ingestion time, and once per user query at retrieval time. The generative call is issued once per user question with the top-k retrieved chunks as context.

All API calls are made via the official `google-genai` Python SDK:
```python
import google.genai as genai
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

The multi-tier generative fallback cascade is documented in detail in **ADR-004**.

## Alternatives Considered

### OpenAI GPT-4 / GPT-3.5 Turbo + `text-embedding-ada-002`
- **Strengths:** Industry-leading generation quality, large context window, well-documented.
- **Why rejected:** Requires a paid API key after a limited trial. GPT-3.5 free tier is severely restricted and GPT-4 has no meaningful free access. Budget constraints during this internship made this impractical.

### Cohere Embed + Command R+
- **Strengths:** Cohere's embedding models are specifically tuned for retrieval tasks; Command R+ supports RAG natively.
- **Why rejected:** Free tier API limits are tighter than Google's. Less familiarity with the SDK. Would introduce a second API provider when Google Gemini can handle both embedding and generation.

### Local Ollama (Llama 3 / Mistral)
- **Strengths:** Fully offline, no API quota constraints, strong generative quality.
- **Why rejected:** Render's free tier has no GPU support and minimal CPU power. Running a quantized 7B LLM locally on Render's free container would produce unacceptably slow inference (30-60+ seconds per query). Also, local embedding models (the original SentenceTransformers approach) already failed the memory constraint — a full LLM would be far worse.

### HuggingFace Inference API
- **Strengths:** Free access to many open-source models.
- **Why rejected:** Rate limits are severe on the free plan. Response times are unpredictable. The consistency and reliability required for a demo deployment could not be guaranteed.

## Consequences

### Positive
- **Near-zero memory footprint:** The `google-genai` SDK is a thin HTTP client. All model computation happens on Google's infrastructure — memory usage on Render stays below 200 MB.
- **Unified API key:** A single `GEMINI_API_KEY` environment variable powers both embeddings and generation, simplifying deployment configuration.
- **High embedding quality:** `gemini-embedding-001` produces 768-dimensional vectors with strong semantic capture, validated by retrieval relevance tests in `tests/test_search.py`.
- **Multi-model fallback synergy:** Because all generative tiers use the same Google `genai` SDK, the fallback cascade (`gemini-2.0-flash` → `gemini-1.5-flash`) requires no additional credentials and the same code path handles all tiers.

### Negative
- **API latency per chunk:** Every document chunk requires an outbound HTTPS call to Google's embedding endpoint during ingestion, adding ~100–300 ms network latency per chunk compared to local model inference (which is instant once loaded).
- **API rate limit exposure:** The free tier of Gemini API has per-minute request limits. For large documents with many chunks, ingestion can trigger 429 errors. This is mitigated at the generation level via the fallback cascade (ADR-004), but embedding 429s during ingestion still require retry logic in `vector_store.py`.
- **Vendor lock-in:** The system depends on Google's API infrastructure. If Google deprecated `gemini-embedding-001`, all existing ChromaDB collections would need to be re-indexed with a replacement embedding model to preserve dimensionality compatibility.

## Related ADRs

- **ADR-001** — ChromaDB (stores and retrieves the `gemini-embedding-001` vectors).
- **ADR-004** — LLM Fallback Cascade (handles 429 rate limits at the generation layer using cascaded Gemini models).