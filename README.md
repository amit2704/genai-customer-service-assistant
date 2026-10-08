# Enterprise GenAI Customer Service Assistant — Production-Oriented RAG

A portfolio implementation of an enterprise customer-service assistant using **RAG, hybrid retrieval, reranking, FastAPI, JWT authentication concepts, and optional Langfuse observability**.

> This repository is a portfolio/demo implementation. It contains no Vodafone/VOXI proprietary data, code, credentials, or internal systems.

## Architecture

```text
                       ┌──────────────────┐
                       │ Enterprise Docs  │
                       └────────┬─────────┘
                                │
                    Clean → Chunk → Embed
                                │
                                ▼
                         FAISS Vector Index
                                │
User ──► FastAPI ──► Auth/RBAC ──► Query
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
              Vector Search              BM25
                    │                       │
                    └───────────┬───────────┘
                                ▼
                     Hybrid / RRF Retrieval
                                │
                                ▼
                           Reranker
                                │
                                ▼
                       Top Relevant Chunks
                                │
                                ▼
                      Grounded Prompt
                                │
                                ▼
                              LLM
                                │
                                ▼
                       Answer + Sources
                                │
                                ▼
                    Optional Langfuse Trace
```

## Why hybrid retrieval?

Dense/vector retrieval is strong for semantic similarity. BM25 is useful for exact terminology, names, identifiers and policy phrases. Combining both provides a stronger first-stage candidate set before reranking.

## Why reranking?

The first-stage retriever is optimized for recall. A cross-encoder reranker performs a more expensive query-passage relevance calculation on a small candidate set and improves precision before context is sent to the LLM.

## Security

`app/security.py` demonstrates JWT token creation/validation and role-based authorization concepts. In a real deployment, identity would normally be delegated to the enterprise identity provider rather than using a demo secret.

## Observability

`app/observability.py` provides an optional Langfuse integration point. With Langfuse credentials configured, this can be extended to capture retrieval latency, retrieved chunks, prompt/response metadata, token usage and evaluation signals.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/ingest.py
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs`.

## Interview explanation

> I designed a production-oriented RAG customer-service assistant. During ingestion, documents are cleaned, recursively chunked and embedded into a vector index. At query time, I combine dense vector retrieval with BM25 lexical retrieval using reciprocal-rank fusion. The candidate set is then reranked with a cross-encoder, and only the most relevant chunks are passed to the LLM through a grounded prompt. FastAPI exposes the service, Pydantic handles validation, JWT/RBAC concepts protect APIs, and Langfuse provides an observability integration point for tracing and evaluation.

## Production caveat

This is intentionally a portfolio implementation. A production system would add enterprise identity integration, a managed vector database such as Pinecone, stronger secrets management, persistent document pipelines, async/background ingestion, rate limiting, structured logging, automated evaluation, CI/CD and deployment controls.
