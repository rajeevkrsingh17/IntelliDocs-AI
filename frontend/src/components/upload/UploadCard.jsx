import { useState } from "react";
import { useDropzone } from "react-dropzone";
import {
  UploadCloud,
  Loader2,
  CheckCircle2,
  RefreshCw,
  Lock,
} from "lucide-react";
import { toast } from "sonner";

import { uploadDocuments } from "../../services/api";

export default function UploadCard({ files = [], setFiles }) {
  const [uploading, setUploading] = useState(false);
  const [overallProgress, setOverallProgress] = useState(0);
  const [activeUploads, setActiveUploads] = useState([]);

  const formatSize = (bytes) => {
    const size = Number(bytes) || 0;
    if (size === 0) return "0 KB";
    if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
    return `${(size / (1024 * 1024)).toFixed(2)} MB`;
  };

  const uploadFiles = async (acceptedFiles) => {
    if (!acceptedFiles || !acceptedFiles.length) return;

    setUploading(true);
    setOverallProgress(0);

    const initialUploadItems = acceptedFiles.map((file) => ({
      name: file.name,
      size: file.size,
      extension: file.name.split(".").pop().toUpperCase(),
      status: "uploading",
      progress: 0,
    }));

    setActiveUploads(initialUploadItems);

    try {
      const response = await uploadDocuments(
        acceptedFiles,
        ({ phase, percent }) => {
          setOverallProgress(percent);
          setActiveUploads((prev) =>
            prev.map((item) => ({
              ...item,
              progress: percent,
              status:
                phase === "completed"
                  ? "completed"
                  : phase === "indexing"
                  ? "indexing"
                  : "uploading",
            }))
          );
        }
      );

      const uploaded = response.uploaded || [];

      setFiles((prev) => {
        const updatedList = [...prev];
        uploaded.forEach((item, index) => {
          const matchedFile = acceptedFiles[index];
          const existingIndex = updatedList.findIndex(
            (f) => f.name === item.filename
          );
          const newFileEntry = {
            name: item.filename,
            size: matchedFile?.size || 0,
            type: matchedFile?.type || "",
            lastModified: matchedFile?.lastModified || Date.now(),
            chunks: item.chunks || 0,
            pages: item.pages || 0,
            indexed: true,
          };
          if (existingIndex >= 0) {
            updatedList[existingIndex] = newFileEntry;
          } else {
            updatedList.push(newFileEntry);
          }
        });
        return updatedList;
      });

      setActiveUploads((prev) =>
        prev.map((item) => ({ ...item, progress: 100, status: "completed" }))
      );

      toast.success(
        `${uploaded.length} document(s) indexed successfully!`
      );
    } catch (error) {
      console.error(error);
      toast.error(error.message || "Upload failed.");
    } finally {
      setTimeout(() => {
        setUploading(false);
        setOverallProgress(0);
        setActiveUploads([]);
      }, 1500);
    }
  };


  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
      "text/plain": [".txt"],
      "application/vnd.ms-powerpoint": [".ppt"],
      "application/vnd.openxmlformats-officedocument.presentationml.presentation": [".pptx"],
      "text/markdown": [".md"],
    },
    multiple: true,
    maxSize: 100 * 1024 * 1024,
    onDrop: uploadFiles,
  });

  return (
    <div className="bg-card rounded-2xl border border-border p-5 shadow-[0_2px_8px_rgba(0,0,0,0.02)] transition-all duration-200">
      
      {/* Title & Description */}
      <div className="mb-3">
        <h2 className="text-lg font-bold text-foreground">
          Upload Documents
        </h2>
      </div>

      {/* Dashed Dropzone Box */}
      <div
        {...getRootProps()}
        className={`flex flex-col items-center justify-center text-center p-6 rounded-xl cursor-pointer transition-all duration-200 mb-4 ${
          isDragActive
            ? "border-2 border-dashed border-black dark:border-white bg-secondary/80"
            : "border border-dashed border-border hover:border-foreground/30 bg-card hover:bg-secondary/40"
        }`}
      >
        <input {...getInputProps()} />

        <div className="w-12 h-12 rounded-xl bg-secondary flex items-center justify-center border border-border mb-3 transition-transform duration-200 group-hover:scale-105">
          {uploading ? (
            <Loader2 size={22} className="animate-spin text-foreground" />
          ) : (
            <UploadCloud size={22} className="text-foreground" />
          )}
        </div>

        <p className="text-base font-bold text-foreground">
          {uploading
            ? "Processing documents..."
            : isDragActive
            ? "Drop files here to upload"
            : "Drag & drop files here, or click to browse"}
        </p>

        <p className="text-sm text-muted-foreground mt-1.5">
          Supports PDF, DOCX, PPTX, TXT, MD
        </p>

        <p className="text-xs text-muted-foreground/80 mt-0.5">
          Maximum 100 MB per file
        </p>

        <div className="flex items-center gap-1.5 text-xs text-muted-foreground mt-3 pt-3 border-t border-border/50 w-full justify-center">
          <Lock size={12} className="text-muted-foreground" />
          <span>Files are securely indexed and never shared</span>
        </div>
      </div>

      {/* Document Count and Names */}
      {files.length > 0 && (
        <div className="p-4 rounded-xl bg-secondary/30 border border-border">
          <p className="text-sm font-semibold text-foreground mb-1">
            {files.length} {files.length === 1 ? "Document" : "Documents"} Indexed:
          </p>
          <div className="flex flex-col gap-2 mt-3">
            {files.map((f, i) => {
              const ext = f.name ? f.name.split(".").pop().toUpperCase() : "FILE";
              return (
                <div key={i} className="flex items-center gap-3 bg-card border border-border px-3 py-2 rounded-lg shadow-sm">
                  <span className="flex items-center justify-center w-5 h-5 rounded-full bg-secondary text-xs font-bold text-muted-foreground shrink-0">
                    {i + 1}
                  </span>
                  <span className="px-1.5 py-0.5 rounded text-[10px] font-bold tracking-wider bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 border border-blue-200 dark:border-blue-800 shrink-0">
                    {ext}
                  </span>
                  <span className="text-sm font-medium text-foreground truncate" title={f.name}>
                    {f.name}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Active Uploads / Indexing Status */}
      {activeUploads.length > 0 && (
        <div className="mt-4 border border-border rounded-xl bg-secondary/30 p-3 space-y-2">
          <div className="flex justify-between items-center text-sm font-semibold text-foreground">
            <span className="flex items-center gap-2">
              <Loader2 size={13} className="animate-spin text-foreground" />
              Processing {activeUploads.length} file(s)
            </span>
            <span className="font-mono text-sm">{overallProgress}%</span>
          </div>

          {activeUploads.map((file, idx) => (
            <div
              key={idx}
              className="bg-card border border-border rounded-lg p-2.5 flex flex-col gap-1.5"
            >
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="px-1.5 py-0.2 rounded bg-secondary font-mono text-xs border border-border">
                    {file.extension}
                  </span>
                  <span className="font-medium text-foreground truncate max-w-[220px]">
                    {file.name}
                  </span>
                  <span className="text-muted-foreground text-xs">
                    ({formatSize(file.size)})
                  </span>
                </div>

                <div className="shrink-0">
                  {file.status === "completed" ? (
                    <span className="flex items-center gap-1 text-emerald-600 font-semibold text-xs">
                      <CheckCircle2 size={12} /> Ready
                    </span>
                  ) : file.status === "indexing" ? (
                    <span className="flex items-center gap-1 text-purple-600 font-semibold text-xs">
                      <RefreshCw size={12} className="animate-spin" /> Indexing
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-foreground font-semibold text-xs">
                      <Loader2 size={12} className="animate-spin" /> Uploading
                    </span>
                  )}
                </div>
              </div>

              <div className="w-full h-1 rounded-full bg-muted overflow-hidden">
                <div
                  className={`h-full transition-all duration-200 ${
                    file.status === "completed"
                      ? "bg-emerald-500"
                      : file.status === "indexing"
                      ? "bg-purple-500"
                      : "bg-black dark:bg-white"
                  }`}
                  style={{ width: `${file.status === "completed" ? 100 : file.progress}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}