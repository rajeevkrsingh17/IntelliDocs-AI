import sys
import uuid
import threading
from pathlib import Path
from typing import Dict, Any

# Add root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from scripts.vector_store import process_document, clear_database, delete_document_from_db, get_all_documents
from scripts.search import retrieve_relevant_chunks, retrieve_multiple_documents
from scripts.llm import generate_answer, generate_document_comparison

BASE_DIR = Path(__file__).resolve().parent.parent
import os as _os
_IS_CLOUD = bool(_os.getenv("RENDER"))
UPLOAD_DIR = Path("/tmp/uploads") if _IS_CLOUD else BASE_DIR / "data" / "uploads"
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

# ──────────────────────────────────────────────
# In-memory job store for background uploads
# ──────────────────────────────────────────────
_upload_jobs: Dict[str, Dict[str, Any]] = {}

app = FastAPI(
    title="IntelliDocs AI API",
    description="Multi-Document RAG using Gemini",
    version="2.3.0",
)

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    # Handle preflight OPTIONS requests directly
    if request.method == "OPTIONS":
        response = JSONResponse(status_code=200, content={})
    else:
        try:
            response = await call_next(request)
        except Exception as exc:
            # Fallback in case exception handler doesn't catch it
            response = JSONResponse(status_code=500, content={"detail": str(exc)})
        
    origin = request.headers.get("Origin") or request.headers.get("origin") or "*"
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Max-Age"] = "86400"  # Cache preflight for 24 hours
    return response



# Catch-all exception handler — ensures CORS headers are ALWAYS present
# even when the server crashes with an unhandled 500 error.
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    origin = request.headers.get("origin", "*")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )


from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    origin = request.headers.get("origin", "*")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    origin = request.headers.get("origin", "*")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
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
def list_documents(x_session_id: str | None = Header(None)):
    return get_all_documents(session_id=x_session_id)


# ──────────────────────────────────────────────
# UPLOAD — saves files immediately, processes
# in a background thread, returns a job_id.
# This avoids Render's 30-second HTTP timeout.
# ──────────────────────────────────────────────

@app.post("/upload")
async def upload_documents(
    background_tasks: BackgroundTasks,
    files: list[UploadFile] = File(...),
    x_session_id: str | None = Header(None),
):
    saved: list[tuple[str, str, Path]] = []

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

        # Read and persist to disk immediately
        content = await file.read()
        with open(save_path, "wb") as buffer:
            buffer.write(content)

        saved.append((file.filename, extension, save_path))

    if not saved:
        raise HTTPException(status_code=400, detail="No valid files provided.")

    # Create a job record
    job_id = str(uuid.uuid4())
    _upload_jobs[job_id] = {
        "status": "processing",
        "progress": 0,
        "processed": 0,
        "total": len(saved),
        "uploaded": [],
        "error": None,
    }

    # Capture session_id for the thread closure
    session = x_session_id

    def _process():
        """Background worker — runs outside the HTTP request lifecycle."""
        for idx, (filename, extension, save_path) in enumerate(saved):
            try:
                result = process_document(save_path, session_id=session)
                _upload_jobs[job_id]["uploaded"].append(
                    {
                        "filename": filename,
                        "file_type": extension.replace(".", "").upper(),
                        "chunks": result["chunks"],
                        "pages": result["pages"],
                    }
                )
            except Exception as exc:
                _upload_jobs[job_id]["status"] = "failed"
                _upload_jobs[job_id]["error"] = str(exc)
                return

            _upload_jobs[job_id]["processed"] = idx + 1
            _upload_jobs[job_id]["progress"] = int((idx + 1) / len(saved) * 100)

        _upload_jobs[job_id]["status"] = "completed"

    background_tasks.add_task(_process)

    # Return immediately — client must poll /upload/status/{job_id}
    return {
        "job_id": job_id,
        "status": "processing",
        "total": len(saved),
    }


@app.get("/upload/status/{job_id}")
def get_upload_status(job_id: str):
    """
    Poll this endpoint after calling POST /upload.
    Returns:
      - {"status": "processing", "progress": 0-99, ...}
      - {"status": "completed", "uploaded": [...], ...}
      - HTTP 500 on processing failure
    """
    job = _upload_jobs.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")

    if job["status"] == "failed":
        raise HTTPException(
            status_code=500,
            detail=job.get("error") or "Document processing failed.",
        )

    if job["status"] == "completed":
        return {
            "status": "completed",
            "uploaded": job["uploaded"],
            "total_documents": len(job["uploaded"]),
            "progress": 100,
        }

    return {
        "status": "processing",
        "progress": job["progress"],
        "processed": job["processed"],
        "total": job["total"],
    }


@app.post("/query")
def ask_question(request: QueryRequest, x_session_id: str | None = Header(None)):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    retrieved = retrieve_relevant_chunks(
        query=request.question,
        n_results=10,
        document_name=request.document_name,
        session_id=x_session_id,
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
def compare_documents(request: CompareRequest, x_session_id: str | None = Header(None)):

    if len(request.documents) < 2:
        raise HTTPException(
            status_code=400,
            detail="Please select at least two documents.",
        )

    docs = retrieve_multiple_documents(request.documents, session_id=x_session_id)

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
def delete_document(filename: str, x_session_id: str | None = Header(None)):
    success = delete_document_from_db(filename, session_id=x_session_id)
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
def clear_all_documents(x_session_id: str | None = Header(None)):
    clear_database(session_id=x_session_id)
    return {
        "status": "success",
        "message": "All documents cleared from vector database.",
    }