import sys
import os
from pathlib import Path
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

# Add scripts directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "scripts"))

from scripts.vector_store import GeminiEmbeddingFunction, GEMINI_API_KEY


def test_gemini_embedding_batch_logic():
    """
    Test GeminiEmbeddingFunction initialization and key handling.
    """
    ef = GeminiEmbeddingFunction(api_key="test_key")
    assert ef.model == "models/gemini-embedding-001"
    assert "batchEmbedContents" in ef.url


def test_gemini_embedding_dimension():
    """
    Test the custom Gemini embedding function if an API key is present.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return  # Skip test if no API key is configured

    ef = GeminiEmbeddingFunction(api_key=api_key)
    test_text = "Hello world, testing Gemini API embeddings."
    try:
        embeddings = ef([test_text])
        assert len(embeddings) == 1
        assert len(embeddings[0]) == 3072  # gemini-embedding-001 dimension is 3072
    except Exception as e:
        raise e


def test_gemini_embedding_sanitization():
    """
    Test that GeminiEmbeddingFunction strips leading/trailing newlines and carriage returns.
    """
    raw_key = "  pa-testkey123456789\n\r  "
    ef = GeminiEmbeddingFunction(api_key=raw_key)
    assert ef.api_key == "pa-testkey123456789"
    assert "\n" not in ef.api_key
    assert "\r" not in ef.api_key


