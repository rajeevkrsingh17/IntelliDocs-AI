import { FileText, Layers, HardDrive, FileCheck } from "lucide-react";

export default function WorkspaceStats({ files = [] }) {
  const calculateStats = () => {
    const totalFiles = files.length;

    const totalChunks = files.reduce((sum, file) => {
      return sum + (file.chunks || 0);
    }, 0);

    const totalPages = files.reduce((sum, file) => {
      return sum + (file.pages || 0);
    }, 0);

    const totalStorage = files.reduce((sum, file) => {
      return sum + (file.size || 0);
    }, 0);

    const storageInMB = (totalStorage / (1024 * 1024)).toFixed(2);

    return {
      files: totalFiles,
      chunks: totalChunks,
      pages: totalPages,
      storage: storageInMB,
    };
  };

  const stats = calculateStats();

  return (
    <div className="px-4 py-3.5">
      <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground mb-3">
        Workspace Overview
      </h3>

      <div className="grid grid-cols-2 gap-2.5">
        {/* Files Card */}
        <div className="p-3 rounded-xl bg-card border border-border shadow-[0_1px_2px_rgba(0,0,0,0.03)] hover:border-gray-300 transition-all">
          <div className="flex items-center gap-1.5 text-blue-600 mb-1">
            <FileCheck size={15} />
            <span className="text-xs font-semibold text-muted-foreground">Files</span>
          </div>
          <p className="text-2xl font-bold text-foreground leading-tight">
            {stats.files}
          </p>
          <p className="text-xs text-muted-foreground mt-0.5 font-medium">
            Indexed
          </p>
        </div>

        {/* Pages Card */}
        <div className="p-3 rounded-xl bg-card border border-border shadow-[0_1px_2px_rgba(0,0,0,0.03)] hover:border-gray-300 transition-all">
          <div className="flex items-center gap-1.5 text-purple-600 mb-1">
            <FileText size={15} />
            <span className="text-xs font-semibold text-muted-foreground">Pages</span>
          </div>
          <p className="text-2xl font-bold text-foreground leading-tight">
            {stats.pages}
          </p>
          <p className="text-xs text-muted-foreground mt-0.5 font-medium">
            Total
          </p>
        </div>

        {/* Chunks Card */}
        <div className="p-3 rounded-xl bg-card border border-border shadow-[0_1px_2px_rgba(0,0,0,0.03)] hover:border-gray-300 transition-all">
          <div className="flex items-center gap-1.5 text-emerald-600 mb-1">
            <Layers size={15} />
            <span className="text-xs font-semibold text-muted-foreground">Chunks</span>
          </div>
          <p className="text-2xl font-bold text-foreground leading-tight">
            {stats.chunks}
          </p>
          <p className="text-xs text-muted-foreground mt-0.5 font-medium">
            Total
          </p>
        </div>

        {/* Storage Card */}
        <div className="p-3 rounded-xl bg-card border border-border shadow-[0_1px_2px_rgba(0,0,0,0.03)] hover:border-gray-300 transition-all">
          <div className="flex items-center gap-1.5 text-amber-600 mb-1">
            <HardDrive size={15} />
            <span className="text-xs font-semibold text-muted-foreground">Storage</span>
          </div>
          <p className="text-xl font-bold text-foreground leading-tight truncate">
            {stats.storage} <span className="text-xs font-semibold">MB</span>
          </p>
          <p className="text-xs text-muted-foreground mt-0.5 font-medium">
            Used
          </p>
        </div>
      </div>
    </div>
  );
}
