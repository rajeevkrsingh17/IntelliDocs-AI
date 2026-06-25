import fitz  # PyMuPDF

pdf_path = "data/raw/Probability_Study_Material.pdf"

doc = fitz.open(pdf_path)

print(f"Total Pages: {len(doc)}")

text = ""

for page in doc:
    text += page.get_text()

query = "probability"

if query.lower() in text.lower():
    print(f"'{query}' found in the document.")
else:
    print(f"'{query}' not found in the document.")

doc.close()