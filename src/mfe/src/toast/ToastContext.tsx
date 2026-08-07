import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import Box from "@mui/joy/Box";
import IconButton from "@mui/joy/IconButton";
import Snackbar from "@mui/joy/Snackbar";
import Typography from "@mui/joy/Typography";

type ToastTone = "danger" | "success" | "neutral";

interface ToastState {
  open: boolean;
  message: string;
  tone: ToastTone;
  copied: boolean;
}

interface ToastApi {
  error: (message: string) => void;
  success: (message: string) => void;
  info: (message: string) => void;
}

const ToastContext = createContext<ToastApi | null>(null);

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toast, setToast] = useState<ToastState>({
    open: false,
    message: "",
    tone: "neutral",
    copied: false,
  });

  const show = useCallback((message: string, tone: ToastTone) => {
    setToast({ open: true, message, tone, copied: false });
  }, []);

  const close = useCallback(() => {
    setToast((prev) => ({ ...prev, open: false, copied: false }));
  }, []);

  const copy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(toast.message);
      setToast((prev) => ({ ...prev, copied: true }));
    } catch {
      setToast((prev) => ({
        ...prev,
        copied: false,
        message: `${prev.message}\n\n(clipboard copy failed)`,
      }));
    }
  }, [toast.message]);

  const api = useMemo<ToastApi>(
    () => ({
      error: (message) => show(message, "danger"),
      success: (message) => show(message, "success"),
      info: (message) => show(message, "neutral"),
    }),
    [show],
  );

  return (
    <ToastContext.Provider value={api}>
      {children}
      <Snackbar
        open={toast.open}
        color={toast.tone}
        variant="solid"
        autoHideDuration={null}
        onClose={(_event, reason) => {
          if (reason === "clickaway") return;
          close();
        }}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
        sx={{
          maxWidth: "min(720px, calc(100vw - 24px))",
          alignItems: "flex-start",
        }}
        endDecorator={
          <IconButton
            size="sm"
            variant="plain"
            onClick={close}
            aria-label="Dismiss"
            sx={{ color: "inherit" }}
          >
            ✕
          </IconButton>
        }
      >
        <Box
          onClick={() => void copy()}
          title="Click to copy"
          sx={{ cursor: "pointer", pr: 1, minWidth: 0 }}
        >
          <Typography level="body-xs" sx={{ opacity: 0.85, mb: 0.5 }}>
            {toast.copied ? "Copied" : "Click message to copy"}
          </Typography>
          <Typography
            level="body-sm"
            sx={{
              whiteSpace: "pre-wrap",
              wordBreak: "break-word",
              fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
              maxHeight: "40vh",
              overflow: "auto",
            }}
          >
            {toast.message}
          </Typography>
        </Box>
      </Snackbar>
    </ToastContext.Provider>
  );
}

export function useToast(): ToastApi {
  const ctx = useContext(ToastContext);
  if (!ctx) {
    throw new Error("useToast must be used within ToastProvider");
  }
  return ctx;
}
