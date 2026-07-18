# ADR-003: Source Citation for Answer Transparency

## Status

Accepted

## Context

Large Language Models can generate answers that are difficult for users to verify. To improve transparency and trust, users should be able to identify the document source of every generated response.

## Decision

The system displays the source document name and chunk number along with each AI-generated answer. This information is retrieved from the metadata stored in ChromaDB.

## Consequences

### Positive
- Improves answer transparency
- Makes responses easier to verify
- Increases user trust
- Supports explainable AI principles

### Negative
- Slightly increases the amount of information displayed in the interface