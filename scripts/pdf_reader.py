import fitz
from pathlib import Path


def extract_pdf_text(file_path):
    """
    Extract text from a PDF.

    Returns:
        list[dict]

        Example:
        [
            {
                "page": 1,
                "text": "Page 1 text..."
            },
            {
                "page": 2,
                "text": "Page 2 text..."
            }
        ]
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    document = fitz.open(file_path)

    pages = []

    try:

        for page_number, page in enumerate(document, start=1):

            text = page.get_text("text").strip()

            if not text:
                continue

            pages.append(
                {
                    "page": page_number,
                    "text": text,
                }
            )

    finally:
        document.close()

    return pages