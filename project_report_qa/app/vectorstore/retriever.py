import re


def hybrid_retrieval(
    vectorstore,
    enhanced_query,
    original_query,
    k_semantic=20,
    k_final=8,
):
    """
    Hybrid retrieval:
    1. Semantic recall (FAISS)
    2. Soft keyword boosting
    """

    # -----------------------------
    # Step 1: Semantic recall
    # -----------------------------
    semantic_docs = vectorstore.similarity_search(
        enhanced_query,
        k=k_semantic
    )

    if not semantic_docs:
        return []

    # -----------------------------
    # Step 2: Keyword scoring
    # -----------------------------
    keywords = [
        kw for kw in re.split(r"\W+", original_query.lower())
        if len(kw) > 2
    ]

    scored_docs = []

    for rank, doc in enumerate(semantic_docs):
        text = doc.page_content.lower()

        keyword_hits = sum(1 for kw in keywords if kw in text)

        # Soft boost: semantic rank still matters
        score = keyword_hits * 2 + (k_semantic - rank)

        scored_docs.append((score, doc))

    # -----------------------------
    # Step 3: Final ranking
    # -----------------------------
    scored_docs.sort(key=lambda x: x[0], reverse=True)

    return [doc for _, doc in scored_docs[:k_final]]
