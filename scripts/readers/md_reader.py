def extract_md_text(md_path):
    """
    Extract text from a Markdown file and return text with metadata.
    """

    with open(md_path, "r", encoding="utf-8", errors="ignore") as file:
        text = file.read()

    # Rough estimate: ~50KB per page
    page_count = max(1, len(text) // 50000)

    return {"text": text, "pages": page_count}