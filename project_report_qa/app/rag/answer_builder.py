import os


def build_answer(question: str, results: list):
    """
    Build final user-facing answer.

    Expected result format:
    {
        "pdf": str,
        "values": { intent: value },
        "evidence": { intent: evidence_text },
        "page": int | None
    }
    """

    lines = ["Response:\n"]

    # -----------------------------
    # Answers per project
    # -----------------------------
    for idx, result in enumerate(results, start=1):
        lines.append(f"Project {idx}:")

        for intent, value in result["values"].items():
            label = intent.replace("_", " ").title()
            lines.append(f"- {label}: {value}")

        lines.append("")

    # -----------------------------
    # Sources
    # -----------------------------
    lines.append("Sources:")

    for idx, result in enumerate(results, start=1):
        raw_path = result["pdf"]

        # extract filename only (no temp path)
        filename = os.path.basename(raw_path)

        # try to get project name if available
        project_name = None
        if "identity" in result["values"]:
            project_name = result["values"]["identity"]

        page = result.get("page", 0)
        page_display = page + 1 if isinstance(page, int) else page

        if project_name:
            lines.append(
                f"- PDF-{idx} ({project_name}), Page {page_display}"
            )
        else:
            lines.append(
                f"- PDF-{idx} ({filename}), Page {page_display}"
            )

    # -----------------------------
    # Evidence
    # -----------------------------
    lines.append("\nEvidence (Direct Quotes):")

    for result in results:
        for intent, evidence in result["evidence"].items():
            label = intent.replace("_", " ").title()
            lines.append(f"- ({label}) \"{evidence}\"")

    return "\n".join(lines)
