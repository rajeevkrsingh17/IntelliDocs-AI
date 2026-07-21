import { useContext } from "react";
import {
  GitCompare,
  FileText,
  Sparkles,
  Loader2,
  CheckCircle2,
  Copy,
  Download,
  FileJson,
} from "lucide-react";
import { ToastContext } from "../../context/ToastContext";
import MarkdownRenderer from "../ui/MarkdownRenderer";

export default function CompareResult({
  result,
  loading,
  documents = [],
}) {
  const { showToast } = useContext(ToastContext);

  const copyComparison = async () => {
    if (!result) return;
    try {
      await navigator.clipboard.writeText(result);
      if (showToast) showToast("✓ Copied comparison to clipboard", "success");
    } catch (err) {
      if (showToast) showToast("Failed to copy comparison", "error");
    }
  };

  const downloadComparison = (format) => {
    if (!result) return;

    let content = result;
    let filename = `intellidocs-comparison-${new Date().getTime()}`;
    let mimeType = "text/plain";

    if (format === "txt") {
      content = `DOCUMENT COMPARISON\n${"=".repeat(50)}\n\nDocuments: ${documents.join(", ")}\n\n${result}`;
      filename += ".txt";
      mimeType = "text/plain";
    } else if (format === "markdown") {
      content = `# Document Comparison\n\n## Documents Compared\n${documents
        .map((d) => `- ${d}`)
        .join("\n")}\n\n## Comparison Result\n\n${result}`;
      filename += ".md";
      mimeType = "text/markdown";
    } else if (format === "json") {
      content = JSON.stringify(
        {
          documents,
          comparison: result,
          generatedAt: new Date().toISOString(),
        },
        null,
        2
      );
      filename += ".json";
      mimeType = "application/json";
    }

    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    if (showToast) showToast(`Downloaded as ${format.toUpperCase()}`, "success");
  };

  if (!loading && !result) {
    return null;
  }

  return (
    <div className="bg-card rounded-2xl border border-border shadow-[0_2px_8px_rgba(0,0,0,0.02)] overflow-hidden transition-all duration-200">

      {/* Header */}
      <div className="flex items-center justify-between border-b border-border px-6 py-4 bg-card">

        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-black dark:bg-white text-white dark:text-black flex items-center justify-center shadow-sm">
            <GitCompare size={16} strokeWidth={2.2} />
          </div>

          <div>
            <h2 className="font-bold text-base text-foreground">
              Comparison Results
            </h2>
            <p className="text-xs text-muted-foreground font-normal">
              AI-generated multi-document synthesis
            </p>
          </div>
        </div>

        {/* Toolbar */}
        <div className="flex items-center gap-1">
          <button
            onClick={copyComparison}
            disabled={!result}
            className="p-1.5 rounded-lg border border-border bg-card hover:bg-secondary text-muted-foreground hover:text-foreground transition text-sm disabled:opacity-40"
            title="Copy Comparison"
          >
            <Copy size={14} />
          </button>

          {/* Download Dropdown */}
          <div className="relative group">
            <button
              disabled={!result}
              className="p-1.5 rounded-lg border border-border bg-card hover:bg-secondary text-muted-foreground hover:text-foreground transition text-sm disabled:opacity-40"
              title="Download Comparison"
            >
              <Download size={14} />
            </button>
            <div className="absolute right-0 mt-1 w-36 bg-card border border-border rounded-xl shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-150 z-20 p-1">
              <button
                onClick={() => downloadComparison("txt")}
                className="w-full text-left px-3 py-1.5 hover:bg-secondary rounded-lg flex items-center gap-2 text-sm font-medium text-foreground"
              >
                <FileText size={14} />
                Text (.txt)
              </button>
              <button
                onClick={() => downloadComparison("markdown")}
                className="w-full text-left px-3 py-1.5 hover:bg-secondary rounded-lg flex items-center gap-2 text-sm font-medium text-foreground"
              >
                <FileText size={14} />
                Markdown (.md)
              </button>
              <button
                onClick={() => downloadComparison("json")}
                className="w-full text-left px-3 py-1.5 hover:bg-secondary rounded-lg flex items-center gap-2 text-sm font-medium text-foreground"
              >
                <FileJson size={14} />
                JSON (.json)
              </button>
            </div>
          </div>
        </div>

      </div>

      {/* Selected Document Pills */}
      {documents.length > 0 && (
        <div className="px-6 py-3 border-b border-border bg-secondary/20 flex items-center gap-2">
          <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Compared:
          </span>
          <div className="flex flex-wrap gap-2">
            {documents.map((doc, index) => (
              <span
                key={index}
                className="px-2.5 py-0.5 rounded-md bg-card border border-border text-foreground text-xs font-medium flex items-center gap-1 shadow-sm"
              >
                📄 {doc}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Body */}
      <div className="p-6">

        {loading ? (
          <div className="flex items-center justify-center gap-3 text-muted-foreground py-10">
            <Loader2 size={20} className="animate-spin text-foreground" />
            <span className="text-sm font-medium">
              Comparing documents and structuring insights...
            </span>
          </div>
        ) : result ? (
          <div className="rounded-xl border border-border bg-card p-5">
            <div className="flex items-center gap-2 mb-3 pb-3 border-b border-border/60">
              <Sparkles size={16} className="text-foreground" />
              <h3 className="font-bold text-sm text-foreground uppercase tracking-wider">
                Synthesis &amp; Comparison Report
              </h3>
            </div>
            <MarkdownRenderer content={result} />
          </div>
        ) : null}

      </div>

      {/* Footer */}
      <div className="border-t border-border px-6 py-3 bg-secondary/20 flex items-center justify-between text-xs text-muted-foreground">
        <div className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400 font-semibold">
          <CheckCircle2 size={13} />
          <span>Powered by RAG Vector Retrieval + AI Reasoning</span>
        </div>
        <span className="font-mono text-xs">Comparison Complete</span>
      </div>

    </div>
  );
}