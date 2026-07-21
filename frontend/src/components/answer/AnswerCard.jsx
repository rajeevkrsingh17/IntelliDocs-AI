import { useContext } from "react";
import {
  Copy,
  ThumbsUp,
  ThumbsDown,
  Clock,
  Sparkles,
  ShieldCheck,
  Loader2,
  User,
  Download,
  FileText,
  FileJson,
  FileText as FileTxt,
} from "lucide-react";
import { ToastContext } from "../../context/ToastContext";
import MarkdownRenderer from "../ui/MarkdownRenderer";
import SourceCitations from "../ui/SourceCitations";

export default function AnswerCard({
  question,
  answer,
  sources,
  loading,
}) {
  const { showToast } = useContext(ToastContext);

  const copyAnswer = async () => {
    if (!answer) return;
    try {
      await navigator.clipboard.writeText(answer);
      if (showToast) showToast("✓ Copied answer to clipboard", "success");
    } catch (err) {
      if (showToast) showToast("Failed to copy answer", "error");
    }
  };

  const downloadAnswer = (format) => {
    if (!answer) return;

    let content = answer;
    let filename = `intellidocs-answer-${new Date().getTime()}`;
    let mimeType = "text/plain";

    if (format === "txt") {
      content = answer;
      filename += ".txt";
      mimeType = "text/plain";
    } else if (format === "markdown") {
      content = `# AI Generated Answer\n\n${answer}\n\n## Sources\n${
        sources?.map((s) => `- ${typeof s === 'string' ? s : s.document_name}`).join("\n") || "No sources"
      }`;
      filename += ".md";
      mimeType = "text/markdown";
    } else if (format === "json") {
      content = JSON.stringify(
        {
          question,
          answer,
          sources,
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

  if (!loading && !answer && !question) {
    return null;
  }

  return (
    <div className="bg-card rounded-2xl border border-border shadow-[0_2px_8px_rgba(0,0,0,0.02)] overflow-hidden transition-all duration-200 h-full flex flex-col">

      {/* Header */}
      <div className="flex flex-wrap items-center justify-between border-b border-border px-6 py-4 bg-card shrink-0">

        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-black dark:bg-white text-white dark:text-black flex items-center justify-center shadow-sm">
            <Sparkles size={16} strokeWidth={2.2} />
          </div>

          <div>
            <div className="flex items-center gap-2">
              <h2 className="font-bold text-lg text-foreground">
                IntelliDocs Answer
              </h2>
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 text-xs font-semibold border border-emerald-200 dark:border-emerald-800">
                <ShieldCheck size={11} />
                Verified Grounded
              </span>
              {sources && sources.length > 0 && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 text-xs font-semibold border border-blue-200 dark:border-blue-800">
                  <Sparkles size={11} />
                  Synthesized from {sources.length} source{sources.length !== 1 ? 's' : ''}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Actions Toolbar */}
        <div className="flex items-center gap-1">
          <button
            onClick={copyAnswer}
            disabled={!answer}
            className="p-1.5 rounded-lg border border-border bg-card hover:bg-secondary text-muted-foreground hover:text-foreground transition text-sm flex items-center gap-1 disabled:opacity-40"
            title="Copy Answer"
          >
            <Copy size={14} />
          </button>

          {/* Download Dropdown */}
          <div className="relative group">
            <button
              disabled={!answer}
              className="p-1.5 rounded-lg border border-border bg-card hover:bg-secondary text-muted-foreground hover:text-foreground transition text-sm flex items-center gap-1 disabled:opacity-40"
              title="Download Answer"
            >
              <Download size={14} />
            </button>
            <div className="absolute right-0 mt-1 w-36 bg-card border border-border rounded-xl shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-150 z-20 p-1">
              <button
                onClick={() => downloadAnswer("txt")}
                className="w-full text-left px-3 py-1.5 hover:bg-secondary rounded-lg flex items-center gap-2 text-sm font-medium text-foreground"
              >
                <FileTxt size={14} />
                Text (.txt)
              </button>
              <button
                onClick={() => downloadAnswer("markdown")}
                className="w-full text-left px-3 py-1.5 hover:bg-secondary rounded-lg flex items-center gap-2 text-sm font-medium text-foreground"
              >
                <FileText size={14} />
                Markdown (.md)
              </button>
              <button
                onClick={() => downloadAnswer("json")}
                className="w-full text-left px-3 py-1.5 hover:bg-secondary rounded-lg flex items-center gap-2 text-sm font-medium text-foreground"
              >
                <FileJson size={14} />
                JSON (.json)
              </button>
            </div>
          </div>

          <button
            className="p-1.5 rounded-lg border border-border bg-card hover:bg-secondary text-muted-foreground hover:text-emerald-600 transition"
            title="Helpful"
          >
            <ThumbsUp size={14} />
          </button>

          <button
            className="p-1.5 rounded-lg border border-border bg-card hover:bg-secondary text-muted-foreground hover:text-rose-600 transition"
            title="Not Helpful"
          >
            <ThumbsDown size={14} />
          </button>
        </div>

      </div>

      {/* Body */}
      <div className="p-6 space-y-4 flex-1 overflow-y-auto flex flex-col">

        {/* User Question Quote */}
        {question && (
          <div className="rounded-xl border border-border bg-secondary/40 p-4 flex items-start gap-3 border-l-4 border-l-foreground/30">
            <div className="w-8 h-8 rounded-lg bg-secondary flex items-center justify-center border border-border shrink-0 mt-0.5">
              <User size={16} className="text-foreground" />
            </div>
            <div className="min-w-0 flex-1">
              <span className="text-sm font-bold uppercase tracking-wider text-muted-foreground block mb-1">
                Your Question
              </span>
              <p className="text-base font-semibold text-foreground leading-relaxed whitespace-pre-wrap">
                {question}
              </p>
            </div>
          </div>
        )}

        {/* Answer Content */}
        <div className="rounded-xl border border-border/80 bg-card p-5 min-h-[160px]">
          {loading ? (
            <div className="flex items-center justify-center gap-3 text-muted-foreground py-8">
              <Loader2 size={20} className="animate-spin text-foreground" />
              <span className="text-base font-medium">
                Searching knowledge base &amp; synthesizing citations...
              </span>
            </div>
          ) : answer ? (
            <MarkdownRenderer content={answer} />
          ) : (
            <p className="text-muted-foreground text-base leading-relaxed py-2 text-center">
              No answer generated yet. Enter a prompt above to receive grounded document insights.
            </p>
          )}
        </div>

        {/* Page Citations */}
        {sources && sources.length > 0 && (
          <SourceCitations sources={sources} />
        )}

      </div>

      {/* Footer Meta */}
      <div className="flex items-center justify-between px-6 py-3 border-t border-border bg-secondary/20 text-muted-foreground text-xs">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5">
            <Clock size={13} />
            <span>
              {loading ? "Generating..." : "Response ready • Instant retrieval"}
            </span>
          </div>
          {!loading && sources && sources.length > 0 && (
            <span className="text-muted-foreground">
              • {sources.length} source{sources.length !== 1 ? 's' : ''} cited
            </span>
          )}
        </div>

        <span className="font-mono text-xs">
          IntelliDocs RAG v2.5
        </span>
      </div>

    </div>
  );
}