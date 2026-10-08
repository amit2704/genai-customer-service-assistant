import json
from pathlib import Path
import faiss
import numpy as np

class VectorRetriever:
    def __init__(self, index_path, metadata_path):
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self.index = None
        self.metadata = []

    def load(self):
        if not self.index_path.exists() or not self.metadata_path.exists():
            raise FileNotFoundError("Vector index not found. Run: python scripts/ingest.py")
        self.index = faiss.read_index(str(self.index_path))
        self.metadata = json.loads(self.metadata_path.read_text())

    def search(self, query_vector, top_k):
        if self.index is None:
            self.load()
        query_vector = np.asarray(query_vector, dtype="float32")
        scores, ids = self.index.search(query_vector, top_k)
        return [
            {**self.metadata[idx], "score": float(score)}
            for score, idx in zip(scores[0], ids[0]) if idx != -1
        ]
