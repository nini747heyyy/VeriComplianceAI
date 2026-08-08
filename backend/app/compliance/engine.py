from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# =========================================================================================
# DATA MODELS (Pydantic Schema Definitions)
# =========================================================================================
# Using Pydantic models ensures that the LLM output conforms exactly to the schema required 
# by downstream frontend dashboards, database storage layers, and reporting tools.
# =========================================================================================

class RuleAuditResult(BaseModel):
    rule_id: str
    rule_title: str
    passed: bool
    evidence_snippet: str = Field(description="Direct text quote from document supporting or failing rule.")
    page_number: int = Field(default=0)
    risk_level: str = Field(description="CRITICAL, HIGH, MEDIUM, LOW")
    reasoning: str
    missing_clause_detected: bool

class AuditReportSummary(BaseModel):
    overall_compliance_score: float
    overall_risk_score: float
    evaluated_rules_count: int
    failed_rules_count: int
    rule_results: List[RuleAuditResult]

# =========================================================================================
# PROMPT ENGINEERING
# =========================================================================================
# System prompt designed to prime the LLM as an expert Enterprise Legal & Compliance Auditor,
# ensuring rigorous, objective, and evidence-backed evaluation.
# =========================================================================================

AUDIT_PROMPT = """You are an Enterprise Legal & Compliance Auditor.
Analyze the target Document Segment against the given Compliance Rule.

Rule: {rule_title}
Rule Statement: {rule_statement}
Severity: {severity}

Document Segment:
{document_segment}

Evaluate if the document segment satisfies, violates, or lacks required clauses dictated by the rule. Return strict JSON.
"""

# =========================================================================================
# COMPLIANCE AUDIT ENGINE CORE LOGIC
# =========================================================================================

class ComplianceAuditEngine:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.0).with_structured_output(RuleAuditResult)

    def audit_document(self, document_text_chunks: List[Dict[str, Any]], rules: List[Dict[str, Any]]) -> AuditReportSummary:
        results: List[RuleAuditResult] = []
        failed_count = 0

         # Optimization: Build full context corpus with page markers. 
        # Future-Scale Note: In production, replace this with a vector database (Chroma/Pinecone) 
        # and semantic retriever (RAG) to dynamically fetch top-k relevant chunks per rule!
        full_context = "\n".join([f"[Page {c.get('page_number', 0)}] {c.get('content', '')}" for c in document_text_chunks[:10]])

        for rule in rules:
            # Aggregate top candidate text sections or evaluate full corpus
            full_context = "\n".join([f"[Page {c['page_number']}] {c['content']}" for c in document_text_chunks[:10]])
            
            prompt = ChatPromptTemplate.from_template(AUDIT_PROMPT)
            eval_input = prompt.format(
                rule_title=rule['title'],
                rule_statement=rule['rule_statement'],
                severity=rule['severity'],
                document_segment=full_context
            )
            # Invoke LLM with strict Pydantic parsing guarantee
            res: RuleAuditResult = self.llm.invoke(eval_input)
            
            # Map the rule ID back to the audit result
            res.rule_id = rule['id']
            results.append(res)
            
            if not res.passed:
                failed_count += 1
                
       # Calculate macro compliance metrics
        total = len(rules) if len(rules) > 0 else 1
        compliance_score = round(((total - failed_count) / total) * 100, 2)
        risk_score = round((failed_count / total) * 100, 2)
        
# Assemble and return the final executive report
        return AuditReportSummary(
            overall_compliance_score=compliance_score,
            overall_risk_score=risk_score,
            evaluated_rules_count=len(rules),
            failed_rules_count=failed_count,
            rule_results=results
        )
