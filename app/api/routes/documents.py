
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Document, DocumentChunk

from app.services.document_processor import extract_text
from app.services.chunking_service import split_text
from app.services.embedding_service import generate_embeddings


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    allowed_extensions = [".pdf", ".docx", ".txt"]

    filename = file.filename or ""

    extension = (
        "." + filename.split(".")[-1].lower()
        if "." in filename
        else ""
    )

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are supported."
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    try:
        # 1. Dosyadan metin çıkar
        result = extract_text(filename, content)
        extracted_text = result["text"]

        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the document."
            )

        # 2. Metni chunk'lara böl
        chunks = split_text(extracted_text)

        # 3. Embedding oluştur
        chunk_texts = [
            chunk["content"]
            for chunk in chunks
        ]

        embeddings = generate_embeddings(chunk_texts)

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Could not process document: {str(error)}"
        )

    try:
        # 4. Belge bilgilerini veritabanına kaydet
        document = Document(
            filename=filename,
            file_type=extension,
            file_size=len(content),
            character_count=len(extracted_text),
            page_count=result["page_count"]
        )

        db.add(document)

        # Belge ID'sini oluştur
        db.flush()

        # 5. Chunk ve embedding kayıtlarını hazırla
        chunk_records = []

        for chunk, embedding in zip(chunks, embeddings):

            chunk_record = DocumentChunk(
                document_id=document.id,
                chunk_index=chunk["chunk_index"],
                content=chunk["content"],
                embedding=embedding
            )

            chunk_records.append(chunk_record)

        # 6. Chunk kayıtlarını veritabanına ekle
        db.add_all(chunk_records)

        # İşlemleri kalıcı olarak kaydet
        db.commit()

        db.refresh(document)

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Could not save document to database: {str(error)}"
        )

    return {
        "message": "Document successfully processed and saved to database!",
        "document_id": document.id,
        "filename": document.filename,
        "file_type": document.file_type,
        "file_size": document.file_size,
        "character_count": document.character_count,
        "page_count": document.page_count,
        "total_chunks": len(chunks),
        "total_embeddings": len(embeddings),
        "embedding_dimension": len(embeddings[0]) if embeddings else None,
        "status": "success"
    }
