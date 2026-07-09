from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from chunker import extract_text, chunk_text

# -----------------------------
# Load embedding model
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Locate PDF
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
pdf_path = BASE_DIR / "data" / "raw" / "sample_document.pdf"

# -----------------------------
# Extract and chunk text
# -----------------------------
text = extract_text(pdf_path)
chunks = chunk_text(text)

# -----------------------------
# Generate embeddings
# -----------------------------
embeddings = model.encode(chunks)

# -----------------------------
# Create persistent ChromaDB
# -----------------------------
db_path = BASE_DIR / "data" / "processed" / "chroma_db"

client = chromadb.PersistentClient(path=str(db_path))

collection = client.get_or_create_collection(
    name="intellidocs"
)

# -----------------------------
# Store data
# -----------------------------
collection.add(
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings.tolist()
)

print("=" * 50)
print("IntelliDocs-AI - ChromaDB Storage")
print("=" * 50)

print(f"Database Location : {db_path}")
print(f"Chunks Stored     : {collection.count()}")

print("\nEmbeddings successfully stored in ChromaDB.")