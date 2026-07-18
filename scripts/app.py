from pathlib import Path

import chromadb
import streamlit as st
from sentence_transformers import SentenceTransformer

from llm import generate_answer
from vector_store import process_pdf

# ------------------------------------------------
# Base Directory
# ------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------
# Page Config
# ------------------------------------------------

st.set_page_config(
    page_title="IntelliDocs-AI",
    page_icon="📄",
    layout="wide",
)

st.title("📄 IntelliDocs-AI")
st.caption("Retrieval-Augmented Generation (RAG) powered by ChromaDB + Gemini")

# ------------------------------------------------
# Upload Folder
# ------------------------------------------------

UPLOAD_FOLDER = BASE_DIR / "data" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------
# Upload PDF
# ------------------------------------------------

uploaded_file = st.file_uploader(
    "📂 Upload a PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    pdf_path = UPLOAD_FOLDER / uploaded_file.name

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Processing PDF..."):

        total_chunks = process_pdf(pdf_path)

    st.success("✅ PDF processed successfully!")
    st.info(f"🧩 Chunks Created: {total_chunks}")

# ------------------------------------------------
# Load Embedding Model
# ------------------------------------------------

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()

# ------------------------------------------------
# Connect ChromaDB
# ------------------------------------------------

db_path = BASE_DIR / "data" / "processed" / "chroma_db"

client = chromadb.PersistentClient(path=str(db_path))

# ------------------------------------------------
# Question Input
# ------------------------------------------------

query = st.text_input("Ask a question about your document")

# ------------------------------------------------
# Generate Answer
# ------------------------------------------------

if st.button("Generate Answer"):

    if not query.strip():
        st.warning("Please enter a question.")
        st.stop()

    try:
        collection = client.get_collection("intellidocs")
    except Exception:
        st.error("No document found. Please upload a PDF first.")
        st.stop()

    with st.spinner("Searching document..."):

        query_embedding = model.encode([query]).tolist()

        results = collection.query(
            query_embeddings=query_embedding,
            n_results=3,
            include=["documents", "metadatas"],
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        context = "\n\n".join(documents)

    with st.spinner("Generating answer..."):

        answer = generate_answer(
            question=query,
            context=context,
        )

    st.success("✅ Answer Generated!")

    st.subheader("🤖 AI Answer")
    st.write(answer)

    st.divider()

    st.subheader("📄 Retrieved Context")

    for i, (doc, meta) in enumerate(zip(documents, metadatas), start=1):

        with st.expander(f"Chunk {i}"):

            st.markdown(f"**📄 Source:** `{meta['source']}`")
            st.markdown(f"**📍 Chunk Number:** `{meta['chunk']}`")

            st.write(doc)