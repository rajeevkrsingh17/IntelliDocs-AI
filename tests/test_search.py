import sys
from pathlib import Path

# Add scripts directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

from search import BM25


def test_bm25_ranking():
    corpus = [
        "The quick brown fox jumps over the lazy dog",
        "Python is a great programming language for AI and machine learning",
        "Information retrieval systems use vector search and BM25 keyword matching",
    ]

    bm25 = BM25(corpus)

    # Query matching exact words in document 2
    scores_python = bm25.get_scores("Python programming AI")
    # Document 2 (index 1) should have the highest score
    best_doc_idx = scores_python.index(max(scores_python))
    assert best_doc_idx == 1

    # Query matching exact words in document 3
    scores_ir = bm25.get_scores("vector search BM25")
    best_doc_idx_ir = scores_ir.index(max(scores_ir))
    assert best_doc_idx_ir == 2
