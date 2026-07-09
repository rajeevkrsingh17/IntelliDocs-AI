from pathlib import Path
from sentence_transformers import SentenceTransformer
from chunker import extract_text, chunk_text

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Locate PDF
BASE_DIR = Path(__file__).resolve().parent.parent
pdf_path = BASE_DIR / "data" / "raw" / "sample_document.pdf"

# Extract and chunk text
text = extract_text(pdf_path)
chunks = chunk_text(text)

# Generate embeddings
embeddings = model.encode(chunks)

print("=" * 50)
print("IntelliDocs-AI - Embedding Generator")
print("=" * 50)

print(f"Total Chunks      : {len(chunks)}")
print(f"Embedding Dimension: {len(embeddings[0])}")

print("\nFirst Chunk Preview:\n")
print(chunks[0][:200])

print("\nFirst Embedding (first 10 values):")
print(embeddings[0][:10])

print("\nEmbeddings generated successfully.")