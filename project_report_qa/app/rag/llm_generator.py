from transformers import pipeline
from langchain.llms import HuggingFacePipeline

from app.rag.prompts import (
    FACT_PRESENTATION_PROMPT,
    DESCRIPTIVE_QA_PROMPT,
)

# -----------------------------
# Load LLM once
# -----------------------------
_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    max_new_tokens=200,
    temperature=0.0,
)

LLM = HuggingFacePipeline(pipeline=_pipeline)


# -----------------------------
# FACT-BASED ANSWER GENERATION
# -----------------------------
def generate_from_facts(question: str, structured_facts: str):
    """
    LLM used ONLY to present verified facts.
    """
    prompt = FACT_PRESENTATION_PROMPT.format(
        question=question,
        facts=structured_facts
    )

    return LLM(prompt).strip()


# -----------------------------
# DESCRIPTIVE / SCOPE QA
# -----------------------------
def generate_from_chunks(question: str, documents: list):
    """
    documents: [{ pdf, context }]
    """

    context_blocks = []

    for doc in documents:
        context_blocks.append(
            f"Document: {doc['pdf']}\n{doc['context']}"
        )

    full_context = "\n\n".join(context_blocks)

    prompt = DESCRIPTIVE_QA_PROMPT.format(
        question=question,
        context=full_context
    )

    return LLM(prompt).strip()
