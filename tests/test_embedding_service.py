import sys
from pathlib import Path

# Add scripts directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

from search import model


def test_embedding_dimension():
    """
    Test that sentence transformer embeddings generate vectors of dimension 384.
    """
    test_text = "Hello world, testing sentence embeddings."
    embedding = model.encode([test_text])
    
    assert len(embedding) == 1
    assert len(embedding[0]) == 384  # Dimension for all-MiniLM-L6-v2
