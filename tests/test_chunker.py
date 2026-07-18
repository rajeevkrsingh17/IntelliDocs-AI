import sys
from pathlib import Path

# Add the scripts folder to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_PATH = PROJECT_ROOT / "scripts"

sys.path.append(str(SCRIPTS_PATH))

from chunker import chunk_text


def test_chunk_text():
    """
    Test that chunk_text() creates multiple non-empty chunks.
    """

    text = "This is a sample sentence. " * 200

    chunks = chunk_text(
        text=text,
        chunk_size=100,
        overlap=20,
    )

    # Check that multiple chunks are created
    assert len(chunks) > 1

    # Check that no chunk is empty
    assert all(len(chunk) > 0 for chunk in chunks)

    # Check that every chunk is a string
    assert all(isinstance(chunk, str) for chunk in chunks)