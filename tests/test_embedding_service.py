import sys
from pathlib import Path
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

# Add scripts directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))


def test_embedding_dimension():
    """
    Test that the Chroma built-in embedding function generates vectors of dimension 384.
    """
    ef = DefaultEmbeddingFunction()
    test_text = "Hello world, testing sentence embeddings."
    embeddings = ef([test_text])
    
    assert len(embeddings) == 1
    assert len(embeddings[0]) == 384  # all-MiniLM-L6-v2 embedding dimension is 384
