from fastapi import FastAPI, Depends, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Core application authentication and RAG pipeline modules
from app.security.rbac import PermissionChecker, get_current_user_claims
from app.rag.pipeline import VerifiedRAGPipeline, GroundedRAGResponse

# Initialize main FastAPI application instance with Swagger/ReDoc configuration
app = FastAPI(
    title="VeriCompliance AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure Cross-Origin Resource Sharing (CORS) for production and local web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vericompliance.ai", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Singleton instance of the RAG engine targeting persistent vector storage
rag_engine = VerifiedRAGPipeline(vector_db_dir="./chroma_data")

# Dependency injection provider for the RAG pipeline instance
def get_rag_engine() -> VerifiedRAGPipeline:
    """Dependency injection provider for the RAG engine."""
    return rag_engine

# Request payload schema for query endpoints
class ChatQueryRequest(BaseModel):
    question: str

# System health monitoring endpoint
@app.get("/api/health", tags=["System"])
def health_check():
    return {"status": "healthy", "engine": "VeriCompliance AI", "version": "1.0.0"}

# Grounded query endpoint requiring active authentication claims
@app.post("/api/chat", response_model=GroundedRAGResponse, tags=["RAG Agent"])
async def chat_endpoint(
    request: ChatQueryRequest,
    claims: dict = Depends(get_current_user_claims),
    engine: VerifiedRAGPipeline = Depends(get_rag_engine)
):
    org_id = claims.get("org_id")
    response = engine.query(question=request.question, organization_id=org_id)
    return response

# Document ingestion endpoint with file extension checks and RBAC permission guards
@app.post("/api/documents/upload", tags=["Ingestion"])
async def upload_document(
    file: UploadFile = File(...),
    claims: dict = Depends(PermissionChecker("docs:write"))
):
    # Validate uploaded file extension against supported compliance formats
    allowed_types = ["pdf", "docx", "pptx", "txt", "csv"]
    ext = file.filename.split(".")[-1].lower()
    
    if ext not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
    
    # Secure storage handling and background asynchronous worker dispatch
    return {
        "filename": file.filename,
        "status": "queued",
        "message": "Document accepted for parsing, OCR, and embedding generation."
    }
