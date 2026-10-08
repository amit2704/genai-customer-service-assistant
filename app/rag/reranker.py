from sentence_transformers import CrossEncoder


class CrossEncoderReranker:
    """Optional second-stage reranker.

    A cross-encoder directly scores (query, passage) pairs and can improve
    precision after the cheaper first-stage hybrid retrieval.
    """

    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, documents, top_k=4):
        pairs = [(query, item["text"]) for item in documents]
        scores = self.model.predict(pairs)
        ranked = sorted(
            zip(documents, scores),
            key=lambda x: float(x[1]),
            reverse=True,
        )
        output = []
        for item, score in ranked[:top_k]:
            enriched = dict(item)
            enriched["rerank_score"] = float(score)
            output.append(enriched)
        return output
