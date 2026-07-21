import { useContext } from "react";
import { MessageSquare, Trash2 } from "lucide-react";
import { ChatHistoryContext } from "../../context/ChatHistoryContext";

export default function ChatHistory({ onSelectHistory, searchQuery = "" }) {
  const { history = [], removeFromHistory, clearHistory } =
    useContext(ChatHistoryContext);

  const formatTime = (date) => {
    const now = new Date();
    const diffMs = now - new Date(date);
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return new Date(date).toLocaleDateString();
  };

  const truncateText = (text, maxLength = 32) => {
    if (!text) return "";
    return text.length > maxLength ? text.substring(0, maxLength) + "..." : text;
  };

  const filteredHistory = history.filter((item) => {
    if (!searchQuery) return true;
    const query = searchQuery.toLowerCase();
    return (
      (item.question && item.question.toLowerCase().includes(query)) ||
      (item.answer && item.answer.toLowerCase().includes(query))
    );
  });

  return (
    <div className="px-4 py-3 flex flex-col flex-1 min-h-0">
      <div className="flex items-center justify-between mb-2.5 shrink-0">
        <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
          Recent Conversations
        </h3>
        {history.length > 0 && (
          <button
            onClick={clearHistory}
            className="text-xs font-semibold text-muted-foreground hover:text-foreground transition"
          >
            Clear all
          </button>
        )}
      </div>

      <div className="space-y-1 overflow-y-auto flex-1 min-h-0 pr-1">
        {history.length === 0 ? (
          <p className="text-xs text-muted-foreground text-center py-3">
            No recent conversations
          </p>
        ) : filteredHistory.length === 0 ? (
          <p className="text-xs text-muted-foreground text-center py-3">
            No matching conversations
          </p>
        ) : (
          filteredHistory.map((item) => (
            <div
              key={item.id}
              className="group p-2.5 rounded-xl hover:bg-card border border-transparent hover:border-border transition-all cursor-pointer flex items-center justify-between"
              onClick={() =>
                onSelectHistory({
                  question: item.question,
                  answer: item.answer,
                  sources: item.sources,
                })
              }
            >
              <div className="flex items-center gap-2.5 min-w-0 pr-2">
                <MessageSquare size={15} className="text-muted-foreground shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-xs md:text-sm font-semibold text-foreground truncate leading-snug">
                    {truncateText(item.question, 30)}
                  </p>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    {formatTime(item.timestamp)}
                  </p>
                </div>
              </div>

              <button
                onClick={(e) => {
                  e.stopPropagation();
                  removeFromHistory(item.id);
                }}
                className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg hover:bg-muted text-muted-foreground hover:text-destructive transition-all shrink-0"
                title="Delete session"
              >
                <Trash2 size={14} />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
