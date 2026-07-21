import { useState, useEffect } from "react";
import {
  ArrowLeftRight,
  FileText,
  GitCompare,
  Sparkles,
  AlertTriangle,
} from "lucide-react";

export default function CompareDocuments({
  files = [],
  onCompare,
  loading,
}) {
  const [document1, setDocument1] = useState("");
  const [document2, setDocument2] = useState("");
  const [comparisonType, setComparisonType] = useState("detailed");
  const [customPrompt, setCustomPrompt] = useState("");

  useEffect(() => {
    if (files.length >= 1 && !document1) {
      setDocument1(files[0].name);
    }
    if (files.length >= 2 && (!document2 || document2 === files[0]?.name)) {
      setDocument2(files[1].name);
    }
  }, [files]);

  const handleCompare = () => {
    if (!document1 || !document2) {
      alert("Please select two documents.");
      return;
    }

    if (document1 === document2) {
      alert("Please select two different documents.");
      return;
    }

    if (
      comparisonType === "custom" &&
      customPrompt.trim() === ""
    ) {
      alert("Please enter your comparison prompt.");
      return;
    }

    onCompare({
      documents: [document1, document2],
      comparisonType,
      customPrompt,
    });
  };

  const swapDocuments = () => {
    const temp = document1;
    setDocument1(document2);
    setDocument2(temp);
  };

  return (
    <div className="bg-card rounded-2xl border border-border p-6 shadow-[0_2px_8px_rgba(0,0,0,0.02)] space-y-6">

      {/* Header */}
      <div>
        <div className="flex items-center gap-2">
          <GitCompare size={18} className="text-foreground" />
          <h2 className="font-bold text-lg text-foreground">
            AI Document Comparison
          </h2>
        </div>
        <p className="text-sm text-muted-foreground mt-1">
          Select two uploaded documents from your workspace to compare similarities, differences, and insights.
        </p>
      </div>

      {files.length < 2 && (
        <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-600 dark:text-amber-400 text-sm flex items-center gap-2.5">
          <AlertTriangle size={16} className="shrink-0" />
          <span>
            Please upload at least <strong>two documents</strong> to perform document comparison.
          </span>
        </div>
      )}

      {/* Grid: Document A & Document B */}
      <div className="grid md:grid-cols-11 gap-4 items-center">

        {/* Document A */}
        <div className="md:col-span-5 space-y-1.5">
          <label className="block text-sm font-semibold text-foreground">
            Select Document A
          </label>
          <select
            value={document1}
            onChange={(e) => setDocument1(e.target.value)}
            className="w-full rounded-xl border border-border bg-background p-3 text-sm font-medium text-foreground focus:outline-none focus:border-black dark:focus:border-white transition-all shadow-sm"
          >
            <option value="">Select first document</option>
            {files.map((file) => (
              <option key={file.name} value={file.name}>
                📄 {file.name}
              </option>
            ))}
          </select>
        </div>

        {/* Swap Button */}
        <div className="md:col-span-1 flex justify-center pt-5">
          <button
            type="button"
            onClick={swapDocuments}
            title="Swap selected documents"
            className="w-9 h-9 rounded-xl border border-border bg-secondary hover:bg-secondary/80 text-foreground transition-transform active:scale-95 flex items-center justify-center shadow-sm"
          >
            <ArrowLeftRight size={16} />
          </button>
        </div>

        {/* Document B */}
        <div className="md:col-span-5 space-y-1.5">
          <label className="block text-sm font-semibold text-foreground">
            Select Document B
          </label>
          <select
            value={document2}
            onChange={(e) => setDocument2(e.target.value)}
            className="w-full rounded-xl border border-border bg-background p-3 text-sm font-medium text-foreground focus:outline-none focus:border-black dark:focus:border-white transition-all shadow-sm"
          >
            <option value="">Select second document</option>
            {files.map((file) => (
              <option key={file.name} value={file.name}>
                📄 {file.name}
              </option>
            ))}
          </select>
        </div>

      </div>

      {/* Comparison Type */}
      <div className="space-y-1.5">
        <label className="block text-sm font-semibold text-foreground">
          Comparison Mode
        </label>
        <select
          value={comparisonType}
          onChange={(e) => setComparisonType(e.target.value)}
          className="w-full rounded-xl border border-border bg-background p-3 text-sm font-medium text-foreground focus:outline-none focus:border-black dark:focus:border-white transition-all shadow-sm"
        >
          <option value="detailed">Detailed Analysis (Similarities, Differences, Insights)</option>
          <option value="similarities">Similarities &amp; Differences Only</option>
          <option value="summary">High-Level Executive Summary</option>
          <option value="custom">Custom Prompt Instructions</option>
        </select>
      </div>

      {/* Custom Prompt Textarea */}
      {comparisonType === "custom" && (
        <div className="space-y-1.5">
          <label className="block text-sm font-semibold text-foreground">
            Custom Instructions Prompt
          </label>
          <textarea
            rows={4}
            value={customPrompt}
            onChange={(e) => setCustomPrompt(e.target.value)}
            placeholder="Specify custom instructions for comparing Document A and B..."
            className="w-full rounded-xl border border-border bg-background p-3 text-sm text-foreground placeholder:text-muted-foreground outline-none focus:border-black dark:focus:border-white transition-all resize-none shadow-sm"
          />
        </div>
      )}

      {/* Compare Primary Button */}
      <button
        onClick={handleCompare}
        disabled={loading || files.length < 2}
        className="w-full bg-black hover:bg-neutral-800 dark:bg-white dark:hover:bg-neutral-200 text-white dark:text-black rounded-xl py-3 font-semibold text-sm transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-sm flex items-center justify-center gap-2"
      >
        <Sparkles size={16} />
        <span>{loading ? "Comparing Documents..." : "Run AI Comparison"}</span>
      </button>

      {/* Footer Info */}
      <div className="pt-2 flex items-center gap-2 text-xs text-muted-foreground border-t border-border/60">
        <FileText size={14} />
        <span>Compare similarities, key differences, missing topics, and strategic takeaways.</span>
      </div>

    </div>
  );
}