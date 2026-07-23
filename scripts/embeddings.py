from pathlib import Path
from scripts.vector_store import GeminiEmbeddingFunction, GEMINI_API_KEY
from scripts.chunker import extract_document, chunk_text

BASE_DIR = Path(__file__).resolve().parent.parent
pdf_path = BASE_DIR / "data" / "raw" / "sample_document.pdf"

if pdf_path.exists():
    text = extract_document(pdf_path)
    chunks = chunk_text(text)
    ef = GeminiEmbeddingFunction(api_key=GEMINI_API_KEY or "dummy_key")
    print("IntelliDocs-AI - Embedding Generator (Gemini text-embedding-004)")
    print(f"Total Chunks: {len(chunks)}")