from fastapi import FastAPI, Depends, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from app.security.rbac import PermissionChecker, get_current_user_claims
from app.rag.pipeline import VerifiedRAGPipeline, GroundedRAGResponse

app = FastAPI(
    title="VeriCompliance AI Core Engine",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vericompliance.ai", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_engine = VerifiedRAGPipeline(vector_db_dir="./chroma_data")

class ChatQueryRequest(BaseModel):
    query: str

@app.get("/api/health", tags=["System"])
def health_check():
    return {"status": "healthy", "engine": "VeriCompliance AI", "version": "1.0.0"}

@app.post("/api/chat", response_model=GroundedRAGResponse, tags=["RAG Agent"])
def execute_grounded_chat(
    payload: ChatQueryRequest,
    claims: dict = Depends(PermissionChecker("docs:read"))
):
    org_id = claims.get("org_id")
    response = rag_engine.query(question=payload.query, organization_id=org_id)
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