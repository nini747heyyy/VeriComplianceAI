# VeriCompliance AI – Knowledge & Compliance Agent Platform

VeriCompliance AI is an enterprise-grade platform engineered to eliminate artificial intelligence hallucinations in high-stakes legal, regulatory, and corporate compliance operations.

## Key Features

1. **Grounded RAG Pipeline**: Structured citations including exact Page, Line, and Paragraph metadata.
2. **Deterministic Refusal Protocol**: Refuses to output responses if semantic search confidence drops below threshold.
3. **Compliance Audit Engine**: Evaluates unstructured documents against customizable or template-based compliance matrices.
4. **Hardened Security**: Enterprise-level RBAC, Multi-Tenant isolation, JWT with Argon2, and encrypted vector storage.

## Architecture

* **Frontend**: Next.js 15 (App Router), React 19, Tailwind CSS, Lucide Icons, Zustand.
* **Backend**: FastAPI, SQLAlchemy, Pydantic, Celery, Redis.
* **Vector Database**: ChromaDB (Default) with Pinecone & FAISS support.
* **AI Core**: LangChain, LangGraph, OpenAI GPT-4o.

## Quick Start (Docker Orchestration)

1. Clone the repository and navigate to root:
   ```bash
   git clone [https://github.com/vericompliance/vericompliance-ai.git](https://github.com/vericompliance/vericompliance-ai.git)
   cd vericompliance-ai