# Postmortem: API Quota Exhaustion & Multi-Model LLM Fallback

## Summary
During Week 3 integration testing, rapid automated query executions caused the Google Gemini API to return HTTP 429 (RESOURCE_EXHAUSTED). The initial single-model architecture had no fallback mechanism, resulting in unhandled exceptions in the user interface.

---

## Timeline

| Time | Event |
|------|-------|
| Week 3, Day 3 | Rapid automated testing triggered Gemini rate-limiting (HTTP 429) |
| +5 min | User-facing queries showed raw Python stack traces in Streamlit |
| +30 min | Attempted fix: simple sleep retry (30s) on the same model — caused UI freeze without success |
| +2 hours | Designed multi-model fallback architecture |
| +4 hours | Implemented and tested: `gemini-2.0-flash` → `gemini-1.5-flash` → `mock` fallback chain |
| +5 hours | Verified 100% uptime under simulated quota exhaustion |

---

## Root Cause
1. The application was coupled to a single LLM model (`gemini-2.0-flash`).
2. Free-tier API quotas are enforced per-model per-minute. When the quota was hit, retrying the same model was futile.
3. There was no error boundary — raw exceptions propagated to the user interface.

---

## What I Fixed
1. **Multi-Model Cascade**: Added `gemini-1.5-flash` as a secondary model tier with a separate quota pool.
2. **Offline Mock Fallback**: Added a final "mock" fallback that extracts and returns raw retrieved context when cloud APIs are unreachable.
3. **Differentiated Error Handling**:
   - HTTP 429 (quota): Skip immediately to next model (zero wasted delay).
   - HTTP 503 (service down): Retry same model 3 times with 5s delay.
   - Missing API key: Skip provider tier instantly.
4. **Transparent Metadata**: Every generated answer now includes metadata showing which model succeeded.

---

## Lessons Learned
- **Never rely on a single cloud API model** for a user-facing feature. Model fallback resilience is essential.
- **Differentiate error types before retrying**: sleeping on a quota error wastes user time; sleeping on a transient 503 error often works.
- **Prioritize failure path engineering**: The failure path took 4 hours and is what makes the system reliable.
