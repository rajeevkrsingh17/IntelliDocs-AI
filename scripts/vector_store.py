import re
import shutil
from pathlib import Path
from datetime import datetime

import chromadb
import os
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from dotenv import load_dotenv
import google.genai as genai

# Load .env
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

from scripts.chunker import chunk_text
from scripts.document_processor import extract_document

# ------------------------------------------------
# Paths
# ------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# Render's project filesystem is read-only at runtime.
# /tmp is always writable on Render and most cloud platforms.
_IS_CLOUD = bool(os.getenv("RENDER"))
DB_PATH = Path("/tmp/chroma_db") if _IS_CLOUD else BASE_DIR / "data" / "processed" / "chroma_db"
UPLOAD_DIR = Path("/tmp/uploads") if _IS_CLOUD else BASE_DIR / "data" / "uploads"
print(f"[DB] ChromaDB path: {DB_PATH} | Cloud mode: {_IS_CLOUD}")

# ------------------------------------------------
# Embedding Functions
# ------------------------------------------------

class GeminiEmbeddingFunction(chromadb.EmbeddingFunction):
    """
    Custom ChromaDB Embedding Function that calls Google Gemini API.
    Uses 'models/gemini-embedding-001' with 768 dimensions config.
    """
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        if not input:
            return []
        
        import time
        from google.genai import types
        embeddings = []
        batch_size = 100
        for i in range(0, len(input), batch_size):
            batch = input[i:i + batch_size]
            max_retries = 5
            backoff_delay = 2.0
            for attempt in range(max_retries):
                try:
                    response = self.client.models.embed_content(
                        model="models/gemini-embedding-001",
                        contents=batch,
                        config=types.EmbedContentConfig(output_dimensionality=768),
                    )
                    for emb in response.embeddings:
                        embeddings.append(emb.values)
                    break
                except Exception as e:
                    error_str = str(e)
                    is_rate_limit = any(k in error_str for k in ("429", "RESOURCE_EXHAUSTED", "rate_limit_exceeded"))
                    
                    if is_rate_limit and attempt < max_retries - 1:
                        print(f"[WARN] Gemini embedding quota hit. Retrying in {backoff_delay}s (attempt {attempt + 1}/{max_retries})...")
                        time.sleep(backoff_delay)
                        backoff_delay *= 2
                        continue
                    else:
                        print(f"[WARN] Gemini embedding API call failed: {e}")
                        raise e
        return embeddings

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize embedding functions
_EF_ONNX = DefaultEmbeddingFunction()
_EF_GEMINI = None

if GEMINI_API_KEY:
    try:
        _EF_GEMINI = GeminiEmbeddingFunction(api_key=GEMINI_API_KEY)
        print("Gemini Cloud Embedding Function initialized (models/gemini-embedding-001, 768 dims).")
    except Exception as e:
        print(f"[WARN] Failed to initialize Gemini Embedding Function: {e}")
else:
    print("[WARN] GEMINI_API_KEY not found. Using local ONNX embeddings.")

# ------------------------------------------------
# Chroma Collection
# ------------------------------------------------

def get_collection():
    """
    Returns the appropriate collection based on whether Gemini API is available.
    """
    client = chromadb.PersistentClient(path=str(DB_PATH))
    if _EF_GEMINI is not None:
        return client.get_or_create_collection("intellidocs_gemini", embedding_function=_EF_GEMINI)
    else:
        return client.get_or_create_collection("intellidocs", embedding_function=_EF_ONNX)




# ------------------------------------------------
# Parse Page Markers from Extracted Text
# ------------------------------------------------


def _split_text_by_pages(text):
    """
    Split extracted text into page-level segments using '--- Page X ---' markers
    inserted by the PDF reader. Returns a list of (page_number, page_text) tuples.

    For documents without page markers (TXT, DOCX, etc.), returns [(1, full_text)].
    """

    # Pattern: --- Page 1 ---, --- Page 2 ---, etc.
    page_pattern = re.compile(r'\n?---\s*Page\s+(\d+)\s*---\n?')

    parts = page_pattern.split(text)

    # If no markers found, return entire text as page 1
    if len(parts) == 1:
        return [(1, text)]

    pages = []

    # parts alternates: [pre_text, page_num, page_text, page_num, page_text, ...]
    # The first element is text before any page marker (usually empty)
    i = 1  # Skip pre-marker text
    while i < len(parts) - 1:
        page_num = int(parts[i])
        page_text = parts[i + 1].strip()
        if page_text:
            pages.append((page_num, page_text))
        i += 2

    return pages if pages else [(1, text)]


# ------------------------------------------------
# Process Document
# ------------------------------------------------


def process_document(file_path, session_id=None):
    """
    Extract text, create chunks, generate embeddings (via ONNX — no API needed)
    and store them inside ChromaDB.

    Works with:
    - PDF
    - DOCX
    - TXT
    - PPTX
    - Markdown
    """

    file_path = Path(file_path)

    print("\n" + "=" * 60)
    print(f"Processing : {file_path.name} | Session: {session_id}")
    print("=" * 60)

    # --------------------------------------------
    # Extract Text
    # --------------------------------------------

    print("Extracting text...")

    extracted = extract_document(file_path)

    # Handle both dict format (with metadata) and string format (backward compatibility)
    if isinstance(extracted, dict):
        text = extracted.get("text", "")
        pages = extracted.get("pages", 1)
    else:
        text = extracted
        pages = 1

    if not text.strip():
        raise ValueError("No text could be extracted from the document.")

    print(f"Characters Extracted : {len(text)}")
    print(f"Pages: {pages}")

    # --------------------------------------------
    # Page-Aware Chunking
    # --------------------------------------------

    print("Chunking document (sentence-aware, page-tracked)...")

    # Split text by page markers for accurate page numbers
    page_segments = _split_text_by_pages(text)

    all_chunks = []       # List of chunk text strings
    all_page_nums = []    # Corresponding page number for each chunk

    for page_num, page_text in page_segments:
        page_chunks = chunk_text(
            text=page_text,
            chunk_size=800,
            overlap_sentences=2,
        )

        for chunk in page_chunks:
            all_chunks.append(chunk)
            all_page_nums.append(page_num)

    print(f"Generated {len(all_chunks)} chunks across {len(page_segments)} pages.")

    if not all_chunks:
        raise ValueError("No chunks could be generated from the document.")

    # --------------------------------------------
    # ChromaDB — embeddings generated automatically
    # by the ONNX embedding function, no API call needed
    # --------------------------------------------

    print("Storing chunks (ONNX embeddings generated in-process)...")
    collection = get_collection()

    # Remove existing chunks for this document if re-uploaded
    try:
        delete_clause = {"document_name": file_path.name}
        if session_id:
            delete_clause = {"$and": [{"document_name": file_path.name}, {"session_id": session_id}]}
        collection.delete(where=delete_clause)
    except Exception:
        pass

    ids = []
    metadatas = []
    base_count = collection.count()

    for i in range(len(all_chunks)):
        ids.append(f"{file_path.stem}_chunk_{base_count + i}")

        meta_entry = {
            "document_name": file_path.name,
            "document_type": file_path.suffix.replace(".", "").upper(),
            "chunk": i + 1,
            "page": all_page_nums[i],
            "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        if session_id:
            meta_entry["session_id"] = session_id
        metadatas.append(meta_entry)

    # ChromaDB calls _EF(all_chunks) internally — pure ONNX, no network call
    collection.add(
        ids=ids,
        documents=all_chunks,
        metadatas=metadatas,
    )

    print(f"Added {len(all_chunks)} chunks.")

    # --------------------------------------------
    # Summary
    # --------------------------------------------

    print("\n" + "=" * 60)
    print("IntelliDocs AI")
    print("=" * 60)

    print(f"Document : {file_path.name}")
    print(f"Type     : {file_path.suffix.upper()}")
    print(f"Chunks   : {len(all_chunks)}")
    print(f"Pages    : {pages}")
    print(f"Database : {DB_PATH}")

    print(f"\nTotal Chunks in Database : {collection.count()}")

    print("\nMetadata Stored")
    print("- Document Name")
    print("- Document Type")
    print("- Chunk Number")
    print("- Page Number (accurate)")
    print("- Upload Time")

    print("\nEmbedding completed successfully.\n")

    return {"chunks": len(all_chunks), "pages": pages}


def get_all_documents(session_id=None) -> list[dict]:
    """
    Retrieves metadata of all documents currently indexed in ChromaDB for a specific session.
    Returns a list of dictionaries containing: name, type, chunks, pages, size.
    """
    try:
        collection = get_collection()
        where_clause = {"session_id": session_id} if session_id else None
        results = collection.get(where=where_clause, include=["metadatas"])
        metadatas = results.get("metadatas", [])
        if not metadatas:
            return []

        doc_info = {}
        for meta in metadatas:
            doc_name = meta.get("document_name")
            if not doc_name:
                continue

            if doc_name not in doc_info:
                doc_path = UPLOAD_DIR / doc_name
                size = 0
                if doc_path.exists():
                     size = doc_path.stat().st_size

                doc_info[doc_name] = {
                    "name": doc_name,
                    "type": meta.get("document_type", ""),
                    "chunks": 0,
                    "pages": 1,
                    "size": size,
                }

            doc_info[doc_name]["chunks"] += 1
            doc_info[doc_name]["pages"] = max(doc_info[doc_name]["pages"], meta.get("page", 1))

        return list(doc_info.values())
    except Exception as e:
        print(f"[WARN] Failed to retrieve documents from ChromaDB: {e}")
        return []


def delete_document_from_db(document_name: str, session_id=None) -> bool:
    """
    Deletes all chunks belonging to a specific document from ChromaDB for a specific session.
    """
    try:
        collection = get_collection()
        delete_clause = {"document_name": document_name}
        if session_id:
            delete_clause = {"$and": [{"document_name": document_name}, {"session_id": session_id}]}
        collection.delete(where=delete_clause)
        print(f"Deleted '{document_name}' from ChromaDB.")
        return True
    except Exception as e:
        print(f"[WARN] Failed to delete '{document_name}' from ChromaDB: {e}")
        return False


# ------------------------------------------------
# Backward Compatibility Wrappers for Streamlit
# ------------------------------------------------

def clear_database(session_id=None):
    """
    Clears all collections from ChromaDB for a specific session.
    """
    if session_id:
        try:
            collection = get_collection()
            collection.delete(where={"session_id": session_id})
            print(f"Cleared database for session: {session_id}")
            return
        except Exception as e:
            print(f"[WARN] Failed to clear collection by session ID: {e}")
            return

    # First try to delete via the client API (nuke whole DB if no session)
    try:
        client = chromadb.PersistentClient(path=str(DB_PATH))
        client.delete_collection("intellidocs")
        print("Database collection 'intellidocs' deleted via API.")
    except Exception:
        pass

    # Then nuke the directory on disk to be absolutely sure
    if DB_PATH.exists():
        try:
            shutil.rmtree(DB_PATH)
            print(f"ChromaDB directory deleted: {DB_PATH}")
        except Exception as e:
            print(f"[WARN] Could not delete ChromaDB directory: {e}")

    # Recreate the directory
    DB_PATH.mkdir(parents=True, exist_ok=True)
    print("Fresh ChromaDB directory created.")


def process_pdf(file_path):
    """
    Wrapper for processing PDF documents.
    Returns the number of chunks.
    """
    result = process_document(file_path)
    return result["chunks"]


# ------------------------------------------------
# CLI Test
# ------------------------------------------------

if __name__ == "__main__":

    sample = BASE_DIR / "data" / "raw" / "sample_document.pdf"

    result = process_document(sample)

    print(f"\nStored {result['chunks']} chunks from {result['pages']} pages successfully.")