import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import CssBaseline from "@mui/joy/CssBaseline";
import { CssVarsProvider } from "@mui/joy/styles";
import App from "./App";
import { ToastProvider } from "./toast/ToastContext";
import { z4Theme } from "./theme";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <CssVarsProvider theme={z4Theme} defaultMode="dark">
      <CssBaseline />
      <ToastProvider>
        <App />
      </ToastProvider>
    </CssVarsProvider>
  </StrictMode>,
);
