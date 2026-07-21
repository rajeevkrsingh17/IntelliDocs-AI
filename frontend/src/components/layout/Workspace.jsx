import { useState, useContext, useEffect } from "react";

import UploadCard from "../upload/UploadCard";
import ChatInput from "../chat/ChatInput";
import AnswerCard from "../answer/AnswerCard";
import CompareDocuments from "../compare/CompareDocuments";

import CompareResult from "../compare/CompareResult";

import { compareDocuments, askQuestion } from "../../services/api";
import { ChatHistoryContext } from "../../context/ChatHistoryContext";
import { ToastContext } from "../../context/ToastContext";

import {
  MessageSquare,
  GitCompare,
  FileText,
  Sparkles,
  Zap,
  Star,
  Layers,
} from "lucide-react";

export default function Workspace({ files = [], setFiles, activeHistoryItem, onNewChat }) {
  // Context
  const { addToHistory } = useContext(ChatHistoryContext);
  const { showToast } = useContext(ToastContext);

  // Mode
  const [mode, setMode] = useState("chat");

  // Chat States
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState("");

  // Compare States
  const [compareLoading, setCompareLoading] = useState(false);
  const [comparisonResult, setComparisonResult] = useState("");
  const [selectedDocuments, setSelectedDocuments] = useState([]);

  // Load history item when clicked from sidebar
  useEffect(() => {
    if (activeHistoryItem) {
      setQuestion(activeHistoryItem.question || "");
      setAnswer(activeHistoryItem.answer || "");
      setSources(activeHistoryItem.sources || []);
      setMode("chat");
    }
  }, [activeHistoryItem]);

  // Auto-select single document
  useEffect(() => {
    if (files && files.length === 1) {
      setSelectedDocument(files[0].name);
    }
  }, [files]);

  const executeQuestion = async (queryText) => {
    const q = queryText !== undefined ? queryText : question;
    if (!q || !q.trim()) return;

    setLoading(true);

    try {
      console.log("Sending question:", q, "Document:", selectedDocument || "All");
      const response = await askQuestion(q, selectedDocument || null);
      
      const ans = response.answer || "";
      const srcs = response.sources || [];

      setAnswer(ans);
      setSources(srcs);

      if (q && ans) {
        addToHistory({
          question: q,
          answer: ans,
          sources: srcs,
        });
      }
    } catch (error) {
      console.error(error);
      setAnswer("Something went wrong while generating the answer. Please check if backend service is running.");
      setSources([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (text) => {
    setQuestion(text);
    executeQuestion(text);
  };

  // Compare Documents
  const handleCompare = async ({
    documents,
    comparisonType,
    customPrompt,
  }) => {
    setCompareLoading(true);

    try {
      setSelectedDocuments(documents);

      const response =
        await compareDocuments({
          documents,
          comparisonType,
          customPrompt,
        });

      setComparisonResult(
        response.comparison
      );
      if (showToast) showToast("Document comparison completed successfully!", "success");
    } catch (error) {
      console.error(error);
      const errMsg = error.message || "Failed to compare documents.";
      setComparisonResult(
        `### ⚠️ Comparison Failed\n\n${errMsg}`
      );
      if (showToast) showToast(errMsg, "error");
    } finally {
      setCompareLoading(false);
    }
  };

  return (
    <main className="flex-1 overflow-auto bg-background transition-colors duration-200 flex flex-col h-full min-h-0">

      <div className="max-w-[1600px] w-full mx-auto px-4 md:px-6 py-6 flex flex-col flex-1 min-h-0 gap-6">

        {/* Compact Header & Controls */}
        <div className="animate-fade-in-up flex flex-col md:flex-row md:items-center justify-between gap-4 shrink-0 bg-card p-4 md:p-5 rounded-2xl border border-border shadow-[0_2px_8px_rgba(0,0,0,0.04)] hover:shadow-md transition-shadow duration-300">
          
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-black dark:bg-white flex items-center justify-center shadow-sm shrink-0 transition-transform hover:scale-105">
              <FileText className="text-white dark:text-black" size={20} strokeWidth={2.2} />
            </div>
            <div>
              <h1 className="text-xl md:text-2xl font-bold text-foreground tracking-tight">
                IntelliDocs AI
              </h1>
              <p className="text-xs md:text-sm font-medium text-muted-foreground">
                Intelligent Document Analysis Platform
              </p>
            </div>
          </div>

          {/* Mode Segmented Control Tabs */}
          <div className="inline-flex p-1 rounded-xl bg-muted/80 border border-border shrink-0">
            <button
              onClick={() => setMode("chat")}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm md:text-base font-semibold transition-all duration-200 ${
                mode === "chat"
                  ? "bg-black text-white dark:bg-white dark:text-black shadow-sm scale-[1.02]"
                  : "text-muted-foreground hover:text-foreground hover:bg-black/5 dark:hover:bg-white/5"
              }`}
            >
              <MessageSquare size={15} />
              <span>Chat</span>
            </button>

            <button
              onClick={() => setMode("compare")}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm md:text-base font-semibold transition-all duration-200 ${
                mode === "compare"
                  ? "bg-black text-white dark:bg-white dark:text-black shadow-sm scale-[1.02]"
                  : "text-muted-foreground hover:text-foreground hover:bg-black/5 dark:hover:bg-white/5"
              }`}
            >
              <GitCompare size={15} />
              <span>Compare Documents</span>
            </button>
          </div>
        </div>

        {/* Main 2-Column Grid */}
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6 items-start">
          
          {/* Left Column - Setup & Upload */}
          <div className="xl:col-span-4 space-y-6 xl:sticky xl:top-0 animate-fade-in-up delay-100">
            {/* Upload Card */}
            <UploadCard
              files={files}
              setFiles={setFiles}
            />
          </div>

          {/* Right Column - Actions & Results */}
          <div className="xl:col-span-8 animate-fade-in-up delay-200 flex flex-col h-full min-h-0">
            
            {/* ==========================
                CHAT MODE
            ========================== */}
            {mode === "chat" && (
              <div className="flex flex-col h-full flex-1 min-h-0 bg-card rounded-[24px] border border-border p-6 shadow-[0_2px_8px_rgba(0,0,0,0.02)]">
                
                {/* Chat Header */}
                <div className="mb-4 shrink-0">
                  <div className="flex items-center gap-2 mb-1">
                    <Sparkles size={18} className="text-foreground" />
                    <h2 className="font-bold text-lg text-foreground">Ask Anything About Your Documents</h2>
                  </div>
                  <p className="text-sm text-muted-foreground">Ask questions in natural language and receive context-aware answers with citations.</p>
                </div>

                {/* Main Content Area */}
                <div className="flex-1 min-h-0 overflow-y-auto mb-4 flex flex-col">
                  {(!question && !answer && !loading) ? (
                    <div className="flex-1 rounded-2xl bg-secondary/30 border border-border flex flex-col items-center justify-center p-8 text-center min-h-[400px]">
                      <div className="w-12 h-12 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center mb-4">
                         <Sparkles size={24} />
                      </div>
                      <h3 className="text-xl font-bold text-foreground mb-2">Welcome to IntelliDocs AI!</h3>
                      <p className="text-sm text-muted-foreground max-w-md mb-8">
                        I can help you understand your documents, find information, and answer questions. Try asking me about your uploaded documents.
                      </p>
                      
                      {/* Suggestion Chips */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl">
                         {[
                           { text: "Summarize this document", icon: FileText },
                           { text: "Compare uploaded files", icon: GitCompare },
                           { text: "What are the key findings?", icon: Sparkles },
                           { text: "Extract important topics", icon: Layers },
                           { text: "Explain like I'm a beginner", icon: Zap },
                           { text: "Generate quiz questions", icon: MessageSquare }
                         ].map((chip, idx) => {
                            const Icon = chip.icon;
                            return (
                              <button
                                key={idx}
                                onClick={() => handleSuggestionClick(chip.text)}
                                className="flex items-center gap-3 p-3 rounded-xl border border-border bg-card hover:bg-secondary transition-colors text-left group"
                              >
                                <Icon size={16} className="text-indigo-500 shrink-0 group-hover:scale-110 transition-transform" />
                                <span className="text-sm font-medium text-muted-foreground group-hover:text-foreground transition-colors">{chip.text}</span>
                              </button>
                            );
                         })}
                      </div>
                    </div>
                  ) : (
                    <div className="flex-1 min-h-0">
                      <AnswerCard
                        question={question}
                        answer={answer}
                        sources={sources}
                        loading={loading}
                      />
                    </div>
                  )}
                </div>

                {/* Input Area */}
                <div className="shrink-0">
                  <ChatInput
                    question={question}
                    setQuestion={setQuestion}
                    onSubmit={() => executeQuestion(question)}
                    loading={loading}
                    files={files}
                    selectedDocument={selectedDocument}
                    setSelectedDocument={setSelectedDocument}
                  />
                  
                  {/* Disclaimer */}
                  <p className="text-center text-[11px] text-muted-foreground mt-3">
                    AI responses may not always be perfect. Please verify important information.
                  </p>
                </div>
              </div>
            )}

            {/* ==========================
                COMPARE MODE
            ========================== */}
            {mode === "compare" && (
              <div className="space-y-6">
                <CompareDocuments
                  files={files}
                  onCompare={handleCompare}
                  loading={compareLoading}
                />

                <CompareResult
                  result={comparisonResult}
                  loading={compareLoading}
                  documents={selectedDocuments}
                />
              </div>
            )}
            
          </div>
        </div>

      </div>
    </main>
  );
}