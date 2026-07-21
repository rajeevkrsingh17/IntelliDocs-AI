import { createContext, useState, useEffect, useCallback } from "react";

export const ChatHistoryContext = createContext();

const STORAGE_KEY = "intellidocs_chat_sessions";

export function ChatHistoryProvider({ children }) {
  const [history, setHistory] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      console.error("Failed to load chat history from localStorage", e);
      return [];
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
    } catch (e) {
      console.error("Failed to save chat history to localStorage", e);
    }
  }, [history]);

  const addToHistory = useCallback((conversation) => {
    const newConversation = {
      id: Date.now(),
      timestamp: new Date().toISOString(),
      ...conversation,
    };
    setHistory((prev) => [newConversation, ...prev]);
    return newConversation.id;
  }, []);

  const removeFromHistory = useCallback((id) => {
    setHistory((prev) => prev.filter((item) => item.id !== id));
  }, []);

  const clearHistory = useCallback(() => {
    setHistory([]);
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (e) {
      console.error(e);
    }
  }, []);

  const getHistory = useCallback(() => history, [history]);

  return (
    <ChatHistoryContext.Provider
      value={{ history, addToHistory, removeFromHistory, clearHistory, getHistory }}
    >
      {children}
    </ChatHistoryContext.Provider>
  );
}
