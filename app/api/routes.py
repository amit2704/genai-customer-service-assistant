from fastapi import APIRouter, HTTPException

from app.rag.service import RAGService
from app.schemas import ChatRequest, ChatResponse

router = APIRouter()
rag_service = RAGService()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer, sources = rag_service.answer(request.question, request.top_k)
        return {"answer": answer, "sources": sources}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to process request") from exc
