import fitz  # PyMuPDF
from pathlib import Path

# -----------------------------
# Locate the PDF file
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
pdf_path = BASE_DIR / "data" / "raw" / "sample_document.pdf"

# -----------------------------
# Check if the PDF exists
# -----------------------------
if not pdf_path.exists():
    print(f"Error: PDF file not found at:\n{pdf_path}")
    exit()

try:
    # -----------------------------
    # Open the PDF
    # -----------------------------
    doc = fitz.open(pdf_path)

    print("=" * 50)
    print("IntelliDocs-AI - PDF Reader")
    print("=" * 50)
    print(f"Loaded PDF : {pdf_path.name}")
    print(f"Total Pages: {len(doc)}")

    # -----------------------------
    # Extract text
    # -----------------------------
    text = ""

    for page in doc:
        try:
            text += page.get_text()
        except Exception:
            # Skip problematic pages without stopping the program
            continue

    print(f"Characters Extracted: {len(text)}")

    # -----------------------------
    # Simple Query
    # -----------------------------
    query = "combination"

    print("\nSearching document...")

    if query.lower() in text.lower():
        print(f"Result: '{query}' found in the document.")
    else:
        print(f"Result: '{query}' not found in the document.")

    doc.close()

    print("\nPDF processing completed successfully.")

except Exception as e:
    print(f"\nError while reading PDF:\n{e}")