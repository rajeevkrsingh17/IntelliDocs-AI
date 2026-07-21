from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from chunker import extract_text, chunk_text

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "processed" / "chroma_db"

MODEL_NAME = "all-MiniLM-L6-v2"


def process_pdf(pdf_path):
    """
    Process an uploaded PDF:
    1. Extract text
    2. Chunk text
    3. Generate embeddings
    4. Store in ChromaDB
    """

    model = SentenceTransformer(MODEL_NAME)

    text = extract_text(pdf_path)

    chunks = chunk_text(text)

    embeddings = model.encode(chunks).tolist()

    client = chromadb.PersistentClient(path=str(DB_PATH))

    # Delete previous collection
    try:
        client.delete_collection("intellidocs")
    except Exception:
        pass

    collection = client.create_collection("intellidocs")

    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings,
    )

    return len(chunks)