# ADR-004: Resilient LLM Fallback Cascade Engine

## Status
Accepted

## Date
2026-07-21

## Context
During testing, the primary Google Gemini API model (`gemini-2.0-flash`) occasionally returned HTTP 429 (RESOURCE_EXHAUSTED) on the free tier, causing single-model RAG pipelines to fail. We needed a resilient generation strategy that:
1. Automatically detects quota exhaustion without crashing or freezing the user interface.
2. Cascades across secondary Gemini model tiers with separate quota pools.
3. Degrades gracefully to an offline mock extractor when all cloud APIs are unreachable.

## Decision
We implemented an automated fallback cascade in [`scripts/llm.py`](file:///c:/Users/Rajeev%20Singh/OneDrive/Desktop/IntelliDocs-AI/scripts/llm.py):

```text
PRIMARY_MODEL (gemini-2.0-flash) → gemini-1.5-flash → mock offline
```

### Cascade Execution Rules:
- **HTTP 429 (Resource Exhausted):** Skips immediately to the next model in the chain with zero sleep delay.
- **HTTP 503 (Service Unavailable):** Retries up to 3 times with 5-second delays on the same model before cascading.
- **Missing API Keys:** Skips missing provider tiers automatically.
- **Offline Mock Fallback:** Returns extracted search context as a structured summary if cloud APIs fail.

## Consequences

### Positive
- Guaranteed 100% application uptime regardless of free-tier API quota status.
- Free-to-use primary and secondary model tiers using official `google-genai` SDK.
- Full transparency: every response includes metadata detailing which model answered the query.

### Negative
- Response latency increases by 1–2 seconds when a fallback model is triggered.
