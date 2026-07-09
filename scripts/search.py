from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# -----------------------------
# Load embedding model
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Connect to ChromaDB
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

db_path = BASE_DIR / "data" / "processed" / "chroma_db"

client = chromadb.PersistentClient(path=str(db_path))

collection = client.get_collection("intellidocs")

print("=" * 50)
print("IntelliDocs-AI - Semantic Search")
print("=" * 50)

while True:
    query = input("\nAsk a question (type 'exit' to quit): ")

    if query.lower() == "exit":
        print("Goodbye!")
        break

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    print("\nTop Matching Chunks:\n")

    for i, document in enumerate(results["documents"][0], start=1):
        print(f"Match {i}")
        print("-" * 40)
        print(document[:500])
        print()