# ADR-002: Google Gemini as the Large Language Model

## Status

Accepted

## Context

The project requires a Large Language Model (LLM) capable of generating context-aware answers from retrieved document chunks. The model should be easy to integrate with Python, provide high-quality responses, and support Retrieval-Augmented Generation (RAG).

## Decision

Google Gemini was selected as the LLM for IntelliDocs-AI.

The retrieved document chunks from ChromaDB are supplied as context to Gemini, which generates an answer based only on the retrieved information.

## Consequences

### Positive

- Easy API integration
- High-quality natural language responses
- Supports RAG workflows
- Fast response time
- Well-documented SDK

### Negative

- Requires an API key
- Depends on internet connectivity
- Subject to API quotas and limits

## Alternatives Considered

### OpenAI GPT

Rejected because it requires a paid API for extended usage.

### Local LLMs

Rejected due to higher hardware requirements and slower inference for this internship project.