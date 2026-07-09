from pathlib import Path
import fitz


def extract_text(pdf_path):
    """Extract text from a PDF file."""
    document = fitz.open(pdf_path)
    text = ""

    for page in document:
        text += page.get_text()

    document.close()
    return text


def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    pdf_path = BASE_DIR / "data" / "raw" / "sample_document.pdf"

    text = extract_text(pdf_path)
    chunks = chunk_text(text)

    print("=" * 50)
    print("IntelliDocs-AI - Text Chunker")
    print("=" * 50)

    print(f"Characters Extracted : {len(text)}")
    print(f"Total Chunks Created : {len(chunks)}")

    print("\nFirst Chunk Preview:\n")
    print(chunks[0][:300])

    print("\nChunking completed successfully.")