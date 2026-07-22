import sys
from pathlib import Path

# Add scripts directory to sys.path for seamless imports locally & on Streamlit Cloud
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import chromadb
import streamlit as st

from llm import generate_answer
from vector_store import process_pdf, clear_database

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
uploaded_files = st.file_uploader(
    "📂 Upload Two PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    clear_database()

    total_chunks = 0

    with st.spinner("Processing PDFs..."):

        for uploaded_file in uploaded_files:

            st.write(f"📄 Processing: {uploaded_file.name}")

            pdf_path = UPLOAD_FOLDER / uploaded_file.name

            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            chunks = process_pdf(pdf_path)

            st.write(f"✅ Stored {chunks} chunks from {uploaded_file.name}")

            total_chunks += chunks

    st.success(f"✅ {len(uploaded_files)} PDFs processed successfully!")
    st.info(f"🧩 Total Chunks Created: {total_chunks}")
    st.subheader("📂 Uploaded Documents")

    for pdf in uploaded_files:
        st.write(f"✅ {pdf.name}")
# ------------------------------------------------
# Connect ChromaDB
# ------------------------------------------------

db_path = BASE_DIR / "data" / "processed" / "chroma_db"

client = chromadb.PersistentClient(path=str(db_path))

# ------------------------------------------------
# Question Input
# ------------------------------------------------

query = st.text_input(
    "💬 Ask a question (e.g., 'Compare the two documents on Machine Learning')"
)

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

    with st.spinner("Searching documents..."):
        from search import retrieve_relevant_chunks

        retrieved = retrieve_relevant_chunks(query, n_results=8)
        documents = retrieved["documents"]
        metadatas = retrieved["metadata"]

        context = ""
        for doc, meta in zip(documents, metadatas):
            doc_name = meta.get("document_name", meta.get("source", "Unknown"))
            page_num = meta.get("page", "N/A")
            chunk_num = meta.get("chunk", "N/A")
            context += (
                f"Document: {doc_name}\n"
                f"Page: {page_num}\n"
                f"Chunk: {chunk_num}\n"
                f"Content:\n{doc}\n\n"
            )

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

    for doc, meta in zip(documents, metadatas):
        doc_name = meta.get("document_name", meta.get("source", "Unknown"))
        page_num = meta.get("page", "N/A")
        chunk_num = meta.get("chunk", "N/A")
        with st.expander(f"📄 {doc_name} | Page {page_num} | Chunk {chunk_num}"):
            st.write(doc)

 