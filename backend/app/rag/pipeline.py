import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

@dataclass
class SourceCitation:
    document_id: str
    document_name: str
    page_number: Optional[int]
    paragraph_number: Optional[int]
    snippet: str

class GroundedRAGResponse(BaseModel):
    answer: str = Field(description="Direct answer grounded ONLY in the retrieved sources.")
    citations: List[Dict[str, Any]] = Field(description="Explicit list of citations supporting the answer.")
    confidence_score: float = Field(description="Score between 0.0 and 1.0 indicating degree of grounding.")
    has_sufficient_evidence: bool = Field(description="False if provided context is insufficient to answer.")

SYSTEM_PROMPT = """You are VeriCompliance AI, an enterprise compliance and knowledge extraction assistant.
You MUST adhere strictly to the following rules:
1. Answer the query ONLY using the provided text fragments in the 'Context' block.
2. If the Context does not explicitly contain the information needed to answer the question, set 'has_sufficient_evidence' to false, assign 'confidence_score' to 0.0, and state: 'I couldn't find enough supporting information in the uploaded documents.'
3. Do NOT extrapolate, hallucinate, or bring in external real-world knowledge.
4. For every statement you make, reference the corresponding citation key [Doc_ID, Page, Paragraph].

Context:
{context}
"""

class VerifiedRAGPipeline:
    def __init__(self, vector_db_dir: str):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_store = Chroma(
            persist_directory=vector_db_dir,
            embedding_function=self.embeddings
        )
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.0).with_structured_output(GroundedRAGResponse)

    def query(self, question: str, organization_id: str, similarity_k: int = 5) -> GroundedRAGResponse:
        # Multi-tenant isolation filter
        retriever = self.vector_store.as_retriever(
            search_kwargs={
                "k": similarity_k,
                "filter": {"organization_id": organization_id}
            }
        )
        
        docs = retriever.get_relevant_documents(question)
        if not docs:
            return GroundedRAGResponse(
                answer="I couldn't find enough supporting information in the uploaded documents.",
                citations=[],
                confidence_score=0.0,
                has_sufficient_evidence=False
            )

        context_str = ""
        citations_map = []
        for idx, doc in enumerate(docs):
            meta = doc.metadata
            c_tag = f"[Source_{idx+1}: Doc {meta.get('title')}, Page {meta.get('page_number')}, Para {meta.get('paragraph_number')}]"
            context_str += f"{c_tag}\n{doc.page_content}\n\n"
            citations_map.append({
                "source_tag": c_tag,
                "document_id": meta.get("document_id"),
                "document_title": meta.get("title"),
                "page_number": meta.get("page_number"),
                "paragraph_number": meta.get("paragraph_number"),
                "content_preview": doc.page_content[:200]
            })

        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "Question: {question}\n\nProvide a structured answer with strict grounding.")
        ])

        formatted_prompt = prompt.format(context=context_str, question=question)
        response: GroundedRAGResponse = self.llm.invoke(formatted_prompt)

        # Post-process verification check
        if not response.has_sufficient_evidence:
            response.answer = "I couldn't find enough supporting information in the uploaded documents."
            response.citations = []
            response.confidence_score = 0.0

        return response