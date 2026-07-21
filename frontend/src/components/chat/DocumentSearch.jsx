import { useState, useMemo, useEffect } from "react";
import { Search, X } from "lucide-react";

export default function DocumentSearch({ files = [], onFilter }) {
  const [searchQuery, setSearchQuery] = useState("");

  const filteredFiles = useMemo(() => {
    if (!searchQuery.trim()) return files;
    return files.filter((file) =>
      file.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [files, searchQuery]);

  useEffect(() => {
    if (onFilter) onFilter(filteredFiles);
  }, [filteredFiles, onFilter]);

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const clearSearch = () => {
    setSearchQuery("");
  };

  return (
    <div className="px-4 py-3.5">
      <div className="relative">
        <Search
          size={16}
          className="absolute left-3.5 top-1/2 transform -translate-y-1/2 text-muted-foreground pointer-events-none"
        />
        <input
          type="text"
          placeholder="Search conversations..."
          value={searchQuery}
          onChange={handleSearchChange}
          className="w-full pl-10 pr-12 py-2.5 rounded-xl border border-border bg-card text-xs md:text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-black dark:focus:border-white transition-all shadow-[0_1px_2px_rgba(0,0,0,0.03)]"
        />
        {searchQuery ? (
          <button
            onClick={clearSearch}
            className="absolute right-3.5 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground transition"
          >
            <X size={15} />
          </button>
        ) : (
          <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-xs font-mono text-muted-foreground border border-border px-1.5 py-0.5 rounded bg-muted/50 pointer-events-none">
            ⌘K
          </span>
        )}
      </div>

      {searchQuery && filteredFiles.length > 0 && (
        <div className="mt-3 space-y-1">
          <p className="text-xs text-muted-foreground px-1">
            Found {filteredFiles.length} item{filteredFiles.length !== 1 ? "s" : ""}
          </p>
          <div className="space-y-1 max-h-40 overflow-y-auto">
            {filteredFiles.map((file, index) => (
              <div
                key={index}
                className="px-3 py-2 rounded-lg bg-secondary/80 text-foreground text-xs md:text-sm font-medium truncate border border-border/50 hover:bg-secondary transition"
              >
                📄 {file.name}
              </div>
            ))}
          </div>
        </div>
      )}

      {searchQuery && filteredFiles.length === 0 && (
        <p className="mt-2 text-xs text-muted-foreground text-center py-2">
          No matches found
        </p>
      )}
    </div>
  );
}
