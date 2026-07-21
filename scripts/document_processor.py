from pathlib import Path

from scripts.readers.pdf_reader import extract_pdf_text
from scripts.readers.docx_reader import extract_docx_text
from scripts.readers.txt_reader import extract_txt_text
from scripts.readers.pptx_reader import extract_pptx_text
from scripts.readers.md_reader import extract_md_text


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".pptx",
    ".md",
}


def extract_document(file_path):
    """
    Extract text from a supported document.
    """

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}")

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    if extension == ".docx":
        return extract_docx_text(file_path)

    if extension == ".txt":
        return extract_txt_text(file_path)

    if extension == ".pptx":
        return extract_pptx_text(file_path)

    if extension == ".md":
        return extract_md_text(file_path)

    raise ValueError(f"No reader available for {extension}")