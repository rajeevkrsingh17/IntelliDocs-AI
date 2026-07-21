import sys
from pathlib import Path

# Add scripts directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

from eval import judge_answer, TEST_CASES


def test_eval_judge_logic():
    """
    Test the judge evaluation heuristic on sample answers.
    """
    question = "What PDF parser does IntelliDocs-AI use?"
    expected = "PyMuPDF (fitz) is used as the primary PDF parser."
    generated = "IntelliDocs-AI uses PyMuPDF (fitz) for extracting text [tech_stack.md, Page 1: \"PyMuPDF: PDF Processing\"]."

    scores = judge_answer(question, expected, generated, is_guardrail=False)

    assert scores["correctness"] >= 4
    assert scores["citation_precision"] == 5
    assert scores["completeness"] >= 4


def test_guardrail_refusal_judge():
    """
    Test that guardrail out-of-corpus queries pass when refusal text is present.
    """
    question = "What is the capital of France?"
    expected = "I could not find this information in the uploaded document(s)."
    generated = "I could not find this information in the uploaded document(s)."

    scores = judge_answer(question, expected, generated, is_guardrail=True)

    assert scores["is_refusal"] is True
    assert scores["correctness"] == 5


def test_test_cases_dataset():
    """
    Test that the evaluation suite contains at least 20 test cases.
    """
    assert len(TEST_CASES) >= 20
