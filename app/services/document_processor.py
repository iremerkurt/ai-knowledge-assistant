
from io import BytesIO

from pypdf import PdfReader
from docx import Document


def extract_text(filename: str, content: bytes) -> dict:

    extension = filename.lower().split(".")[-1]

    # TXT dosyası
    if extension == "txt":
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = content.decode("cp1254", errors="replace")

        return {
            "text": text,
            "page_count": None
        }

    # PDF dosyası
    elif extension == "pdf":
        pdf = PdfReader(BytesIO(content))

        pages = []
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            pages.append(page_text)

        return {
            "text": "\n".join(pages),
            "page_count": len(pdf.pages)
        }

    # DOCX dosyası
    elif extension == "docx":
        document = Document(BytesIO(content))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return {
            "text": "\n".join(paragraphs),
            "page_count": None
        }

    else:
        raise ValueError("Unsupported file format.")
