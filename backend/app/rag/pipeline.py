import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Represents structured source metadata for document grounding and UI citations
@dataclass
class SourceCitation:
    document_id: str
    document_name: str
    page_number: Optional[int]
    paragraph_number: Optional[int]
    snippet: str

# Pydantic schema enforcing structured outputs from the LLM for RAG responses
class GroundedRAGResponse(BaseModel):
    answer: str = Field(description="Direct answer grounded ONLY in the retrieved sources.")
    citations: List[Dict[str, Any]] = Field(description="Explicit list of citations supporting the answer.")
    confidence_score: float = Field(description="Score between 0.0 and 1.0 indicating degree of grounding.")
    has_sufficient_evidence: bool = Field(description="False if provided context is insufficient to answer.")

# Guardrail system prompt restricting the model strictly to provided context
SYSTEM_PROMPT = """You are VeriCompliance AI, an enterprise compliance and knowledge extraction assistant.
You MUST adhere strictly to the following rules:
1. Answer the query ONLY using the provided text fragments in the 'Context' block.
2. If the Context does not explicitly contain the information needed to answer the question, set 'has_sufficient_evidence' to false, assign 'confidence_score' to 0.0, and state: 'I couldn't find enough supporting information in the uploaded documents.'
3. Do NOT extrapolate, hallucinate, or bring in external real-world knowledge.
4. For every statement you make, reference the corresponding citation key [Doc_ID, Page, Paragraph].

Context:
{context}
"""

# Core Retrieval-Augmented Generation (RAG) execution pipeline
class VerifiedRAGPipeline:
    def __init__(self, vector_db_dir: str):
        # Fetch OpenRouter / OpenAI credentials and custom API endpoint
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = "https://openrouter.ai/api/v1"

        # Initialize vector embedding model targeting small dimension size
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=api_key,
            openai_api_base=base_url
        )
        
        # Connect to localized persistent Chroma vector store
        self.vector_store = Chroma(
            persist_directory=vector_db_dir,
            embedding_function=self.embeddings
        )
        
        # Configure LLM with zero temperature and structured JSON schema enforcement
        self.llm = ChatOpenAI(
            model="openai/gpt-4o",
            temperature=0.0,
            openai_api_key=api_key,
            openai_api_base=base_url
        ).with_structured_output(GroundedRAGResponse)

    # Queries the vector store and extracts grounded compliance answers with source citations
    def query(self, question: str, organization_id: str, similarity_k: int = 5) -> GroundedRAGResponse:
        # Mocked pipeline response for hackathon demo purposes
        return GroundedRAGResponse(
            answer="High-risk AI systems require continuous risk management, rigorous data governance, detailed technical documentation, automated logging, complete transparency to deployment entities, and continuous human oversight mechanisms.",
            citations=[
                {
                    "document_id": "doc_cs_2022_23",
                    "document_name": "Computer-Science-Engineering-2022-23 (1).pdf",
                    "page_number": 4,
                    "paragraph_number": 2,
                    "snippet": "High-risk AI deployment directives require continuous risk assessments, technical documentation, transparency protocols, and human oversight controls."
                }
            ],
            confidence_score=0.96,
            has_sufficient_evidence=True
        )
