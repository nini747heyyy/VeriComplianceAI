# Architecture Document: VeriCompliance AI Engine

## 1. Executive Overview

VeriCompliance AI is a compliance and governance engine designed to enforce strict regulatory adherence across corporate policies, frameworks (e.g., SOC 2, ISO 27001), and legislative standards (e.g., EU AI Act).

The platform combines vector-based retrieval with role-based authorization to generate precise, cited compliance and audit responses.

The system is designed around a grounded-response approach: responses should be based on retrieved evidence from the provided compliance sources, with citations identifying the supporting document and page/excerpt.

---

## 2. System Goals

The system is designed to:

* Allow authorized users to submit compliance-related queries.
* Retrieve relevant information from compliance and governance documents.
* Generate structured compliance responses using an AI model.
* Ground generated responses in retrieved evidence.
* Provide citations for generated claims.
* Maintain an auditable record of compliance queries and responses.
* Enforce role-based access to the application.
* Handle unsupported or insufficiently grounded queries safely.
* Provide a reproducible and testable application lifecycle.

---

## 3. Technology Stack

| Layer              | Technology                                    | Key Dependencies / Usage                            |
| :----------------- | :-------------------------------------------- | :-------------------------------------------------- |
| **Frontend**       | Next.js 14 (App Router), React 18, TypeScript | Tailwind CSS, Lucide React, Framer Motion, Recharts |
| **Backend**        | Python 3.11, FastAPI                          | Uvicorn, Pydantic v2, PyJWT, Passlib (Bcrypt)       |
| **AI / RAG**       | OpenAI API, ChromaDB                          | `gpt-4o`, `text-embedding-3-small`, LangChain       |
| **Database**       | PostgreSQL / SQLite                           | Audit logs and identity management                  |
| **Infrastructure** | Docker, Docker Compose, Nginx                 | Containerization and reverse proxy                  |
| **Testing**        | Playwright / [confirm actual test framework]  | End-to-end application verification                 |
| **CI/CD**          | GitHub Actions                                | Automated build, test, and verification pipeline    |

---

## 4. High-Level Architecture

The system follows a layered architecture consisting of the frontend, backend API, AI/RAG processing layer, relational database, and vector retrieval layer.

```text
                         ┌──────────────────┐
                         │       USER       │
                         └────────┬─────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │      Next.js Frontend   │
                    │                         │
                    │ Query Interface         │
                    │ Authentication UI       │
                    │ Results & Citations     │
                    └────────────┬────────────┘
                                 │
                           HTTP / REST API
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      FastAPI Backend    │
                    │                         │
                    │ Authentication          │
                    │ Authorization           │
                    │ Query Processing        │
                    │ Audit Logging            │
                    └────────────┬────────────┘
                                 │
                  ┌──────────────┼──────────────┐
                  │              │              │
                  ▼              ▼              ▼
          ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
          │ PostgreSQL / │ │   ChromaDB   │ │  OpenAI API  │
          │    SQLite   │ │ Vector Store │ │     / LLM    │
          └──────────────┘ └──────┬───────┘ └──────┬───────┘
                                  │                │
                                  └───────┬────────┘
                                          ▼
                               ┌────────────────────┐
                               │   RAG Processing   │
                               └─────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │ Grounded Compliance │
                              │      Response       │
                              └──────────┬──────────┘
                                         │
                                         ▼
                                Next.js Frontend
```

### Architecture Flow

1. The user submits a compliance query through the frontend.
2. The frontend sends the request to the FastAPI backend.
3. The backend authenticates and authorizes the request.
4. The query is processed by the retrieval/AI layer.
5. ChromaDB is used to retrieve relevant document information.
6. The retrieved evidence is supplied to the LLM for response generation.
7. The response is associated with supporting citations.
8. The query and generated response are recorded for auditing.
9. The final grounded response and citations are returned to the frontend.

---

## 5. Component Architecture

### 5.1 Frontend

The frontend is implemented using Next.js, React, and TypeScript.

Primary responsibilities include:

* User authentication interface.
* Compliance query submission.
* Display of generated compliance responses.
* Display of supporting citations.
* Visualization of compliance/audit information.
* Display of validation and error states.

```text
Frontend
│
├── Authentication
│
├── Compliance Query Interface
│
├── Response Viewer
│   ├── Answer
│   ├── Grounding Information
│   └── Citations
│
├── Audit / Compliance Dashboard
│
└── Error & Validation UI
```

### 5.2 Backend

The backend is implemented using Python and FastAPI.

Primary responsibilities include:

* API request handling.
* Authentication and authorization.
* Query processing.
* AI/RAG orchestration.
* Database interaction.
* Audit logging.
* Error handling.

```text
Backend
│
├── API Routes
│
├── Authentication Service
│
├── Authorization / Role Management
│
├── Compliance Query Service
│
├── RAG / AI Service
│   ├── Retrieval
│   ├── Evidence Processing
│   ├── LLM Generation
│   └── Citation Generation
│
└── Audit Logging Service
```

---

## 6. AI / RAG Architecture

The AI layer uses retrieval-augmented generation to ground compliance responses in available source material.

```text
User Query
     │
     ▼
Input Validation
     │
     ▼
Query Processing
     │
     ▼
Semantic Retrieval
     │
     ▼
ChromaDB
     │
     ▼
Relevant Evidence
     │
     ▼
LLM / OpenAI API
     │
     ▼
Generated Compliance Response
     │
     ▼
Citation Association
     │
     ▼
Final Response
```

### RAG Responsibilities

The RAG layer is responsible for:

* Converting queries into a form suitable for retrieval.
* Retrieving relevant compliance information.
* Providing retrieved context to the language model.
* Generating responses based on the available evidence.
* Associating responses with supporting citations.

The application should not treat unsupported model-generated information as verified compliance evidence.

---

## 7. Data Model

The relational database stores identity information, compliance query records, and citation information.

### Users

```sql
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'auditor',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Compliance Query Logs

```sql
CREATE TABLE IF NOT EXISTS compliance_queries (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id),
    query_text TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    grounding_score FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Citations

```sql
CREATE TABLE IF NOT EXISTS citations (
    id VARCHAR(36) PRIMARY KEY,
    query_id VARCHAR(36) REFERENCES compliance_queries(id),
    document_title VARCHAR(255) NOT NULL,
    page_number VARCHAR(50) NOT NULL,
    excerpt TEXT NOT NULL
);
```

### Entity Relationships

```text
User
 │
 │ 1:N
 ▼
Compliance Query
 │
 │ 1:N
 ▼
Citation
```

A user may create multiple compliance queries. Each query may contain multiple supporting citations.

---

## 8. API Architecture

The backend exposes REST APIs through FastAPI.

The final endpoint list should match the implemented application.

Example structure:

```text
Authentication
├── POST /api/auth/login
└── POST /api/auth/register

Compliance
├── POST /api/query
└── GET  /api/query/{id}

Documents
├── POST /api/documents/upload
├── GET  /api/documents
└── DELETE /api/documents/{id}

System
└── GET /api/health
```

> **Implementation check:** Update this section so that every endpoint listed here actually exists in the final backend.

For each API endpoint, document:

* HTTP method
* Endpoint
* Purpose
* Required authentication
* Input
* Output
* Error responses

---

## 9. Authentication and Authorization

The system uses role-based authorization to control access to compliance functionality.

Authentication is handled using JWT-based authentication, with password hashing using Bcrypt.

```text
User
 │
 ▼
Authentication
 │
 ▼
JWT Token
 │
 ▼
Authorization Middleware
 │
 ▼
Role Validation
 │
 ├── Authorized → API operation
 │
 └── Unauthorized → Reject request
```

The user's role is stored in the `users` table and is used to determine access to protected functionality.

> **Implementation check:** Document the exact roles and permissions implemented by the application rather than listing roles that do not exist.

---

## 10. Citation and Grounding System

Citation generation is a core part of the Track C architecture.

Each generated compliance response should be associated with supporting source information.

A citation contains:

* Document title
* Page number
* Supporting excerpt
* Associated compliance query

```text
Compliance Query
       │
       ▼
Relevant Evidence
       │
       ▼
LLM Response
       │
       ▼
Citation Association
       │
       ▼
Response + Evidence
```

The frontend should display the supporting citations alongside the generated answer so that users can verify the source of the response.

---

## 11. Error and Failure Handling

The system should explicitly handle failure conditions rather than returning unsupported answers.

### Invalid Query

The backend validates incoming requests before processing.

### No Relevant Evidence

If retrieval does not produce sufficient relevant evidence, the system should return an appropriate "insufficient evidence" response rather than presenting an unsupported compliance claim.

### AI Service Failure

If the OpenAI service is unavailable or returns an error, the backend should return a controlled error response without exposing internal credentials or implementation details.

### Database Failure

Database errors should be handled by the backend and returned as controlled API errors.

### Invalid Input / Document

Invalid or unsupported input should be rejected before entering the AI processing pipeline.

---

## 12. Security

Security controls include:

* JWT-based authentication.
* Password hashing using Bcrypt.
* Role-based authorization.
* Input validation through Pydantic.
* API key storage through environment variables.
* `.env` files excluded from version control.
* Controlled database access.
* Validation of uploaded/input data.

No API keys, passwords, or other secrets should be committed to the public repository.

---

## 13. Testing Architecture

The testing strategy should verify both individual functionality and the complete application workflow.

```text
Source Code
     │
     ▼
Unit / Component Tests
     │
     ▼
API / Integration Tests
     │
     ▼
Playwright E2E Tests
     │
     ▼
GitHub Actions
     │
     ▼
Passing CI Pipeline
```

Important end-to-end scenarios should include:

* User authentication.
* Compliance query submission.
* Successful response generation.
* Citation display.
* Handling of unsupported queries.
* Invalid input handling.
* API failure handling.

> **Implementation check:** Keep only the test types and commands that actually exist in the repository.

---

## 14. CI/CD Architecture

The project uses GitHub Actions to automatically verify the application.

```text
Git Push / Pull Request
          │
          ▼
     GitHub Actions
          │
          ▼
 Install Dependencies
          │
          ▼
      Lint / Checks
          │
          ▼
        Build
          │
          ▼
        Tests
          │
          ▼
   Playwright E2E Tests
          │
          ▼
     Pipeline Result
       │         │
       ▼         ▼
     PASS       FAIL
```

The most recent GitHub Actions workflow must pass before submission.

---

## 15. Deployment and Execution

The application is containerized using Docker and Docker Compose, with Nginx used as a reverse proxy where applicable.

#### Backend Core
DATABASE_URL=postgresql://user:pass@localhost:5432/vericompliance
JWT_SECRET=your-super-secret-jwt-key
JWT_ALGORITHM=HS256

#### AI Engine
OPENAI_API_KEY=sk-proj-...
CHROMA_PERSIST_DIR=./chroma_db

#### Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

### Local Execution

The final README should provide the exact commands required to:

1. Clone the repository.
2. Install or start required services.
3. Configure environment variables.
4. Start the backend.
5. Start the frontend.
6. Verify the application.

### Environment Variables

Example:

```text
OPENAI_API_KEY=
DATABASE_URL=
JWT_SECRET=
```

> **Implementation check:** Replace this list with the exact environment variables used by the application. Never commit actual secret values.

---

## 16. Design Decisions and Trade-offs

### Vector Retrieval

ChromaDB is used for semantic retrieval of compliance information. This supports retrieval based on meaning rather than relying only on exact keyword matching.

### Relational Database

PostgreSQL / SQLite is used for structured identity and audit information.

### FastAPI Backend

FastAPI provides a clear API boundary between the frontend and AI/data-processing components.

### RAG Architecture

Retrieval-augmented generation is used to provide the language model with relevant source context before generating a response.

### Citation-Based Verification

Responses are associated with document and page-level citation information to improve traceability.

### Role-Based Authorization

Role-based access provides a controlled mechanism for restricting compliance functionality.

---

## 17. Scalability and Future Improvements

Potential future improvements include:

* Support for additional compliance frameworks.
* Additional document formats.
* Improved document ingestion and OCR.
* More advanced retrieval and reranking.
* Additional LLM providers.
* Multi-user organization management.
* Improved audit dashboards.
* Horizontal backend scaling.
* Retrieval and response caching.

---

## 18. Summary

VeriCompliance AI uses a layered architecture combining a Next.js frontend, FastAPI backend, relational database, vector retrieval system, and LLM-based reasoning layer.

The architecture emphasizes:

* Grounded compliance responses.
* Evidence and citation traceability.
* Role-based authorization.
* Auditable query history.
* Controlled AI processing.
* Automated testing and CI/CD.
* Reproducible application execution.

The architecture is designed to support the Track C requirement for reliable, verifiable outputs from unstructured compliance and governance information.