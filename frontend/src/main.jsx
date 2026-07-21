import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Toaster } from "sonner";

import "./index.css";
import App from "./App.jsx";
import { ThemeProvider } from "./context/ThemeContext";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <ThemeProvider>

      <App />

      <Toaster
        richColors
        position="top-right"
        closeButton
        duration={3000}
      />

    </ThemeProvider>
  </StrictMode>
);