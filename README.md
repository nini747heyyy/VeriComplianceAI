# VeriCompliance AI – Knowledge & Compliance Agent Platform

_“In legal and regulatory compliance, a 95% accurate AI is a 100% liability.”_

VeriCompliance AI is an enterprise-grade platform engineered to eliminate artificial intelligence
hallucinations in high-stakes legal, regulatory, and corporate compliance operations. By
combining Deterministic Refusal Protocols with Granular Grounding, we ensure every
answer is backed by verifiable evidence.

## 🚀 The Problem

Organizations deal with a huge number of documents every day, including company policies,
compliance guidelines, contracts, legal documents, and meeting transcripts. Most of this
information is unstructured, making it difficult to find the right answers quickly.
Although Large Language Models (LLMs) are great at understanding language, they can
sometimes generate information that is incorrect but sounds convincing. This becomes a serious
problem in compliance, legal, healthcare, and finance, where every answer must be accurate and
backed by real evidence. A compliance officer cannot rely on a system that invents regulations or
misinterprets policies.
Most AI chatbots answer questions using their general knowledge instead of the organization's
actual documents. As a result, users have no way to verify whether the information is correct or
where it came from.
The challenge is to build a knowledge and compliance agent that understands unstructured
documents, gives reliable answers based only on the provided data, and clearly shows the source
of every response.

## ✨Our Solution- VeriCompliance AI

VeriCompliance AI is a knowledge and compliance assistant designed to provide accurate and
trustworthy answers from uploaded documents. Instead of relying on general AI knowledge, it searches
through the provided files and generates responses only from verified content.

<img width="1418" height="902" alt="image" src="https://github.com/user-attachments/assets/07e5a775-479e-4d1f-a84c-d9941159531b" />

 ### Trust, Grounding & Evidence — At a Glance

• Verified Knowledge: Upload policies, contracts, compliance manuals, and meeting transcripts.

• Traceable Answers: Ask questions and receive answers supported by document citation

• Intelligent Summarization: Generate clear summaries of long documents.

• Compliance Auditing: Check documents against compliance rules and receive pass or fail reports
with supporting evidence.

• Actionable Insights: Extract action items from meeting transcripts and link them back to the original
source.

By making every answer traceable to the original document, VeriCompliance AI reduces AI
hallucinations and helps organizations make decisions they can trust

## 🚀 Key Technical Features

1. Grounded RAG Pipeline: Implements a sophisticated Retrieval-Augmented
Generation(RAG)system with structured citations including exact Page, Line, and
Paragraph metadata

2. Deterministic Refusal Protocol: A safety layer that refuses to output responses if
semantic search confidence drops below a specific threshold, ensuring zero guesswork.

3. Compliance Audit Engine: Automates the evaluation of unstructured documents
against customisable or template-based compliance matrices.

4. Hardened Security: Built with enterprise-level RBAC, Multi-Tenant isolation, JWT with
Argon2, and encrypted vector storage

## 🛠Technical Architecture & Data Flow

<img width="792" height="689" alt="image" src="https://github.com/user-attachments/assets/fb56dd09-ffcf-4add-b320-e69c3fd67bce" />

## 🛠 Tech Stack

<img width="735" height="269" alt="image" src="https://github.com/user-attachments/assets/366a6ada-51e3-41e1-ae8f-f81324dac502" />

## 📦 Quick Start(Docker)

Get the full stack running in under 2 minutes:

```
git clone https://github.com/nini747heyyy/VeriComplianceAI.git

cd VeriComplianceAI

docker-compose up /-build
```

Access the dashboard at:
```http://localhost:3000``` .

## 🚀 Meet the Team — The Compliance Crew

**4 minds. 1 mission. 0 tolerance for hallucinations.**

🧑‍💻 Names:

1. Anuska Sharma ( Team Lead )

2. Devangi Banerjee
 
3. Sreeja Guha

> **Built under pressure. Driven by innovation.  
> Engineered for trustworthy AI.**

 




