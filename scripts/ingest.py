import json
from pathlib import Path
import faiss
import numpy as np
from app.config import settings
from app.rag.chunking import split_text
from app.rag.embeddings import Embedder

def main():
    data_dir = Path("data")
    artifacts = Path("artifacts")
    artifacts.mkdir(exist_ok=True)
    chunks = []
    for path in data_dir.glob("*.txt"):
        text = path.read_text(encoding="utf-8")
        for chunk_id, chunk in enumerate(split_text(text, settings.chunk_size, settings.chunk_overlap)):
            chunks.append({"source": path.name, "chunk_id": chunk_id, "text": chunk})
    if not chunks:
        raise RuntimeError("No .txt files found in data/")
    vectors = np.asarray(Embedder(settings.embedding_model).encode([x["text"] for x in chunks]), dtype="float32")
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index, settings.vector_index_path)
    Path(settings.metadata_path).write_text(json.dumps(chunks, indent=2), encoding="utf-8")
    print(f"Indexed {len(chunks)} chunks.")

if __name__ == "__main__":
    main()
