from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text: str, chunk_size: int = 700, chunk_overlap: int = 100) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return [x.strip() for x in splitter.split_text(text) if x.strip()]
