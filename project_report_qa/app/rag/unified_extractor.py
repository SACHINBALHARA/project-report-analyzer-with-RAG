import re
from collections import defaultdict

BIG_NUMBER_RE = re.compile(r"\b\d{1,3}(?:,\d{3})+(?:,\d{3})?\b")
DATE_RE = re.compile(r"\d{2}-[A-Za-z]{3}-\d{4}")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+\d[\d\s\-]{7,}")
UPPER_NAME_RE = re.compile(r"\b[A-Z][A-Z\s]{15,}\b")

ORG_RE = re.compile(
    r"\b[A-Z][A-Za-z &]+(?:Energy|Group|Inc|Ltd|Corporation|Corp)\b"
)

LOCATION_RE = re.compile(
    r"(Location|City/State)\s*([A-Za-z0-9 ,\-]+)",
    re.IGNORECASE
)

PROBABILITY_RE = re.compile(
    r"Project Probability\s*([A-Za-z]+|\d{1,3}%|\(\d{1,3}%\))",
    re.IGNORECASE
)

STOP_WORDS = {"PEC", "DIAGRAM", "INDUSTRY", "CODE", "ACTIVITY"}
FINANCIAL_KEYWORDS = ["tiv", "usd", "investment", "capital", "cost"]


def extract_from_text(text: str):
    result = defaultdict(list)
    text_lower = text.lower()

    # Identity
    for m in UPPER_NAME_RE.findall(text):
        name = m.strip()
        for stop in STOP_WORDS:
            if stop in name:
                name = name.split(stop)[0].strip()
        if len(name.split()) >= 4:
            result["identity"].append(name)

    # Financial
    for m in BIG_NUMBER_RE.finditer(text):
        value = int(m.group().replace(",", ""))
        if value < 100_000_000:
            continue
        idx = m.start()
        window = text_lower[max(0, idx-100): idx+100]
        if any(k in window for k in FINANCIAL_KEYWORDS):
            result["financial"].append(m.group())

    # Organization
    for m in ORG_RE.findall(text):
        result["organization"].append(m.strip())

    # Contacts
    for e in EMAIL_RE.findall(text):
        result["contacts"].append(e)
    for p in PHONE_RE.findall(text):
        result["contacts"].append(p.strip())

    # Location
    m = LOCATION_RE.search(text)
    if m:
        loc = m.group(2)
        for stop in ["Phone", "Tel"]:
            if stop in loc:
                loc = loc.split(stop)[0]
        result["location"].append(loc.strip())

    # Timeline
    for d in DATE_RE.findall(text):
        result["timeline"].append(d)

    # Probability
    p = PROBABILITY_RE.search(text)
    if p:
        result["probability"].append(p.group(1))

    return result
