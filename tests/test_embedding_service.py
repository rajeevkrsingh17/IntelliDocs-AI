import sys
import os
from pathlib import Path
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

# Add scripts directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "scripts"))

from scripts.vector_store import VoyageEmbeddingFunction, VOYAGE_API_KEY


def test_embedding_dimension():
    """
    Test that the Chroma built-in embedding function generates vectors of dimension 384.
    """
    ef = DefaultEmbeddingFunction()
    test_text = "Hello world, testing sentence embeddings."
    embeddings = ef([test_text])
    
    assert len(embeddings) == 1
    assert len(embeddings[0]) == 384  # all-MiniLM-L6-v2 embedding dimension is 384


def test_voyage_embedding_dimension():
    """
    Test the custom Voyage embedding function if an API key is present.
    """
    api_key = os.getenv("VOYAGE_API_KEY")
    if not api_key:
        return  # Skip test if no API key is configured

    ef = VoyageEmbeddingFunction(api_key=api_key)
    test_text = "Hello world, testing Voyage API embeddings."
    try:
        embeddings = ef([test_text])
        assert len(embeddings) == 1
        assert len(embeddings[0]) == 512  # voyage-4-lite dimension is 512
    except Exception as e:
        raise e


def test_voyage_embedding_sanitization():
    """
    Test that VoyageEmbeddingFunction strips leading/trailing newlines and carriage returns.
    """
    raw_key = "  pa-testkey123456789\n\r  "
    ef = VoyageEmbeddingFunction(api_key=raw_key)
    assert ef.api_key == "pa-testkey123456789"
    assert "\n" not in ef.api_key
    assert "\r" not in ef.api_key

