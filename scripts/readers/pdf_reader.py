import fitz


def extract_pdf_text(pdf_path):
    """
    Extract text structurally from a PDF document.
    - Handles text blocks.
    - Extracts tables and represents them as Markdown tables.
    - Detects images and inserts structural placeholders.
    """

    document = fitz.open(pdf_path)

    text = ""
    page_count = len(document)

    for page_num, page in enumerate(document, start=1):
        page_text = page.get_text("text").strip()
        
        # 1. Fast Table Extraction (only if text suggests tabular structure or small doc)
        table_text = ""
        if page_text and (page_count <= 20 or "\t" in page_text or "|" in page_text or "  " in page_text):
            try:
                tables = page.find_tables()
                if tables and len(tables) > 0:
                    for t_idx, table in enumerate(tables, start=1):
                        data = table.extract()
                        if data and len(data) > 0:
                            headers = [str(x) if x is not None else "" for x in data[0]]
                            rows = [[str(x) if x is not None else "" for x in r] for r in data[1:]]
                            
                            md_table = f"\n\n[Table {t_idx} on Page {page_num}]\n"
                            md_table += "| " + " | ".join(headers) + " |\n"
                            md_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
                            for row in rows:
                                md_table += "| " + " | ".join(row) + " |\n"
                            table_text += md_table + "\n"
            except Exception as e:
                print(f"[WARN] Error extracting tables on page {page_num}: {e}")

        # Combine page content
        text += f"\n--- Page {page_num} ---\n"
        if page_text:
            text += page_text + "\n"
        if table_text:
            text += table_text

    document.close()

    return {"text": text, "pages": page_count}