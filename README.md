# AI Knowledge Assistant

An AI-powered document question-answering system built with Retrieval-Augmented Generation (RAG). The application allows users to upload documents and ask natural language questions about their content.

The system extracts document text, splits it into chunks, generates vector embeddings, stores them in PostgreSQL with pgvector, and retrieves relevant information to generate context-aware answers using Claude API.

## Features

- **Document Upload:** Supports PDF, DOCX, and TXT files.
- **Text Extraction:** Extracts text from uploaded documents.
- **Text Chunking:** Splits documents into smaller chunks with overlapping content.
- **Vector Embeddings:** Generates multilingual embeddings using Sentence Transformers.
- **Vector Database:** Stores document chunks and embeddings in PostgreSQL with pgvector.
- **Semantic Search:** Retrieves relevant document chunks using cosine similarity.
- **AI-Powered Answers:** Uses Claude API to generate answers based on retrieved document context.
- **Source Attribution:** Returns document names and source references with generated answers.
- **Relevance Filtering:** Filters retrieved results using a configurable similarity threshold.

## Architecture

```text
                User
                  |
                  v
             FastAPI
                  |
          +-------+-------+
          |               |
          v               v
    Document Upload    Chat API
          |               |
          v               v
    Text Extraction   Query Embedding
          |               |
          v               v
      Chunking        Semantic Search
          |               |
          v               v
     Embeddings       PostgreSQL
          |            + pgvector
          v               |
     PostgreSQL           v
      + pgvector     Relevant Chunks
                          |
                          v
                      Claude API
                          |
                          v
                   Generated Answer
                    + Sources
```

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Database | PostgreSQL |
| Vector Database Extension | pgvector |
| ORM | SQLAlchemy |
| Embedding Model | Sentence Transformers |
| LLM | Claude API |
| Document Processing | pypdf, python-docx |
| Text Splitting | LangChain Text Splitters |
| Containerization | Docker, Docker Compose |
| API Documentation | Swagger UI |

## Project Structure

```text
ai-knowledge-assistant/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── chat.py
│   │       └── documents.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── services/
│   │   ├── chunking_service.py
│   │   ├── document_processor.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   └── retrieval_service.py
│   │
│   └── main.py
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── sample_document.pdf
├── sample_document.txt
├── create_sample_pdf.py
│
├── test_claude.py
├── test_db.py
├── test_embedding.py
└── test_retrieval.py
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/iremerkurt/ai-knowledge-assistant.git

cd ai-knowledge-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory using `.env.example` as a template.

```env
POSTGRES_DB=ai_knowledge
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432

ANTHROPIC_API_KEY=your_anthropic_api_key
```

Add your own PostgreSQL credentials and Anthropic API key.

### 5. Start PostgreSQL with pgvector

Make sure Docker Desktop is running.

```bash
docker compose up -d
```

### 6. Enable pgvector

```bash
docker exec -it ai_knowledge_db psql -U postgres -d ai_knowledge
```

Execute the following SQL command:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 7. Create Database Tables

```bash
python test_db.py
```

### 8. Start the FastAPI Application

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

## API Documentation

Interactive API documentation is available through Swagger UI:

http://127.0.0.1:8000/docs

### Document Upload

**Endpoint:** `POST /documents/upload`

Supported file formats:
- PDF
- DOCX
- TXT

### Ask Questions

**Endpoint:** `POST /chat/`

Example request:

```json
{
  "question": "What are the main categories of Machine Learning?",
  "top_k": 5
}
```

The response contains:
- Generated answer
- Number of retrieved sources
- Source document names
- Document and chunk identifiers
- Similarity scores

## Current Project Status

The current implementation provides a working RAG-based document question-answering system.

Implemented:
- Document ingestion and text extraction
- Chunking and embedding generation
- PostgreSQL vector storage
- Semantic retrieval
- Claude API integration
- Context-grounded answer generation
- Source attribution
- Basic relevance filtering
- Dockerized PostgreSQL database

Planned Improvements:
- Automated testing with Pytest
- Agentic RAG architecture using LangGraph
- Tool-based agent workflows
- Advanced retrieval strategies
- RAG evaluation with RAGAS
- FastAPI containerization
- CI/CD with GitHub Actions
- Improved error handling and production readiness

## Future Development

The long-term goal is to evolve this project into an Agentic RAG system capable of making retrieval decisions, selecting tools, and executing multi-step workflows.

## Author

**İrem Erkurt**

Computer Engineering Graduate | AI & Machine Learning

[GitHub](https://github.com/iremerkurt)

---

*This project is being actively developed as an AI Engineering portfolio project.*