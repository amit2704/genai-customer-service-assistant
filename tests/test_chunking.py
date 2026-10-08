from app.rag.chunking import split_text

def test_split_text_returns_chunks():
    chunks = split_text("A" * 2000, chunk_size=500, chunk_overlap=50)
    assert len(chunks) > 1
    assert all(chunks)
