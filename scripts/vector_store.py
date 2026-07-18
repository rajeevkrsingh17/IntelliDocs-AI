from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from chunker import extract_text, chunk_text

# ------------------------------------------------
# Paths
# ------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "chroma_db"

# ------------------------------------------------
# Load Embedding Model
# ------------------------------------------------

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")


def process_pdf(pdf_path):
    """
    Process a PDF and store its embeddings along with metadata.
    """

    print("Extracting text...")
    text = extract_text(pdf_path)

    print("Chunking...")
    chunks = chunk_text(
        text=text,
        chunk_size=500,
        overlap=50,
    )

    print(f"Total Chunks: {len(chunks)}")

    print("Generating embeddings...")
    embeddings = model.encode(chunks)

    client = chromadb.PersistentClient(path=str(DB_PATH))

    try:
        client.delete_collection("intellidocs")
        print("Old collection deleted.")
    except Exception:
        print("No previous collection found.")

    collection = client.create_collection("intellidocs")

    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=[
            {
                "source": pdf_path.name,
                "chunk": i + 1,
            }
            for i in range(len(chunks))
        ],
    )

    print("=" * 60)
    print("IntelliDocs-AI")
    print("=" * 60)
    print(f"Database Location : {DB_PATH}")
    print(f"Chunks Stored     : {collection.count()}")
    print("Metadata Stored   : Source + Chunk Number")
    print("Embeddings stored successfully.")

    return len(chunks)


if __name__ == "__main__":

    pdf_path = BASE_DIR / "data" / "raw" / "sample_document.pdf"

    total = process_pdf(pdf_path)

    print(f"\nStored {total} chunks successfully.")