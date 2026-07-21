import sys
from pathlib import Path

# Add scripts directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

from vector_store import get_collection


def test_vector_store_collection():
    """
    Test that we can retrieve our ChromaDB collection.
    """
    collection = get_collection()
    assert collection is not None
    assert collection.name == "intellidocs"
