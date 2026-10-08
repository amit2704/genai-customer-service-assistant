# Interview Guide

## 30-second answer

This is an enterprise RAG assistant. I ingest and chunk documents, generate embeddings, and index them. At query time I combine vector retrieval and BM25, rerank the candidates, construct a grounded prompt, and call the LLM. FastAPI exposes the service and returns both the answer and source metadata. JWT/RBAC and Langfuse are included as production-oriented integration points.

## Key questions to prepare

1. Why RAG instead of fine-tuning?
2. Why recursive chunking?
3. How did you choose chunk size and overlap?
4. Why hybrid search?
5. Why BM25?
6. Why reranking after retrieval?
7. Why use a cross-encoder?
8. What is top-k?
9. How do you reduce hallucination?
10. How do you evaluate retrieval quality?
11. How do you secure document access?
12. How do you debug a bad answer?
13. What happens when the vector database is unavailable?
14. How do you monitor latency and token usage?
15. How would you scale ingestion and chat APIs?

## Honest project boundary

Do not claim that this demo used a particular enterprise client, proprietary data, or production infrastructure unless you personally worked with it. The repository is designed to demonstrate the technical concepts and provide code you can study and explain.
