
from app.db.database import SessionLocal
from app.services.retrieval_service import search_similar_chunks


# Veritabanı oturumu oluştur
db = SessionLocal()

try:
    # Test sorusu
    question = "What is Machine Learning?"

    # En benzer metin parçalarını getir
    results = search_similar_chunks(
        db=db,
        query=question,
        top_k=5
    )

    print("\nQuestion:", question)
    print("\nRetrieved Results:\n")

    for result in results:
        print("Document:", result["filename"])
        print("Chunk ID:", result["chunk_id"])
        print("Similarity:", round(result["similarity"], 4))
        print("Content:", result["content"])
        print("-" * 50)

finally:
    # Veritabanı oturumunu kapat
    db.close()
