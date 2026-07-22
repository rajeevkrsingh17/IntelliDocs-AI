import sys
import os
from pathlib import Path
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

# Add scripts directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "scripts"))

from scripts.vector_store import GeminiEmbeddingFunction, GEMINI_API_KEY


def test_embedding_dimension():
    """
    Test that the Chroma built-in embedding function generates vectors of dimension 384.
    """
    ef = DefaultEmbeddingFunction()
    test_text = "Hello world, testing sentence embeddings."
    embeddings = ef([test_text])
    
    assert len(embeddings) == 1
    assert len(embeddings[0]) == 384  # all-MiniLM-L6-v2 embedding dimension is 384


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
        assert len(embeddings[0]) == 768  # text-embedding-004 dimension is 768
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print(f"\n[WARN] Skipping test_gemini_embedding_dimension due to API quota exhaustion: {e}")
            return
        raise e

