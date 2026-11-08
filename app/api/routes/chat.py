
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.retrieval_service import search_similar_chunks
from app.services.llm_service import generate_answer


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


# Kullanıcıdan alınacak soru
class ChatRequest(BaseModel):

    question: str

    top_k: int = Field(default=5, ge=1, le=20)


@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    # Soru kontrolü
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        # 1. Soruyla ilgili metin parçalarını bul
        retrieved_chunks = search_similar_chunks(
            db=db,
            query=request.question,
            top_k=request.top_k
        )

        # 2. Minimum benzerlik eşiğini belirle
        MIN_SIMILARITY = 0.30

        # 3. Yeterince benzer olmayan sonuçları ele
        retrieved_chunks = [
            chunk
            for chunk in retrieved_chunks
            if chunk["similarity"] >= MIN_SIMILARITY
        ]

        # 4. Bulunan metinleri Claude'a gönder
        result = generate_answer(
            question=request.question,
            retrieved_chunks=retrieved_chunks
        )

        # 5. Cevabı ve kaynakları kullanıcıya döndür
        return {
            "question": request.question,
            "answer": result["answer"],
            "total_sources": len(result["sources"]),
            "sources": result["sources"]
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(error)}"
        )
