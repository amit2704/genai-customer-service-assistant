import re
from collections import defaultdict

import numpy as np
from rank_bm25 import BM25Okapi


def tokenize(text: str):
    return re.findall(r"(?u)\b\w+\b", text.lower())


class HybridRetriever:
    """Combines dense semantic retrieval and BM25 lexical retrieval.

    Dense retrieval helps with semantic similarity; BM25 helps with exact
    product/policy terminology and identifiers.
    """

    def __init__(self, dense_retriever, metadata):
        self.dense = dense_retriever
        self.metadata = metadata
        self.bm25 = BM25Okapi([tokenize(x["text"]) for x in metadata])

    def search(self, query, top_k_vector=8, top_k_bm25=8, final_k=4):
        dense_results = self.dense.search(
            self.dense.embedder.encode([query]),
            top_k_vector,
        )

        bm25_scores = self.bm25.get_scores(tokenize(query))
        lexical_ids = np.argsort(bm25_scores)[::-1][:top_k_bm25]

        # Reciprocal-rank fusion gives each retrieval strategy a comparable
        # contribution without requiring scores to be on the same scale.
        scores = defaultdict(float)
        result_map = {}

        for rank, item in enumerate(dense_results, start=1):
            key = (item["source"], item["chunk_id"])
            scores[key] += 1.0 / (60 + rank)
            result_map[key] = item

        for rank, idx in enumerate(lexical_ids, start=1):
            item = dict(self.metadata[int(idx)])
            item["score"] = float(bm25_scores[int(idx)])
            key = (item["source"], item["chunk_id"])
            scores[key] += 1.0 / (60 + rank)
            result_map[key] = item

        ranked = sorted(scores, key=scores.get, reverse=True)
        return [result_map[key] | {"hybrid_score": scores[key]} for key in ranked[:final_k]]
