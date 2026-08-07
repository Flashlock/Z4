import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath, URL } from "node:url";

export default defineConfig({
  plugins: [react()],
  base: "./",
  build: {
    outDir: fileURLToPath(new URL("../dist_mfe", import.meta.url)),
    emptyOutDir: true,
  },
  server: {
    port: 5174,
  },
});
