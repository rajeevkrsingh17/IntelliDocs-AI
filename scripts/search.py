from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from llm import generate_answer

# ------------------------------------------------
# Load Embedding Model
# ------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")
# ------------------------------------------------
# Connect ChromaDB
# ------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

db_path = BASE_DIR / "data" / "processed" / "chroma_db"

client = chromadb.PersistentClient(path=str(db_path))

collection = client.get_collection("intellidocs")

# ------------------------------------------------
# Retrieve Relevant Chunks
# ------------------------------------------------

def retrieve_relevant_chunks(query, n_results=3):
    """
    Returns the most relevant document chunks.
    """

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )

    return results["documents"][0]


# ------------------------------------------------
# CLI
# ------------------------------------------------

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("IntelliDocs-AI - RAG Document Question Answering")
    print("=" * 60)

    while True:

        query = input("\nAsk a question (type 'exit' to quit): ")

        if query.lower() == "exit":
            print("\nGoodbye!")
            break

        try:

            print("\nSearching document...")

            documents = retrieve_relevant_chunks(
                query=query,
                n_results=3,
            )

            if not documents:
                print("\nNo relevant information found.")
                continue

            context = "\n\n".join(documents)

            print("Generating answer using Gemini...")

            answer = generate_answer(
                question=query,
                context=context,
            )

            print("\n" + "=" * 60)
            print("Answer")
            print("=" * 60)
            print(answer)

            print("\n" + "=" * 60)
            print("Retrieved Context")
            print("=" * 60)

            for i, doc in enumerate(documents, start=1):

                print(f"\nChunk {i}")
                print("-" * 40)
                print(doc)

        except Exception as e:

            print("\nAn error occurred:")
            print(e)