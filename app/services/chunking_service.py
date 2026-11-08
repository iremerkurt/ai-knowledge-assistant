
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> list:

    if not text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(text)

    results = []

    for index, chunk in enumerate(chunks):
        results.append({
            "chunk_index": index,
            "content": chunk
        })

    return results
