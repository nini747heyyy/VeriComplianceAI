from fastapi import FastAPI, Depends, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Assuming these are your internal modules
from app.security.rbac import PermissionChecker, get_current_user_claims
from app.rag.pipeline import VerifiedRAGPipeline, GroundedRAGResponse

app = FastAPI(
    title="VeriCompliance AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vericompliance.ai", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize globally or attach to app.state
rag_engine = VerifiedRAGPipeline(vector_db_dir="./chroma_data")

def get_rag_engine() -> VerifiedRAGPipeline:
    """Dependency injection for the RAG pipeline."""
    return rag_engine

class ChatQueryRequest(BaseModel):
    question: str

@app.get("/api/health", tags=["System"])
def health_check():
    return {"status": "healthy", "engine": "VeriCompliance AI", "version": "1.0.0"}

@app.post("/api/chat", response_model=GroundedRAGResponse, tags=["RAG Agent"])
async def chat_endpoint(
    request: ChatQueryRequest,
    claims: dict = Depends(get_current_user_claims), # Fix: Injected claims
    engine: VerifiedRAGPipeline = Depends(get_rag_engine) # Fix: Injected engine
):
    org_id = claims.get("org_id")
    response = engine.query(question=request.question, organization_id=org_id)
    return response

@app.post("/api/documents/upload", tags=["Ingestion"])
async def upload_document(
    file: UploadFile = File(...),
    claims: dict = Depends(PermissionChecker("docs:write"))
):
    allowed_types = ["pdf", "docx", "pptx", "txt", "csv"]
    ext = file.filename.split(".")[-1].lower()
    
    if ext not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
    
    # Secure storage logic & async task dispatch to Celery
    return {
        "filename": file.filename,
        "status": "queued",
        "message": "Document accepted for parsing, OCR, and embedding generation."
    }