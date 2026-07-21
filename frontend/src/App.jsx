import { useState, useEffect } from "react";

import Navbar from "./components/layout/Navbar";
import Sidebar from "./components/layout/Sidebar";
import Workspace from "./components/layout/Workspace";
import ToastContainer from "./components/ui/ToastContainer";
import { ToastProvider } from "./context/ToastContext";
import { ChatHistoryProvider } from "./context/ChatHistoryContext";
import { getDocuments, clearAllDocuments } from "./services/api";

function App() {
  // Stores uploaded documents
  const [files, setFiles] = useState([]);
  const [activeHistoryItem, setActiveHistoryItem] = useState(null);
  const [chatKey, setChatKey] = useState(0);

  // Fetch indexed documents on startup
  useEffect(() => {
    const fetchDocs = async () => {
      try {
        const docs = await getDocuments();
        setFiles(docs || []);
      } catch (err) {
        console.error("Error fetching indexed documents on mount:", err);
      }
    };
    fetchDocs();
  }, []);

  const handleNewChat = () => {
    setActiveHistoryItem(null);
    setChatKey((prev) => prev + 1);
  };

  const handleSelectHistory = (item) => {
    setActiveHistoryItem(item);
  };

  const handleClearAllDocuments = async () => {
    if (window.confirm("Are you sure you want to clear all indexed documents?")) {
      setFiles([]);
      try {
        await clearAllDocuments();
      } catch (err) {
        console.error(err);
      }
    }
  };

  return (
    <ToastProvider>
      <ChatHistoryProvider>
        <div className="min-h-screen bg-background transition-colors duration-300">

          {/* Top Navigation */}

          <Navbar onClearAllDocuments={handleClearAllDocuments} filesCount={files.length} />

          {/* Main Layout */}

          <div className="flex h-[calc(100vh-64px)] overflow-hidden">

            {/* Sidebar */}

            <Sidebar
              files={files}
              setFiles={setFiles}
              onNewChat={handleNewChat}
              onSelectHistory={handleSelectHistory}
              onClearAll={handleClearAllDocuments}
            />

            {/* Workspace */}

            <Workspace
              key={chatKey}
              files={files}
              setFiles={setFiles}
              activeHistoryItem={activeHistoryItem}
              onNewChat={handleNewChat}
            />

          </div>

          {/* Toast Container */}

          <ToastContainer />

        </div>
      </ChatHistoryProvider>
    </ToastProvider>
  );
}

export default App;