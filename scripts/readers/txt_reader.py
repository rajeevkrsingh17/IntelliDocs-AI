def extract_txt_text(txt_path):
    """
    Extract text from a TXT file and return text with metadata.
    """

    with open(txt_path, "r", encoding="utf-8", errors="ignore") as file:
        text = file.read()

    # Rough estimate: ~50KB per page
    page_count = max(1, len(text) // 50000)

    return {"text": text, "pages": page_count}