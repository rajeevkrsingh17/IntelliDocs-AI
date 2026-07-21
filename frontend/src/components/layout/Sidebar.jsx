import { useState, useContext, useEffect } from "react";
import {
  FileText,
  Plus,
  Trash2,
  FolderOpen,
  MessageSquare,
  Database,
  Search,
  X,
} from "lucide-react";
import ChatHistory from "../chat/ChatHistory";
import WorkspaceStats from "../chat/WorkspaceStats";
import { ToastContext } from "../../context/ToastContext";
import { deleteDocument, clearAllDocuments } from "../../services/api";

export default function Sidebar({ files = [], setFiles, onNewChat, onSelectHistory }) {
  const [sidebarTab, setSidebarTab] = useState("conversations");
  const [searchQuery, setSearchQuery] = useState("");
  const { showToast } = useContext(ToastContext);

  const removeFile = async (name) => {
    setFiles((prev) => prev.filter((file) => file.name !== name));
    try {
      await deleteDocument(name);
      if (showToast) showToast(`Deleted "${name}" from vector database`, "info");
    } catch (err) {
      console.error(err);
    }
  };

  const handleClearAll = async () => {
    if (!files.length) return;
    if (window.confirm("Are you sure you want to clear all indexed documents?")) {
      setFiles([]);
      try {
        await clearAllDocuments();
        if (showToast) showToast("Cleared all documents from vector store", "success");
      } catch (err) {
        console.error(err);
      }
    }
  };

  const formatSize = (bytes) => {
    const size = Number(bytes) || 0;
    if (size === 0) return "0 KB";
    if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
    return `${(size / (1024 * 1024)).toFixed(2)} MB`;
  };

  const getFormatBadgeStyle = (filename) => {
    const ext = filename ? filename.split(".").pop().toLowerCase() : "";
    switch (ext) {
      case "pdf":
        return "bg-rose-50 text-rose-600 border-rose-200 dark:bg-rose-950/40 dark:text-rose-400 dark:border-rose-800";
      case "docx":
      case "doc":
        return "bg-blue-50 text-blue-600 border-blue-200 dark:bg-blue-950/40 dark:text-blue-400 dark:border-blue-800";
      case "pptx":
      case "ppt":
        return "bg-amber-50 text-amber-600 border-amber-200 dark:bg-amber-950/40 dark:text-amber-400 dark:border-amber-800";
      case "md":
      case "txt":
        return "bg-purple-50 text-purple-600 border-purple-200 dark:bg-purple-950/40 dark:text-purple-400 dark:border-purple-800";
      default:
        return "bg-slate-100 text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700";
    }
  };



  const filesToDisplay = files.filter(file => 
    file?.name?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <aside className="w-[360px] bg-sidebar border-r border-border flex flex-col transition-colors duration-200 overflow-hidden shrink-0">

      {/* Primary Action: New Conversation */}
      <div className="p-4 border-b border-border/60">
        <button
          onClick={onNewChat}
          className="w-full flex items-center justify-center gap-2.5 py-3 px-4 rounded-xl bg-black hover:bg-neutral-800 dark:bg-white dark:hover:bg-neutral-200 text-white dark:text-black font-semibold text-sm shadow-sm transition-all duration-150 active:scale-[0.99]"
        >
          <Plus size={18} strokeWidth={2.5} />
          <span>New Conversation</span>
        </button>
      </div>

      {/* Search Bar */}
      <div className="border-b border-border/60 p-4">
        <div className="relative">
          <Search
            size={16}
            className="absolute left-3.5 top-1/2 transform -translate-y-1/2 text-muted-foreground pointer-events-none"
          />
          <input
            type="text"
            placeholder={sidebarTab === "conversations" ? "Search conversations..." : "Search documents..."}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-10 py-2.5 rounded-xl border border-border bg-card text-xs md:text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-black dark:focus:border-white transition-all shadow-[0_1px_2px_rgba(0,0,0,0.03)]"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              className="absolute right-3.5 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground transition"
            >
              <X size={15} />
            </button>
          )}
        </div>
      </div>

      {/* Sidebar Tab Switcher */}
      <div className="px-4 pt-3 pb-2 border-b border-border/60">
        <div className="flex p-1 rounded-xl bg-muted/80 border border-border">
          <button
            onClick={() => setSidebarTab("conversations")}
            className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-sm font-semibold transition-all duration-150 ${sidebarTab === "conversations"
                ? "bg-black text-white dark:bg-white dark:text-black shadow-sm"
                : "text-muted-foreground hover:text-foreground"
              }`}
          >
            <MessageSquare size={15} />
            <span>Chats</span>
          </button>
          <button
            onClick={() => setSidebarTab("documents")}
            className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-sm font-semibold transition-all duration-150 ${sidebarTab === "documents"
                ? "bg-black text-white dark:bg-white dark:text-black shadow-sm"
                : "text-muted-foreground hover:text-foreground"
              }`}
          >
            <Database size={15} />
            <span>Documents</span>
          </button>
        </div>
      </div>

      {/* ========================
          CONVERSATIONS TAB
      ======================== */}
      {sidebarTab === "conversations" && (
        <div className="flex-1 flex flex-col animate-fade-in min-h-0">
          {/* Recent Conversations */}
          <div className="flex-1 flex flex-col min-h-0">
            <ChatHistory
              onSelectHistory={(item) => {
                setSearchQuery("");
                onSelectHistory(item);
              }}
              searchQuery={searchQuery}
            />
          </div>

          {/* Workspace Stats (2x2 Grid) */}
          <div className="border-t border-border/60">
            <WorkspaceStats files={files} />
          </div>
        </div>
      )}

      {/* ========================
          DOCUMENTS TAB
      ======================== */}
      {sidebarTab === "documents" && (
        <div className="flex-1 overflow-y-auto flex flex-col animate-fade-in">
          {/* Knowledge Base Header */}
          <div className="px-4 pt-4 pb-2.5 flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <h3 className="text-sm font-bold text-foreground">
                Knowledge Base
              </h3>
              <span className="bg-secondary text-secondary-foreground text-xs px-2.5 py-0.5 rounded-lg font-bold border border-border">
                {files.length} files
              </span>
            </div>

            <div className="flex items-center gap-2">
              {files.length > 0 && (
                <button
                  onClick={handleClearAll}
                  className="text-xs font-semibold text-muted-foreground hover:text-destructive transition px-2 py-1 rounded-lg hover:bg-destructive/10"
                  title="Clear all documents"
                >
                  Clear all
                </button>
              )}
            </div>
          </div>

          {/* Documents List */}
          <div className="flex-1 overflow-y-auto px-4 pb-4 space-y-2.5">
            {filesToDisplay.length === 0 && files.length === 0 ? (
              <div className="border border-dashed border-border rounded-xl bg-card p-6 text-center mt-2">
                <div className="w-14 h-14 rounded-2xl bg-secondary flex items-center justify-center border border-border mx-auto mb-3">
                  <FolderOpen size={24} className="text-muted-foreground" />
                </div>
                <p className="font-bold text-foreground text-sm">No Documents Yet</p>
                <p className="text-sm text-muted-foreground mt-1.5 leading-relaxed">
                  Upload files in the main workspace to build your knowledge base
                </p>
              </div>
            ) : filesToDisplay.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-6">
                No matching documents found
              </p>
            ) : (
              filesToDisplay.map((file) => {
                const ext = file.name ? file.name.split(".").pop().toUpperCase() : "DOC";
                return (
                  <div
                    key={file.name}
                    className="bg-card border border-border rounded-xl p-3.5 hover:border-foreground/20 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-[0_2px_8px_rgba(0,0,0,0.06)] transition-all group"
                  >
                    <div className="flex items-start justify-between gap-2.5">
                      <div className="flex items-start gap-3 min-w-0 flex-1">
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-black border shrink-0 uppercase tracking-wide mt-0.5 ${getFormatBadgeStyle(
                            file.name
                          )}`}
                        >
                          {ext}
                        </span>

                        <div className="min-w-0 flex-1">
                          <h4
                            className="font-semibold text-foreground truncate text-sm leading-snug"
                            title={file.name}
                          >
                            {file.name}
                          </h4>

                          <div className="flex items-center gap-2 text-xs text-muted-foreground mt-1.5">
                            <span>{formatSize(file.size)}</span>
                            {file.pages > 0 && <span>• {file.pages} pages</span>}
                            {file.chunks > 0 && <span>• {file.chunks} chunks</span>}
                          </div>

                          <div className="flex items-center gap-1.5 mt-2">
                            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 text-xs font-semibold border border-emerald-200 dark:border-emerald-800">
                              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                              Indexed
                            </span>
                          </div>
                        </div>
                      </div>

                      <button
                        onClick={() => removeFile(file.name)}
                        className="p-1.5 rounded-lg text-muted-foreground opacity-0 group-hover:opacity-100 hover:bg-destructive/10 hover:text-destructive transition-all shrink-0"
                        title="Delete document"
                      >
                        <Trash2 size={15} />
                      </button>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      )}


    </aside>
  );
}