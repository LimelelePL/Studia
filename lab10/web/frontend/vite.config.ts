import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    // Przekierowanie zapytań /api do backendu FastAPI — brak problemów z CORS.
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
