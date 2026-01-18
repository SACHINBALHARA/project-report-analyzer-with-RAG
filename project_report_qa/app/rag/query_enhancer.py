def enhance_query(user_query: str) -> str:
    """
    Expand user query using domain-specific synonyms
    for industrial project reports.
    """
    q = user_query.lower()

    expansions = {
        "project name": ["project name", "plant name", "unit name"],
        "budget": ["budget", "tiv", "total investment", "usd"],
        "status": ["status", "cancelled", "active", "on hold"],
        "location": ["location", "site", "city", "country"],
    }

    for key, variants in expansions.items():
        if key in q:
            return " OR ".join(variants)

    # fallback: return original query
    return user_query
