from app.config import settings
from app.observability import TraceManager
from app.rag.embeddings import Embedder
from app.rag.prompt import build_prompt
from app.rag.retriever import VectorRetriever
from app.rag.hybrid_retriever import HybridRetriever
from app.rag.reranker import CrossEncoderReranker
from app.services.llm import LLMService


class RAGService:
    def __init__(self):
        self.embedder = Embedder(settings.embedding_model)
        self.dense = VectorRetriever(
            settings.vector_index_path,
            settings.metadata_path,
        )
        self.retriever = None
        self.reranker = CrossEncoderReranker()
        self.llm = LLMService()
        self.trace = TraceManager()

    def _ensure_retriever(self):
        if self.retriever is None:
            self.dense.load()
            self.retriever = HybridRetriever(self.dense, self.dense.metadata)

    def answer(self, question: str, top_k: int):
        self._ensure_retriever()

        candidates = self.retriever.search(
            question,
            top_k_vector=settings.top_k_vector,
            top_k_bm25=settings.top_k_bm25,
            final_k=max(top_k, settings.top_k_final),
        )
        reranked = self.reranker.rerank(question, candidates, top_k=top_k)
        prompt = build_prompt(question, reranked)
        answer = self.llm.generate(prompt)

        sources = [
            {
                "source": x["source"],
                "chunk_id": x["chunk_id"],
                "hybrid_score": round(x["hybrid_score"], 4),
                "rerank_score": round(x["rerank_score"], 4),
            }
            for x in reranked
        ]
        self.trace.flush()
        return answer, sources
