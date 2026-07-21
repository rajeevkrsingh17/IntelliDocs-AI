from docx import Document


def extract_docx_text(docx_path):
    """
    Extract text from a DOCX document and return text with metadata.
    """

    document = Document(docx_path)

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    full_text = "\n".join(text)
    # Rough estimate: ~50KB per page
    page_count = max(1, len(full_text) // 50000)

    return {"text": full_text, "pages": page_count}