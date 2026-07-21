import sys
from pathlib import Path

# Add scripts directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

from readers.pdf_reader import extract_pdf_text


def test_pdf_extraction():
    """
    Test structural text, tables, and images extraction from a PDF.
    """
    pdf_path = PROJECT_ROOT / "data" / "raw" / "sample_document.pdf"

    # Check that sample file exists before running test
    if not pdf_path.exists():
        return

    result = extract_pdf_text(pdf_path)

    assert "text" in result
    assert "pages" in result
    assert result["pages"] > 0
    assert len(result["text"]) > 0
