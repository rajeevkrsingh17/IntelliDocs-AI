import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_URL,
});

/**
 * Upload multiple documents.
 *
 * Supports:
 * - PDF
 * - DOCX
 * - TXT
 * - PPT
 * - PPTX
 * - MD
 */
export async function uploadDocuments(files, onProgress = () => {}) {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  try {
    const response = await api.post("/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },

      onUploadProgress: (event) => {
        if (!event.total) return;

        const progress = Math.round(
          (event.loaded * 100) / event.total
        );

        onProgress(progress);
      },
    });

    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail ||
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