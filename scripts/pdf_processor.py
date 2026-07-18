import shutil
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from chunker import extract_text_from_pdf, chunk_text


BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_FOLDER = BASE_DIR / "data" / "uploads"
DB_PATH = BASE_DIR / "data" / "processed" / "chroma_db"

MODEL_NAME = "all-MiniLM-L6-v2"


def process_pdf(uploaded_pdf_path):
    """
    Process uploaded PDF:
    1. Extract text
    2. Chunk text
    3. Generate embeddings
    4. Store into ChromaDB
    """

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Extracting text...")
    text = extract_text_from_pdf(uploaded_pdf_path)

    print("Chunking document...")
    chunks = chunk_text(text)

    print("Generating embeddings...")
    embeddings = model.encode(chunks).tolist()

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path=str(DB_PATH))

    # Delete old collection
    try:
        client.delete_collection("intellidocs")
    except Exception:
        pass

    collection = client.create_collection("intellidocs")

    print("Saving embeddings...")

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    print("Done!")

    return len(chunks)