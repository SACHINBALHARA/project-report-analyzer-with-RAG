from sentence_transformers import CrossEncoder

# Lightweight + CPU friendly
_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, docs, top_k=3):
    """
    Re-rank retrieved documents using cross-encoder.
    """
    if not docs:
        return []

    pairs = [(query, d.page_content) for d in docs]
    scores = _model.predict(pairs)

    ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
    return [doc for _, doc in ranked[:top_k]]
