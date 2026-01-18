from collections import defaultdict
from app.rag.fact_extractor import extract_facts_from_text


def aggregate_by_pdf(docs):
    """
    Group retrieved chunks by PDF and extract facts per document.
    """
    pdf_groups = defaultdict(list)

    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        pdf_groups[source].append(doc)

    aggregated_results = []

    for pdf_name, pdf_docs in pdf_groups.items():
        combined_text = "\n".join(d.page_content for d in pdf_docs)
        facts = extract_facts_from_text(combined_text)

        aggregated_results.append({
            "pdf": pdf_name,
            "facts": facts,
            "docs": pdf_docs,
        })

    return aggregated_results
