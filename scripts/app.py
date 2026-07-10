from pathlib import Path

import chromadb
import streamlit as st
from sentence_transformers import SentenceTransformer

st.set_page_config(
    page_title="IntelliDocs-AI",
    page_icon="📄",
)

st.title("📄 IntelliDocs-AI")
st.write("Ask questions about your PDF using semantic search.")

# ----------------------------
# Load Model
# ----------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ----------------------------
# Connect ChromaDB
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

db_path = BASE_DIR / "data" / "processed" / "chroma_db"

client = chromadb.PersistentClient(path=str(db_path))

collection = client.get_collection("intellidocs")

# ----------------------------
# Search UI
# ----------------------------

query = st.text_input("Ask a question")

if st.button("Search"):

    if not query.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Searching document..."):

        query_embedding = model.encode([query]).tolist()

        results = collection.query(
            query_embeddings=query_embedding,
            n_results=3,
        )

    st.success("Top Matches")

    for i, doc in enumerate(results["documents"][0], start=1):
        with st.expander(f"Match {i}", expanded=True):
            st.write(doc)