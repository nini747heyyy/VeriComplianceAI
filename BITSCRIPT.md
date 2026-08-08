# VeriComplianceAI — BITScript

## 1. Project Identity

**Project:** VeriCompliance AI  
**Repository:** `nini747heyyy/VeriComplianceAI`  
**Purpose:** Grounded knowledge and compliance assistant for high-stakes legal, regulatory, and corporate compliance workflows.

VeriCompliance AI is designed around a core principle: an AI system should not invent an answer when the supplied evidence does not support it. The platform combines retrieval-augmented generation (RAG), document grounding, deterministic refusal, compliance auditing, structured citations, and security controls.

The repository currently contains separate `backend`, `frontend`, and `docs` areas, together with root-level agent/constitution files and Docker configuration.

---

## 2. Core Problem

Organizations work with large collections of policies, contracts, compliance manuals, regulatory documents, and meeting transcripts. These documents are often unstructured and difficult to search.

A conventional LLM can produce fluent but unsupported answers. In compliance and other high-stakes domains, this creates unacceptable risk.

The system therefore aims to:

1. Retrieve relevant evidence from supplied documents.
2. Generate answers grounded in that evidence.
3. Attach traceable citations to responses.
4. Refuse or flag answers when evidence is insufficient.
5. Audit documents against compliance requirements.
6. Extract actionable information from meeting transcripts.
7. Preserve tenant and user security.

---

## 3. Product Principles

### 3.1 Zero-Hallucination-by-Design

The assistant must never treat general model knowledge as authoritative evidence for a document-grounded answer.

If the retrieved context does not support an answer, the system should refuse, qualify, or flag the response rather than guess.

### 3.2 Evidence First

Every material compliance claim should be traceable to its originating document.

Citation metadata should be as granular as the available source permits, including:

- Document ID
- Document title
- Page number
- Section/paragraph
- Exact supporting snippet
- Relevance/confidence score

### 3.3 Deterministic Refusal

The repository constitution specifies an 85% grounding-confidence threshold. Retrieval/generation logic should therefore expose confidence and apply a deterministic refusal or warning path when the threshold is not satisfied.

Do not silently lower the threshold to make an answer appear complete.

### 3.4 Security by Default

Passwords must never be stored in plaintext. Authentication and authorization should use secure password hashing and token/session controls.

The intended architecture includes:

- RBAC
- Multi-tenant isolation
- JWT-based authentication
- Argon2/Bcrypt password hashing
- Protected document access
- Encrypted vector/document storage where supported

---

## 4. Repository Structure

```text
VeriComplianceAI/
├── backend/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── types/
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.js
│   └── tailwind.config.js
│
├── docs/
│   └── ARCHITECHTURE.md
│
├── agents.md
├── constitution.md
├── docker-compose.yml
├── nginx.conf
├── package.json
├── package-lock.json
└── README.md
```

> The structure above reflects the repository tree currently exposed by GitHub. Individual files inside `backend/app` and `frontend/app` may evolve as development continues.

---

## 5. Backend Responsibilities

The backend is the system's trusted processing layer.

It should be responsible for:

- Authentication and authorization
- Document ingestion
- Document parsing
- Text extraction
- Chunking
- Embedding generation
- Vector retrieval
- RAG orchestration
- Citation construction
- Confidence calculation
- Deterministic refusal
- Compliance auditing
- Summarization
- Meeting/action-item extraction
- Tenant isolation
- API validation and error handling

### Backend rules

1. Never return fabricated citations.
2. Never create a citation for a passage that was not retrieved.
3. Preserve document/page metadata through the entire retrieval pipeline.
4. Validate uploaded files before processing.
5. Enforce authorization at the API/service layer, not only in the UI.
6. Never expose secrets through API responses or logs.
7. Keep business logic separate from route/controller logic where practical.
8. Return predictable structured errors.

---

## 6. Frontend Responsibilities

The frontend provides the user-facing compliance workspace.

Primary capabilities should include:

- Authentication
- Dashboard
- Document upload
- Document/library management
- Grounded Q&A
- Citation inspection
- Document summarization
- Compliance audit results
- Action-item extraction
- Confidence/refusal indicators
- Tenant/user-aware navigation

### Frontend rules

1. Do not present unsupported AI output as verified fact.
2. Display citations close to the claims they support.
3. Clearly distinguish verified answers from refusal/low-confidence responses.
4. Keep API types synchronized with backend response schemas.
5. Do not put API secrets in client-side code.
6. Handle loading, empty, error, and refusal states explicitly.
7. Keep compliance-critical information visually prominent.

---

## 7. RAG Pipeline

The expected grounded-answer flow is:

```text
User Question
     │
     ▼
Request Validation
     │
     ▼
Tenant/User Authorization
     │
     ▼
Query Processing
     │
     ▼
Semantic Retrieval
     │
     ▼
Top Relevant Chunks
     │
     ├──► Confidence / Relevance Evaluation
     │
     ▼
Grounding Threshold Check
     │
     ├── Below threshold ──► Deterministic Refusal / Flag
     │
     ▼
Context Assembly
     │
     ▼
LLM Generation
     │
     ▼
Citation Validation
     │
     ▼
Structured Response
```

### Retrieval requirements

Each retrieved chunk should retain enough metadata to reconstruct its source:

```text
documentId
documentTitle
pageNumber
section/paragraph
exactSnippet
relevanceScore
```

Retrieval must be tenant-aware. A user from Tenant A must never receive chunks belonging to Tenant B.

---

## 8. Citation Contract

A citation should conceptually follow this structure:

```typescript
interface Citation {
  id: string;
  documentId: string;
  documentTitle: string;
  pageNumber: number;
  exactSnippet: string;
  relevanceScore: number;
}
```

If additional source granularity exists, it may be extended with fields such as:

```text
section
paragraph
lineNumber
chunkId
sourceType
```

### Citation validation

Before returning an answer:

1. Confirm that each citation refers to a real document.
2. Confirm that the referenced chunk exists.
3. Confirm that the snippet belongs to that chunk.
4. Confirm that the citation was retrieved for the current query.
5. Reject or remove unsupported citations.
6. Do not manufacture page numbers or snippets.

---

## 9. Deterministic Refusal Protocol

The refusal layer is a critical safety mechanism.

### Minimum behavior

```text
IF grounding_confidence >= 0.85
    continue to grounded generation
ELSE
    do not guess
    return a refusal/insufficient-evidence response
```

A low-confidence response should communicate that the supplied documents do not provide sufficient evidence.

The system should not bypass the threshold because a user asks the question repeatedly.

---

## 10. Compliance Audit Engine

The compliance engine evaluates a document or organizational policy against a compliance matrix.

Conceptual flow:

```text
Document
   │
   ▼
Text Extraction
   │
   ▼
Relevant Requirement Retrieval
   │
   ▼
Requirement-by-Requirement Evaluation
   │
   ├── PASS
   ├── FAIL
   └── INSUFFICIENT EVIDENCE
   │
   ▼
Evidence + Citation
   │
   ▼
Audit Report
```

A compliance result should contain:

- Requirement ID/name
- Evaluation status
- Explanation
- Evidence
- Source citation
- Confidence
- Recommended action where applicable

The system should avoid converting "no evidence found" into "requirement failed" unless the compliance rule explicitly defines that behavior.

---

## 11. Grounded Compliance Auditor Agent

The repository already defines a **Grounded Compliance Auditor** agent.

Its role is to verify corporate actions and policies against regulatory texts such as:

- EU AI Act
- SOC 2
- ISO 27001

The agent is expected to produce structured JSON containing citation payloads.

### Agent behavior

The agent must:

1. Read only authorized/retrieved evidence.
2. Identify applicable requirements.
3. Compare evidence against the requirement.
4. Produce a structured result.
5. Attach citations.
6. Flag insufficient evidence.
7. Never invent regulatory text.

---

## 12. System Constitution

The repository's constitution establishes three important constraints:

### Zero Hallucination Guarantee

Answers must be supported by source material.

### Strict Verification

Grounding confidence below 85% must be flagged.

### Data Protection

Plaintext passwords are prohibited; secure password hashing must be used.

These principles take priority over convenience or answer completeness.

---

## 13. API Design Principles

APIs should be organized around clear resources and actions.

Suggested conceptual groups:

```text
/auth
/users
/tenants
/documents
/documents/{id}
/documents/{id}/summary
/query
/citations
/audits
/audits/{id}
/actions
```

Actual endpoint names should follow the existing backend implementation rather than introducing duplicate routes.

### API response principles

Successful responses should be predictable and typed.

Errors should include:

```json
{
  "error": {
    "code": "INSUFFICIENT_GROUNDING",
    "message": "The supplied documents do not contain enough evidence to answer this question."
  }
}
```

Never expose stack traces, credentials, tokens, internal filesystem paths, or provider secrets to clients.

---

## 14. Authentication and Authorization

The platform should enforce:

```text
Authentication
      │
      ▼
JWT / Session Validation
      │
      ▼
User Identity
      │
      ▼
Tenant Resolution
      │
      ▼
RBAC Permission Check
      │
      ▼
Resource Access
```

Every document/query/audit operation must be evaluated against the authenticated user's permissions and tenant.

RBAC should distinguish at minimum between ordinary users and privileged administrative capabilities if the product requires them.

---

## 15. Multi-Tenant Isolation

Tenant ID should be part of the authorization boundary.

Never rely on a frontend-supplied tenant ID as proof of access.

For every tenant-sensitive database/vector query:

```text
authenticated_user
        +
authorized_tenant
        +
requested_resource
        ↓
authorization check
        ↓
query
```

A missing or invalid tenant context should fail closed.

---

## 16. Document Processing

The document ingestion pipeline should conceptually be:

```text
Upload
  ↓
File Validation
  ↓
Malware/Format Safety Checks
  ↓
Text Extraction
  ↓
Page/Section Metadata Preservation
  ↓
Chunking
  ↓
Embedding
  ↓
Vector Storage
  ↓
Document Index
```

Important invariant:

> Chunking must not destroy source-location metadata.

If a chunk originates from page 12, the retrieval result should retain page 12.

---

## 17. Summarization

Summarization should remain grounded in the selected document.

For long documents:

1. Retrieve/process relevant sections.
2. Generate section-level summaries.
3. Combine them into a document-level summary.
4. Preserve important source references.
5. Avoid adding facts that are not present in the source.

---

## 18. Meeting Action-Item Extraction

For meeting transcripts, the platform should identify:

- Action item
- Responsible person/team when explicitly stated
- Deadline when explicitly stated
- Status when explicitly stated
- Supporting transcript evidence

Do not infer ownership or deadlines that were not stated.

---

## 19. Docker / Deployment

The repository includes:

- Root `docker-compose.yml`
- Backend `Dockerfile`
- Frontend `Dockerfile`
- `nginx.conf`

The intended developer workflow is to run the complete stack through Docker Compose.

Conceptual architecture:

```text
                 ┌─────────────────┐
                 │     Browser     │
                 └────────┬────────┘
                          │
                          ▼
                    ┌───────────┐
                    │   Nginx   │
                    └─────┬─────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
       ┌─────────────┐         ┌──────────────┐
       │  Frontend   │         │   Backend    │
       │    App      │────────►│     API      │
       └─────────────┘         └──────┬───────┘
                                      │
                       ┌──────────────┼──────────────┐
                       ▼              ▼              ▼
                 Document Store   Vector Store     LLM
```

Use the repository's actual Docker Compose configuration as the source of truth for service names, ports, environment variables, and dependencies.

---

## 20. Development Workflow

Before modifying code:

1. Read `README.md`.
2. Read `constitution.md`.
3. Read `agents.md`.
4. Read `docs/ARCHITECHTURE.md`.
5. Inspect the relevant frontend/backend module.
6. Check existing types and API contracts.
7. Make the smallest coherent change.
8. Run the relevant tests/build/lint checks.
9. Verify that security and grounding invariants remain intact.

Do not rewrite unrelated parts of the repository.

---

## 21. Code Change Rules

### Prefer

- Small, focused changes
- Existing abstractions
- Strong typing
- Explicit error handling
- Unit/integration tests
- Reusable service functions
- Centralized configuration
- Schema validation
- Structured logging without secrets

### Avoid

- Hardcoded API keys
- Hardcoded JWT secrets
- Plaintext passwords
- Client-side secrets
- Fake citations
- Unsupported compliance claims
- Silent exception swallowing
- Cross-tenant queries
- Duplicated business logic
- Large unrelated refactors

---

## 22. Testing Strategy

The platform should test the complete trust chain.

### Unit tests

Test:

- Chunking
- Citation construction
- Confidence calculations
- Threshold logic
- Authorization helpers
- Compliance rule evaluation
- Response schemas

### Integration tests

Test:

- Upload → extraction → indexing
- Query → retrieval → grounded response
- Low confidence → refusal
- Authentication → authorization
- Tenant isolation
- Audit generation

### Security tests

Test:

- Invalid JWT
- Expired JWT
- Unauthorized document access
- Cross-tenant access
- Malformed uploads
- Injection attempts
- Secret leakage
- Password handling

### Critical acceptance test

A question whose answer is absent from the knowledge base must **not** receive a confident fabricated answer.

---

## 23. Observability

Useful non-sensitive telemetry includes:

- Request ID
- User/tenant-safe identifier
- Retrieval latency
- Number of retrieved chunks
- Retrieval confidence
- Refusal rate
- LLM latency
- Audit duration
- Error code

Never log:

- Passwords
- JWTs
- API keys
- Raw secrets
- Sensitive document contents unless explicitly required and protected

---

## 24. Failure Handling

The application should fail closed for security and trust-critical operations.

Examples:

### No documents

Return a clear "no knowledge available" state.

### Low retrieval confidence

Return deterministic refusal/insufficient evidence.

### Vector database unavailable

Return a service error; do not fall back to unsupported model knowledge.

### LLM unavailable

Return a controlled error; do not fabricate a result.

### Invalid citation

Reject the response or mark it invalid rather than displaying an unverified citation.

### Unauthorized access

Return an authorization error without revealing whether another tenant owns the resource.

---

## 25. Definition of Done

A feature is complete only when:

- [ ] Backend behavior is implemented.
- [ ] Frontend behavior is implemented where applicable.
- [ ] API contracts/types are synchronized.
- [ ] Authentication/authorization is enforced.
- [ ] Tenant isolation is preserved.
- [ ] Grounding requirements are preserved.
- [ ] Citations are traceable.
- [ ] Low-confidence behavior is deterministic.
- [ ] Errors are handled.
- [ ] Relevant tests pass.
- [ ] Docker workflow still works.
- [ ] Documentation is updated where necessary.
- [ ] No secrets are committed.

---

## 26. AI Coding-Agent Instructions

When an AI coding agent works on this repository, it must follow these rules:

1. Treat `constitution.md` as a non-negotiable project constraint.
2. Treat `agents.md` as the source of truth for agent behavior.
3. Inspect existing implementation before creating new abstractions.
4. Never fabricate repository files, APIs, environment variables, or dependencies.
5. Never claim that a feature works without checking the implementation/build/tests.
6. Preserve citation metadata end-to-end.
7. Preserve the 85% grounding-confidence rule.
8. Never replace missing evidence with general LLM knowledge.
9. Preserve tenant isolation.
10. Never expose credentials or secrets.
11. Prefer minimal, reviewable patches.
12. Update documentation when architecture or behavior changes.
13. If a requested feature conflicts with the constitution, identify the conflict before implementing it.
14. When uncertain about compliance facts, distinguish implementation logic from legal advice.
15. Treat external regulatory documents as evidence sources, not assumptions.

---

## 27. Recommended Commit Style

Use focused commits such as:

```text
feat: add grounded query endpoint
feat: add compliance audit result schema
fix: prevent cross-tenant document retrieval
fix: enforce grounding threshold
refactor: isolate citation validation service
test: add deterministic refusal coverage
docs: update architecture documentation
chore: update frontend dependencies
```

---

## 28. Project Success Criteria

VeriCompliance AI succeeds when a compliance user can:

1. Upload trusted documents.
2. Ask a question about those documents.
3. Receive an answer grounded in retrieved evidence.
4. Inspect exactly where the answer came from.
5. See confidence/refusal behavior when evidence is insufficient.
6. Run a compliance audit.
7. Understand PASS/FAIL/INSUFFICIENT-EVIDENCE results.
8. Extract actionable information from meeting transcripts.
9. Do all of the above without crossing tenant or authorization boundaries.

The defining product property is not simply "AI answers questions."

It is:

> **Evidence-backed answers that know when they cannot answer.**

---

## 29. Repository Source

Primary source repository:

`https://github.com/nini747heyyy/VeriComplianceAI`

This BITScript is intended to be placed at the repository root as:

`BITSCRIPT.md`

It should complement, not replace, the existing `README.md`, `constitution.md`, `agents.md`, and architecture documentation.
