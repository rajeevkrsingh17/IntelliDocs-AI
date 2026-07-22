import fitz  # PyMuPDF
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent

def create_resume_pdf():
    # Page dimensions: A4 (595 x 842 points)
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    
    # Title / Header (Dark slate blue theme)
    # Background Accent for header
    page.draw_rect(fitz.Rect(0, 0, 595, 110), color=(0.12, 0.17, 0.28), fill=(0.12, 0.17, 0.28))
    
    # Text insertion
    # Name
    page.insert_text(fitz.Point(40, 45), "RAJEEV KUMAR", fontsize=24, color=(1, 1, 1), fontname="hebo")
    # Subtitle
    page.insert_text(fitz.Point(40, 68), "B.Tech CSE (Artificial Intelligence & Data Engineering)", fontsize=10, color=(0.8, 0.85, 0.9), fontname="helv")
    # Contact info
    contact_text = "Email: rajeevkrsingh17@gmail.com | GitHub: github.com/rajeevkrsingh17"
    page.insert_text(fitz.Point(40, 88), contact_text, fontsize=9.5, color=(0.8, 0.85, 0.9), fontname="hebo")
    
    # Section helper
    def draw_section_header(y_pos, title):
        page.draw_line(fitz.Point(40, y_pos), fitz.Point(555, y_pos), color=(0.12, 0.17, 0.28), width=1.5)
        page.draw_rect(fitz.Rect(40, y_pos - 18, 140, y_pos), color=(0.12, 0.17, 0.28), fill=(0.12, 0.17, 0.28))
        page.insert_text(fitz.Point(48, y_pos - 5), title.upper(), fontsize=10, color=(1, 1, 1), fontname="hebo")
        return y_pos + 18

    # 1. Education Section
    y = draw_section_header(150, "Education")
    page.insert_text(fitz.Point(40, y), "B.Tech in Computer Science & Engineering (AI & Data Engineering)", fontsize=11, color=(0.1, 0.1, 0.1), fontname="hebo")
    page.insert_text(fitz.Point(40, y + 15), "Lovely Professional University | Expected Graduation: 2028", fontsize=9.5, color=(0.3, 0.3, 0.3), fontname="helv")
    
    # 2. Projects Section
    y = draw_section_header(210, "Projects")
    page.insert_text(fitz.Point(40, y), "IntelliDocs-AI — AI-Powered Document Q&A System (RAG)", fontsize=11, color=(0.1, 0.1, 0.1), fontname="hebo")
    page.insert_text(fitz.Point(40, y + 15), "Python · PyMuPDF · Gemini Embeddings · ChromaDB · Rank-BM25 · FastAPI · Streamlit · React", fontsize=8.5, color=(0.12, 0.17, 0.28), fontname="hebo")
    page.insert_text(fitz.Point(470, y), "June – July 2026", fontsize=9, color=(0.4, 0.4, 0.4), fontname="helv")
    
    bullets = [
        "Engineered an end-to-end RAG Document Q&A platform using Python, PyMuPDF, Google Gemini API (gemini-embedding-001), ChromaDB, and Rank-BM25, enabling hybrid vector & sparse semantic search over PDF documents with chunk-level source citations.",
        "Implemented Reciprocal Rank Fusion (RRF k=60) & resilient LLM fallback architecture cascading across Google Gemini model tiers (gemini-3.1-flash-lite -> gemini-2.0-flash -> gemini-1.5-flash -> mock) with automated retry logic, achieving 100% service uptime during API rate-limit spikes.",
        "Built a multi-document comparative analysis engine & dual user interface in Streamlit and React (Vite + TailwindCSS) backed by a FastAPI REST API, supporting side-by-side cross-document topic comparison and structural summarization across PDF corpora."
    ]
    
    bullet_y = y + 32
    for b in bullets:
        # Wrap text manually
        words = b.split()
        lines = []
        current_line = []
        for w in words:
            test_line = " ".join(current_line + [w])
            # Check if line fits within 500pt width
            if page.rect.width - 120 < fitz.get_text_length(test_line, fontsize=9.5, fontname="helv"):
                lines.append(" ".join(current_line))
                current_line = [w]
            else:
                current_line.append(w)
        if current_line:
            lines.append(" ".join(current_line))
            
        # Draw bullet point
        page.insert_text(fitz.Point(40, bullet_y), "-", fontsize=12, color=(0.12, 0.17, 0.28), fontname="hebo")
        for line in lines:
            page.insert_text(fitz.Point(52, bullet_y), line, fontsize=9.5, color=(0.15, 0.15, 0.15), fontname="helv")
            bullet_y += 13
        bullet_y += 5

    # 3. Technical Skills
    y = draw_section_header(bullet_y + 10, "Technical Skills")
    skills = [
        ("Languages", "Python, SQL, JavaScript"),
        ("ML & NLP", "Sentence Transformers (all-MiniLM-L6-v2), PyTorch (intro), Scikit-learn"),
        ("LLM & GenAI", "Google Gemini API, RAG Architecture, Hybrid Search (Dense + BM25 RRF), Prompt Eng."),
        ("Databases", "ChromaDB (Local HNSW), PostgreSQL"),
        ("Web & Backend", "FastAPI, Uvicorn, Streamlit, React, Vite, TailwindCSS"),
        ("Tools & Testing", "Git, GitHub, Docker (intro), Pytest (10 test suites passed)"),
        ("Concepts", "Retrieval-Augmented Generation, Vector Embeddings, Cosine Similarity, Reciprocal Rank Fusion")
    ]
    for category, items in skills:
        page.insert_text(fitz.Point(40, y), f"{category}:", fontsize=9.5, color=(0.12, 0.17, 0.28), fontname="hebo")
        page.insert_text(fitz.Point(140, y), items, fontsize=9.5, color=(0.15, 0.15, 0.15), fontname="helv")
        y += 14

    # 4. Certifications & Internships
    y = draw_section_header(y + 10, "Certifications & Internships")
    page.insert_text(fitz.Point(40, y), "Summer Internship 2026 — Foundations of Applied Machine Learning", fontsize=10.5, color=(0.1, 0.1, 0.1), fontname="hebo")
    page.insert_text(fitz.Point(40, y + 13), "Lovely Professional University | June – July 2026", fontsize=9.5, color=(0.3, 0.3, 0.3), fontname="helv")
    page.insert_text(fitz.Point(40, y + 26), "Problem Statement: I2 – Document Q&A (RAG over a Focused Corpus)", fontsize=9.5, color=(0.15, 0.15, 0.15), fontname="helv")

    # Save
    doc.save(DOCS_DIR / "resume_final.pdf")
    doc.close()
    print("Created docs/resume_final.pdf")

def create_showcase_slide_pdf():
    # Landscape orientation: US Letter (792 x 612 points)
    doc = fitz.open()
    page = doc.new_page(width=792, height=612)
    
    # Elegant Dark Background (Midnight Navy)
    page.draw_rect(fitz.Rect(0, 0, 792, 612), color=(0.08, 0.11, 0.18), fill=(0.08, 0.11, 0.18))
    
    # Title header
    page.insert_text(fitz.Point(50, 60), "INTELLIDOCS-AI", fontsize=28, color=(0.38, 0.69, 0.95), fontname="hebo")
    page.insert_text(fitz.Point(50, 90), "Resilient, Hybrid RAG Document Q&A System", fontsize=16, color=(1, 1, 1), fontname="hebo")
    
    # Grid lines / borders
    page.draw_line(fitz.Point(50, 110), fitz.Point(742, 110), color=(0.38, 0.69, 0.95), width=1.5)
    
    # Left Column: Problem & Key Metrics
    page.draw_rect(fitz.Rect(50, 140, 380, 540), color=(0.12, 0.17, 0.28), fill=(0.12, 0.17, 0.28))
    page.insert_text(fitz.Point(70, 170), "THE PROBLEM", fontsize=13, color=(0.38, 0.69, 0.95), fontname="hebo")
    
    prob_bullets = [
        "LLMs hallucinate when asked about private files.",
        "Simple Vector Search misses exact numeric values, codes & acronyms.",
        "RAG servers easily crash under free-tier memory (512MB RAM) and LLM API rate limits (HTTP 429)."
    ]
    y_prob = 195
    for bullet in prob_bullets:
        words = bullet.split()
        lines = []
        current = []
        for w in words:
            test = " ".join(current + [w])
            if fitz.get_text_length(test, fontsize=9.5, fontname="helv") > 280:
                lines.append(" ".join(current))
                current = [w]
            else:
                current.append(w)
        if current:
            lines.append(" ".join(current))
        page.insert_text(fitz.Point(70, y_prob), ">", fontsize=11, color=(0.89, 0.45, 0.45), fontname="hebo")
        for line in lines:
            page.insert_text(fitz.Point(82, y_prob), line, fontsize=9.5, color=(0.9, 0.9, 0.9), fontname="helv")
            y_prob += 13
        y_prob += 5

    # Key Achievement Highlight (glowing box)
    page.draw_rect(fitz.Rect(70, y_prob + 10, 360, y_prob + 120), color=(0.15, 0.27, 0.4), fill=(0.15, 0.23, 0.35), width=1)
    page.insert_text(fitz.Point(85, y_prob + 32), "KEY ACHIEVEMENT:", fontsize=11, color=(0.4, 0.85, 0.5), fontname="hebo")
    ach_text1 = "Reduced RAM footprint from ~800MB"
    ach_text2 = "to ~150MB, enabling free deployment"
    ach_text3 = "on Render while keeping Hybrid Search"
    page.insert_text(fitz.Point(85, y_prob + 52), ach_text1, fontsize=10, color=(1, 1, 1), fontname="hebo")
    page.insert_text(fitz.Point(85, y_prob + 70), ach_text2, fontsize=10, color=(1, 1, 1), fontname="hebo")
    page.insert_text(fitz.Point(85, y_prob + 88), ach_text3, fontsize=10, color=(1, 1, 1), fontname="hebo")

    # Right Column: The Solution & Tech Stack
    page.draw_rect(fitz.Rect(410, 140, 742, 540), color=(0.12, 0.17, 0.28), fill=(0.12, 0.17, 0.28))
    page.insert_text(fitz.Point(430, 170), "THE RAG SOLUTION", fontsize=13, color=(0.38, 0.69, 0.95), fontname="hebo")
    
    sol_bullets = [
        "Hybrid Retrievals: ChromaDB (HNSW Dense) + Rank-BM25 (Sparse) merged via RRF (k=60).",
        "Resilient Failover Cascade: Graceful degradation from Gemini 2.0 -> 1.5 -> local mock summaries.",
        "Multi-Document Compare: Unified side-by-side analysis."
    ]
    y_sol = 195
    for bullet in sol_bullets:
        words = bullet.split()
        lines = []
        current = []
        for w in words:
            test = " ".join(current + [w])
            if fitz.get_text_length(test, fontsize=9.5, fontname="helv") > 280:
                lines.append(" ".join(current))
                current = [w]
            else:
                current.append(w)
        if current:
            lines.append(" ".join(current))
        page.insert_text(fitz.Point(430, y_sol), "v", fontsize=11, color=(0.4, 0.85, 0.5), fontname="hebo")
        for line in lines:
            page.insert_text(fitz.Point(445, y_sol), line, fontsize=9.5, color=(0.9, 0.9, 0.9), fontname="helv")
            y_sol += 13
        y_sol += 5

    # Tech Stack Table Drawing
    page.insert_text(fitz.Point(430, y_sol + 10), "PRODUCTION TECH STACK", fontsize=11, color=(0.38, 0.69, 0.95), fontname="hebo")
    stack_y = y_sol + 28
    techs = [
        ("Frontend", "React 19, Vite, Tailwind CSS"),
        ("Backend API", "FastAPI, Uvicorn, Python 3.12"),
        ("Embeddings", "Google Gemini gemini-embedding-001"),
        ("Vector DB", "ChromaDB (Persistent HNSW)"),
        ("Sparse Match", "Okapi Rank-BM25"),
        ("Synthesis / LLM", "Google Gemini Flash Cascade"),
        ("Validation", "Pytest Suite (10 Passed Tests)")
    ]
    for layer, tech in techs:
        page.insert_text(fitz.Point(430, stack_y), layer, fontsize=9.5, color=(0.7, 0.7, 0.7), fontname="hebo")
        page.insert_text(fitz.Point(540, stack_y), tech, fontsize=9.5, color=(1, 1, 1), fontname="helv")
        stack_y += 14

    # Footer
    page.insert_text(fitz.Point(50, 570), "Rajeev Kumar | B.Tech CSE (Lovely Professional University)", fontsize=9.5, color=(0.5, 0.6, 0.7), fontname="helv")
    page.insert_text(fitz.Point(50, 583), "Foundations of Applied Machine Learning - Summer 2026", fontsize=9.5, color=(0.5, 0.6, 0.7), fontname="helv")
    page.insert_text(fitz.Point(520, 570), "Vercel: intellidocs-ai-tau.vercel.app", fontsize=9, color=(0.38, 0.69, 0.95), fontname="helv")
    page.insert_text(fitz.Point(520, 583), "Render: intellidocs-api-yedx.onrender.com", fontsize=9, color=(0.38, 0.69, 0.95), fontname="helv")

    # Save
    doc.save(DOCS_DIR / "showcase_slide.pdf")
    doc.close()
    print("Created docs/showcase_slide.pdf")

if __name__ == "__main__":
    create_resume_pdf()
    create_showcase_slide_pdf()
