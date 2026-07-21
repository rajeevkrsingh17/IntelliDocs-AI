import sys
from pathlib import Path

# Add root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scripts.vector_store import process_document, clear_database, delete_document_from_db, get_all_documents
from scripts.search import retrieve_relevant_chunks, retrieve_multiple_documents
from scripts.llm import generate_answer, generate_document_comparison

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
    ".ppt",
    ".pptx",
    ".md",
}

app = FastAPI(
    title="IntelliDocs AI API",
    description="Multi-Document RAG using Gemini",
    version="2.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str
    document_name: str | None = None


class CompareRequest(BaseModel):
    documents: list[str]
    comparison_type: str = "detailed"
    custom_prompt: str | None = None


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "IntelliDocs AI Backend Running",
    }


@app.get("/documents")
def list_documents():
    return get_all_documents()


@app.post("/upload")
async def upload_documents(files: list[UploadFile] = File(...)):
    uploaded = []

    for file in files:
        if not file.filename:
            continue

        extension = Path(file.filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} has unsupported file type.",
            )

        save_path = UPLOAD_DIR / file.filename

        # Read file content and save to disk
        content = await file.read()
        with open(save_path, "wb") as buffer:
            buffer.write(content)

        # Process and index the document
        result = process_document(save_path)

        uploaded.append(
            {
                "filename": file.filename,
                "file_type": extension.replace(".", "").upper(),
                "chunks": result["chunks"],
                "pages": result["pages"],
            }
        )

    return {
        "status": "success",
        "uploaded": uploaded,
        "total_documents": len(uploaded),
    }


@app.post("/query")
def ask_question(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    retrieved = retrieve_relevant_chunks(
        query=request.question,
        n_results=10,
        document_name=request.document_name,
    )

    documents = retrieved["documents"]
    metadata = retrieved["metadata"]

    if not documents:
        return {
            "answer": "No relevant information found.",
            "sources": [],
        }

    context_parts = []
    total_chunks = len(documents)
    context_parts.append(
        f"[{total_chunks} relevant chunks retrieved — ranked by relevance]\n"
    )
    for idx, (doc, meta) in enumerate(zip(documents, metadata), start=1):
        doc_name = meta.get("document_name", "Document")
        page_num = meta.get("page", 1)
        chunk_num = meta.get("chunk", 1)
        context_parts.append(
            f"═══ Chunk {idx}/{total_chunks} | {doc_name} | Page {page_num} | Chunk {chunk_num} ═══\n{doc}"
        )

    context = "\n\n".join(context_parts)

    answer = generate_answer(
        question=request.question,
        context=context,
    )

    # Build structured source objects, de-duplicated by (document_name, page)
    seen = {}
    for item in metadata:
        doc_name = item.get("document_name", "Unknown")
        page = item.get("page")
        chunk = item.get("chunk")
        key = (doc_name, page)

        if key not in seen:
            seen[key] = {
                "document_name": doc_name,
                "page": page,
                "chunks": [chunk],
            }
        else:
            if chunk not in seen[key]["chunks"]:
                seen[key]["chunks"].append(chunk)

    sources = list(seen.values())

    return {
        "answer": answer,
        "sources": sources,
    }


@app.post("/compare")
def compare_documents(request: CompareRequest):

    if len(request.documents) < 2:
        raise HTTPException(
            status_code=400,
            detail="Please select at least two documents.",
        )

    docs = retrieve_multiple_documents(request.documents)

    if len(docs) < 2:
        found_names = [d["name"] for d in docs]
        missing = [d for d in request.documents if d not in found_names]
        raise HTTPException(
            status_code=404,
            detail=f"Could not retrieve content for comparison. Missing or empty: {', '.join(missing)}.",
        )

    comparison = generate_document_comparison(
        documents=docs,
        comparison_type=request.comparison_type,
        custom_prompt=request.custom_prompt,
    )

    return {
        "comparison": comparison,
        "documents": request.documents,
        "comparison_type": request.comparison_type,
        "custom_prompt": request.custom_prompt,
    }


@app.delete("/documents/{filename}")
def delete_document(filename: str):
    success = delete_document_from_db(filename)
    if not success:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete {filename} from vector database.",
        )
    return {
        "status": "success",
        "message": f"Successfully deleted {filename}",
    }


@app.post("/clear")
def clear_all_documents():
    clear_database()
    return {
        "status": "success",
        "message": "All documents cleared from vector database.",
    }