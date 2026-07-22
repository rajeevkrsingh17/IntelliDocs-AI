import { useState, useContext } from "react";
import {
  FileText,
  Moon,
  Sun,
  Settings,
  Trash2,
  Database,
  Activity,
  Menu,
} from "lucide-react";

import { useTheme } from "../../context/ThemeContext";
import { ChatHistoryContext } from "../../context/ChatHistoryContext";
import { ToastContext } from "../../context/ToastContext";
import api from "../../services/api";

export default function Navbar({ onClearAllDocuments, filesCount, setSidebarOpen }) {
  const { theme, toggleTheme } = useTheme();
  const [settingsOpen, setSettingsOpen] = useState(false);
  const { clearHistory } = useContext(ChatHistoryContext);
  const { showToast } = useContext(ToastContext);

  const checkHealth = async () => {
    setSettingsOpen(false);
    try {
      await api.get("/");
      if (showToast) showToast("Backend API is running optimally.", "success");
    } catch (err) {
      if (showToast) showToast("Cannot connect to backend API.", "error");
    }
  };

  const handleClearHistory = () => {
    setSettingsOpen(false);
    if (window.confirm("Are you sure you want to clear all chat sessions?")) {
      clearHistory();
      if (showToast) showToast("Chat history cleared.", "success");
    }
  };

  const handleClearKnowledgeBase = () => {
    setSettingsOpen(false);
    if (onClearAllDocuments) {
      onClearAllDocuments();
    }
  };

  return (
    <header className="sticky top-0 z-50 h-16 bg-card border-b border-border shadow-[0_1px_3px_rgba(0,0,0,0.02)] flex items-center justify-between px-6 transition-colors duration-200">

      {/* Left Section */}
      <div className="flex items-center gap-3">

        {/* Toggle Sidebar Button (Mobile/Tablet only) */}
        <button
          onClick={() => setSidebarOpen((prev) => !prev)}
          className="xl:hidden w-9 h-9 rounded-lg border border-border bg-card hover:bg-muted text-muted-foreground hover:text-foreground flex items-center justify-center mr-1 shrink-0"
          title="Toggle Sidebar"
        >
          <Menu size={18} />
        </button>

        {/* Logo Icon Container */}
        <div className="w-9 h-9 rounded-xl bg-black dark:bg-white flex items-center justify-center shadow-sm">
          <FileText className="text-white dark:text-black" size={20} strokeWidth={2.2} />
        </div>


        {/* Title & Tagline */}
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-lg font-bold text-foreground tracking-tight">
              IntelliDocs AI
            </h1>

            <span className="text-[11px] font-semibold bg-secondary text-secondary-foreground px-2 py-0.5 rounded-md border border-border">
              Beta
            </span>
          </div>

          <p className="text-xs text-muted-foreground font-normal leading-none mt-0.5">
            AI-powered Document Intelligence
          </p>
        </div>

      </div>

      {/* Right Section */}
      <div className="flex items-center gap-2">

        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="w-9 h-9 rounded-lg border border-border bg-card hover:bg-muted text-muted-foreground hover:text-foreground transition-all duration-200 flex items-center justify-center"
          title={
            theme === "dark"
              ? "Switch to Light Mode"
              : "Switch to Dark Mode"
          }
        >
          {theme === "dark" ? (
            <Sun
              size={18}
              className="text-amber-400 transition-transform duration-200"
            />
          ) : (
            <Moon
              size={18}
              className="text-foreground transition-transform duration-200"
            />
          )}
        </button>

        {/* Settings */}
        <div className="relative">
          <button
            onClick={() => setSettingsOpen(!settingsOpen)}
            className={`w-9 h-9 rounded-lg border border-border transition-all duration-200 flex items-center justify-center ${settingsOpen ? "bg-muted text-foreground" : "bg-card hover:bg-muted text-muted-foreground hover:text-foreground"}`}
            title="Settings"
          >
            <Settings
              size={18}
              className={settingsOpen ? "text-foreground" : "text-muted-foreground"}
            />
          </button>
          
          {settingsOpen && (
            <>
              {/* Backdrop to close dropdown when clicking outside */}
              <div 
                className="fixed inset-0 z-40" 
                onClick={() => setSettingsOpen(false)}
              ></div>
              
              <div className="absolute right-0 mt-2 w-56 bg-card border border-border rounded-xl shadow-lg z-50 p-1 flex flex-col gap-1 overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">
                
                <div className="px-3 py-2 border-b border-border mb-1">
                  <h3 className="text-sm font-semibold text-foreground">Workspace Settings</h3>
                  <p className="text-xs text-muted-foreground">Manage your environment</p>
                </div>
                
                <button
                  onClick={handleClearHistory}
                  className="w-full text-left px-3 py-2 hover:bg-secondary rounded-lg flex items-center gap-2.5 text-sm font-medium text-foreground transition-colors"
                >
                  <Trash2 size={16} className="text-muted-foreground" />
                  Clear Chat History
                </button>
                
                <button
                  onClick={handleClearKnowledgeBase}
                  className="w-full text-left px-3 py-2 hover:bg-secondary rounded-lg flex items-center gap-2.5 text-sm font-medium text-foreground transition-colors"
                >
                  <Database size={16} className="text-muted-foreground" />
                  <div className="flex flex-col">
                    <span>Purge Knowledge Base</span>
                    <span className="text-[10px] text-muted-foreground font-normal">{filesCount || 0} indexed files</span>
                  </div>
                </button>
                
                <button
                  onClick={checkHealth}
                  className="w-full text-left px-3 py-2 hover:bg-secondary rounded-lg flex items-center gap-2.5 text-sm font-medium text-foreground transition-colors"
                >
                  <Activity size={16} className="text-muted-foreground" />
                  API Health Check
                </button>

              </div>
            </>
          )}
        </div>

      </div>

    </header>
  );
}