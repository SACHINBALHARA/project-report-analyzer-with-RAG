# -----------------------------
# Intent keyword maps
# -----------------------------

EXTRACTIVE_INTENTS = {
    "financial": ["budget", "cost", "tiv", "usd", "investment", "capital"],
    "location": ["location", "where", "site", "address"],
    "identity": ["project name", "plant name", "project", "name"],
    "organization": ["owner", "company", "parent", "manager", "responsibility"],
    "timeline": ["update", "phase", "timeline", "completion", "start", "end"],
    "probability": ["probability", "chance", "likelihood"],
    "contact": ["contact", "email", "phone"],
}

DESCRIPTIVE_INTENTS = {
    "scope": [
        "scope",
        "what does the project involve",
        "project involves",
        "project scope",
    ],
    "description": [
        "description",
        "overview",
        "summary",
        "explain",
        "details",
        "about the project",
    ],
    "history": [
        "history",
        "background",
        "previous",
        "past",
    ],
    "comparison": [
        "compare",
        "difference",
        "which project",
        "higher",
        "lower",
    ],
}


# -----------------------------
# Main intent detector
# -----------------------------

def detect_intents(question: str):
    q = question.lower()
    intents = {
        "extractive": [],
        "descriptive": [],
    }

    # detect extractive intents
    for intent, keywords in EXTRACTIVE_INTENTS.items():
        if any(k in q for k in keywords):
            intents["extractive"].append(intent)

    # detect descriptive intents
    for intent, keywords in DESCRIPTIVE_INTENTS.items():
        if any(k in q for k in keywords):
            intents["descriptive"].append(intent)

    return intents


# -----------------------------
# Helpers
# -----------------------------

def has_extractive_intent(intents: dict) -> bool:
    return len(intents.get("extractive", [])) > 0


def has_descriptive_intent(intents: dict) -> bool:
    return len(intents.get("descriptive", [])) > 0
