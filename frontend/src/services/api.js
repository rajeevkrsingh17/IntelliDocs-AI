import axios from "axios";

// In production (Vercel), requests to /api/* are proxied to Render via vercel.json rewrites.
// In local dev, Vite proxies /api/* to http://127.0.0.1:8000 via vite.config.js.
// This means ALL requests are same-origin → CORS is completely eliminated.
const API_URL = "/api";

// Persistent Session ID generator per browser/device
function getSessionId() {
  let sid = localStorage.getItem("intellidocs_session_id");
  if (!sid) {
    sid = "sess_" + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    localStorage.setItem("intellidocs_session_id", sid);
  }
  return sid;
}

const api = axios.create({
  baseURL: API_URL,
});

// Attach X-Session-ID header to every request
api.interceptors.request.use((config) => {
  config.headers["X-Session-ID"] = getSessionId();
  return config;
});


/**
 * Upload multiple documents.
 *
 * Phase 1 — HTTP transfer: progress 0→99 (phase: "uploading")
 * Phase 2 — Backend indexing: progress 0→99 (phase: "indexing")
 * Done     — progress 100 (phase: "completed")
 *
 * onProgress receives: { phase: "uploading"|"indexing"|"completed", percent: 0-100 }
 */
export async function uploadDocuments(files, onProgress = () => {}) {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append("files", file);
  });

  try {
    // ── Phase 1: transfer bytes to server ──────────────────────────────────
    const uploadRes = await api.post("/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
      onUploadProgress: (event) => {
        if (!event.total) return;
        // Cap at 99 so the bar never shows 100% until indexing is also done
        const pct = Math.min(99, Math.round((event.loaded * 100) / event.total));
        onProgress({ phase: "uploading", percent: pct });
      },
    });

    const { job_id } = uploadRes.data;

    // ── Phase 2: poll the background indexing job ──────────────────────────
    onProgress({ phase: "indexing", percent: 0 });

    const POLL_INTERVAL_MS = 3000;   // poll every 3 s
    const MAX_WAIT_MS = 10 * 60 * 1000; // give up after 10 minutes
    const startedAt = Date.now();

    while (Date.now() - startedAt < MAX_WAIT_MS) {
      await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL_MS));

      const statusRes = await api.get(`/upload/status/${job_id}`);
      const data = statusRes.data;

      if (data.status === "completed") {
        onProgress({ phase: "completed", percent: 100 });
        return data; // { status, uploaded, total_documents, progress }
      }

      // Still processing — report progress so the bar moves
      onProgress({ phase: "indexing", percent: data.progress ?? 0 });
    }

    throw new Error(
      "Document indexing is taking longer than expected. " +
      "It will complete in the background — please refresh the Documents tab in a minute."
    );
  } catch (error) {
    throw new Error(
      error.response?.data?.detail ||
      error.message ||
      "Failed to upload documents."
    );
  }
}

/**
 * Ask a question.
 */
export async function askQuestion(question, documentName = null) {
  try {
    const response = await api.post("/query", {
      question,
      document_name: documentName,
    });

    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail ||
      "Failed to generate answer."
    );
  }
}

/**
 * Compare two or more uploaded documents.
 */
export async function compareDocuments({
  documents,
  comparisonType = "detailed",
  customPrompt = null,
}) {
  try {
    const response = await api.post("/compare", {
      documents,
      comparison_type: comparisonType,
      custom_prompt: customPrompt,
    });

    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail ||
      "Failed to compare documents."
    );
  }
}

/**
 * Delete a single document from the vector store.
 */
export async function deleteDocument(filename) {
  try {
    const response = await api.delete(`/documents/${encodeURIComponent(filename)}`);
    return response.data;
  } catch (error) {
    console.error("Failed to delete document:", error);
  }
}

/**
 * Clear all documents from the vector store.
 */
export async function clearAllDocuments() {
  try {
    const response = await api.post("/clear");
    return response.data;
  } catch (error) {
    console.error("Failed to clear documents:", error);
  }
}

/**
 * Get all indexed documents.
 */
export async function getDocuments() {
  try {
    const response = await api.get("/documents");
    return response.data;
  } catch (error) {
    console.error("Failed to get documents:", error);
    return [];
  }
}

export default api;