import { useState } from "react";
import { FileText, BookOpen, ChevronDown, ChevronUp } from "lucide-react";

export default function SourceCitations({ sources = [] }) {
  const [isExpanded, setIsExpanded] = useState(true);

  if (!sources || sources.length === 0) {
    return null;
  }

  // Group by document name
  const groupedSourcesMap = new Map();
  
  sources.forEach((source, idx) => {
    let docName = "Source Document";
    let pageNum = null;
    let chunkNum = null;

    if (typeof source === "object" && source.document_name) {
      docName = source.document_name;
      pageNum = source.page;
      chunkNum = source.chunks ? source.chunks[0] : (source.chunk || null);
    } else if (typeof source === "string") {
      const match = source.match(
        /^(.+?)\s*\(Page\s+(\d+),\s+Chunk\s+(\d+)\)|^(.+?)\s*\(Chunk\s+(\d+)\)/
      );
      if (match) {
        docName = match[1] || match[4];
        pageNum = match[2] ? parseInt(match[2]) : null;
        chunkNum = match[3] || match[5];
      } else {
        docName = source;
      }
    }

    if (!groupedSourcesMap.has(docName)) {
      groupedSourcesMap.set(docName, {
        id: idx,
        name: docName,
        pages: new Set(),
        chunks: new Set(),
      });
    }

    const group = groupedSourcesMap.get(docName);
    if (pageNum !== null) group.pages.add(pageNum);
    if (chunkNum !== null) group.chunks.add(chunkNum);
  });

  const groupedSources = Array.from(groupedSourcesMap.values()).map(group => ({
    ...group,
    pages: Array.from(group.pages).sort((a,b) => a-b),
    chunks: Array.from(group.chunks).sort((a,b) => a-b)
  }));

  return (
    <div className="mt-4 pt-4 border-t border-border/60">

      {/* Citations Header Toggle */}
      <button
        onClick={() => setIsExpanded((prev) => !prev)}
        className="w-full flex items-center justify-between py-1 text-left group"
      >
        <div className="flex items-center gap-2">
          <BookOpen size={14} className="text-foreground" />
          <h4 className="font-bold text-xs text-foreground tracking-tight">
            Source Citations
          </h4>
          <span className="text-[10px] font-semibold bg-secondary text-secondary-foreground px-2 py-0.5 rounded-md border border-border">
            {groupedSources.length} document{groupedSources.length !== 1 ? "s" : ""}
          </span>
        </div>

        <div className="flex items-center gap-1 text-xs text-muted-foreground group-hover:text-foreground transition">
          <span className="text-[11px] font-medium">
            {isExpanded ? "Collapse" : "Expand"}
          </span>
          {isExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </div>
      </button>

      {/* Citations List */}
      {isExpanded && (
        <div className="grid gap-2 mt-3">
          {groupedSources.map((source) => (
            <div
              key={source.id}
              className="p-3 rounded-xl bg-secondary/30 border border-border/60 hover:border-border transition-all flex items-start justify-between gap-3"
            >
              <div className="flex items-start gap-2.5 min-w-0 flex-1">
                <FileText
                  size={15}
                  className="text-foreground mt-0.5 shrink-0"
                />
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-foreground text-xs truncate">
                    {source.name}
                  </p>

                  <div className="flex items-center gap-2 mt-1 text-[10px] text-muted-foreground flex-wrap">
                    {source.pages && source.pages.length > 0 && (
                      <span className="bg-card border border-border px-1.5 py-0.5 rounded font-mono">
                        Page{source.pages.length > 1 ? "s" : ""} {source.pages.join(", ")}
                      </span>
                    )}
                    {source.chunks && source.chunks.length > 0 && (
                      <span className="bg-card border border-border px-1.5 py-0.5 rounded font-mono">
                        Chunk{source.chunks.length > 1 ? "s" : ""} {source.chunks.join(", ")}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <span className="text-[10px] font-semibold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 px-1.5 py-0.5 rounded border border-emerald-200 dark:border-emerald-800 shrink-0">
                Verified
              </span>
            </div>
          ))}
        </div>
      )}

    </div>
  );
}
