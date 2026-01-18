from langchain.prompts import PromptTemplate


FACT_PRESENTATION_PROMPT = PromptTemplate(
    input_variables=["question", "facts"],
    template="""
You are an industrial project analyst.

You are given VERIFIED facts extracted from project documents.
Do NOT invent or infer information.

Question:
{question}

Extracted Facts (per project):
{facts}

Instructions:
- Answer clearly and professionally
- Separate answers per project
- Do NOT add information not present in the facts
"""
)


DESCRIPTIVE_QA_PROMPT = PromptTemplate(
    input_variables=["question", "context"],
    template="""
You are an industrial project analyst.

Answer the question using ONLY the context below.
The documents are semi-structured project reports.

Rules:
- Do NOT invent facts
- Do NOT speculate
- If information is missing, say "Not specified in the document"
- Answer per project if multiple documents are present

Context:
{context}

Question:
{question}

Answer:
"""
)
