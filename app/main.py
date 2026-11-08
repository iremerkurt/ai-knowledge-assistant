
from fastapi import FastAPI
from app.api.routes import documents, chat

app = FastAPI(
    title="AI Knowledge Assistant",
    description="An AI-powered document question answering system using RAG.",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Knowledge Assistant!",
        "status": "running"
    }

# Document API bağlantısı
app.include_router(documents.router)
app.include_router(chat.router)
