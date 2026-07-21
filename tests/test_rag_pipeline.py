import sys
from pathlib import Path

# Add scripts directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

from llm import generate_answer


def test_rag_pipeline_answer():
    """
    Test generating an answer using the fallback chain.
    """
    context = "PyMuPDF is used to extract text and tables from PDFs in IntelliDocs-AI."
    question = "Which parser is used for PDFs?"

    answer = generate_answer(question, context)

    assert len(answer) > 0
    assert "PyMuPDF" in answer or "mock" in answer.lower()
