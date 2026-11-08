
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk
from app.services.embedding_service import generate_embeddings


def search_similar_chunks(
    db: Session,
    query: str,
    top_k: int = 5
):
    # 1. Kullanıcının sorusunun embedding vektörünü oluştur
    query_embedding = generate_embeddings([query])[0]

    # 2. Cosine distance hesaplamasını hazırla
    distance = DocumentChunk.embedding.cosine_distance(
        query_embedding
    )

    # 3. En yakın chunk kayıtlarını sorgula
    statement = (
        select(
            DocumentChunk.id,
            DocumentChunk.document_id,
            DocumentChunk.chunk_index,
            DocumentChunk.content,
            Document.filename,
            distance.label("distance")
        )
        .join(
            Document,
            Document.id == DocumentChunk.document_id
        )
        .order_by(distance)
        .limit(top_k)
    )

    # 4. Sorguyu veritabanında çalıştır
    results = db.execute(statement).all()

    # 5. Sonuçları düzenle
    retrieved_chunks = []

    for result in results:
        retrieved_chunks.append({
            "chunk_id": result.id,
            "document_id": result.document_id,
            "chunk_index": result.chunk_index,
            "filename": result.filename,
            "content": result.content,
            "distance": float(result.distance),
            "similarity": 1 - float(result.distance)
        })

    return retrieved_chunks
