from collections import defaultdict

# ---- Intent detection ----
from app.rag.intent_router import (
    detect_intents,
    has_extractive_intent,
    has_descriptive_intent,
)

# ---- Unified extraction ----
from app.rag.unified_extractor import extract_from_text

# ---- Retrieval + reranking ----
from app.vectorstore.retriever import hybrid_retrieval
from app.rag.reranker import rerank

# ---- Answer formatting ----
from app.rag.answer_builder import build_answer

# ---- LLM generation ----
from app.rag.llm_generator import generate_from_chunks


# Map extractive intent → unified extractor section
INTENT_TO_SECTION = {
    "financial": "financial",
    "identity": "identity",
    "organization": "organization",
    "location": "location",
    "timeline": "timeline",
    "probability": "probability",
    "contact": "contacts",
}


def answer_question(question: str, vectorstore):
    """
    Main QA entry point.

    - Multi-PDF
    - Multi-intent
    - Deterministic extraction for facts
    - LLM fallback for descriptive questions (scope, summary, explanation)
    """

    # --------------------------------------------------
    # 1. Detect intents
    # --------------------------------------------------
    intents = detect_intents(question)

    if not has_extractive_intent(intents) and not has_descriptive_intent(intents):
        return (
            "Response:\n"
            "The question is too vague or not supported.\n\n"
            "Please ask about project details such as budget, location, scope, timeline, etc."
        )

    # --------------------------------------------------
    # 2. Retrieve + rerank
    # --------------------------------------------------
    retrieved_docs = hybrid_retrieval(
        vectorstore,
        question,   # enhanced query
        question    # original query
    )
    reranked_docs = rerank(question, retrieved_docs, top_k=15)

    if not reranked_docs:
        return (
            "Response:\n"
            "No relevant information was found in the uploaded documents."
        )

    # --------------------------------------------------
    # 3. Group chunks by PDF
    # --------------------------------------------------
    pdf_groups = defaultdict(list)
    for doc in reranked_docs:
        source = doc.metadata.get("source", "unknown")
        pdf_groups[source].append(doc)

    # keep deterministic ordering
    pdf_groups = dict(sorted(pdf_groups.items()))

    results = []

    # --------------------------------------------------
    # 4. EXTRACTIVE PATH (facts)
    # --------------------------------------------------
    if has_extractive_intent(intents):
        for pdf, docs in pdf_groups.items():
            combined_text = "\n".join(d.page_content for d in docs)
            extracted = extract_from_text(combined_text)

            project_result = {
                "pdf": pdf,
                "values": {},
                "evidence": {},
                "page": None,
            }

            for intent in intents["extractive"]:
                section = INTENT_TO_SECTION.get(intent)
                if not section:
                    continue

                values = extracted.get(section)
                if not values:
                    continue

                value = values[0]
                project_result["values"][intent] = value

                # find evidence
                for d in docs:
                    if value in d.page_content:
                        idx = d.page_content.find(value)
                        project_result["evidence"][intent] = d.page_content[
                            max(0, idx - 80): idx + len(value) + 80
                        ].strip()
                        project_result["page"] = d.metadata.get("page")
                        break

            if project_result["values"]:
                results.append(project_result)

    # --------------------------------------------------
    # 5. DESCRIPTIVE PATH (scope, summary, explanation)
    # --------------------------------------------------
    if has_descriptive_intent(intents):
        llm_inputs = []

        for pdf, docs in pdf_groups.items():
            # limit context to reduce noise
            context = "\n".join(d.page_content for d in docs[:4])

            llm_inputs.append({
                "pdf": pdf,
                "context": context
            })

        # Only descriptive question
        if not results:
            return generate_from_chunks(question, llm_inputs)

        # Mixed question: facts + explanation
        descriptive_answer = generate_from_chunks(question, llm_inputs)
        factual_answer = build_answer(question, results)

        return f"{factual_answer}\n\n---\n\n{descriptive_answer}"

    # --------------------------------------------------
    # 6. Final factual-only answer
    # --------------------------------------------------
    if not results:
        return (
            "Response:\n"
            "The requested information was not found in the uploaded documents."
        )

    return build_answer(question, results)
