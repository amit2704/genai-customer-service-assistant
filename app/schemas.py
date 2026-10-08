from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=4, ge=1, le=10)

class Source(BaseModel):
    source: str
    chunk_id: int
    score: float

class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
