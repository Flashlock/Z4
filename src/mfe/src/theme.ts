import { extendTheme } from "@mui/joy/styles";

export const z4Theme = extendTheme({
  fontFamily: {
    body: '"IBM Plex Sans", sans-serif',
    display: '"IBM Plex Sans", sans-serif',
  },
  colorSchemes: {
    dark: {
      palette: {
        primary: {
          500: "#2563EB",
          solidBg: "#2563EB",
          solidHoverBg: "#1D4ED8",
        },
        success: {
          500: "#16A34A",
        },
        warning: {
          500: "#F59E0B",
        },
        danger: {
          500: "#DC2626",
        },
        neutral: {
          500: "#475569",
          outlinedBorder: "rgba(71, 85, 105, 0.6)",
        },
        background: {
          body: "#0F172A",
          surface: "#1E293B",
          level1: "#1E293B",
        },
        text: {
          primary: "#E2E8F0",
          secondary: "#94A3B8",
          tertiary: "#475569",
        },
      },
    },
  },
  radius: {
    sm: "2px",
    md: "2px",
    lg: "2px",
  },
});

export const copper = "#C97A2B";
