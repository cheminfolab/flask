import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from "path"

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  base: "/",
  server: {
    port: 3000,
    // `npm run dev`: forward API calls to the Django backend (no CORS setup needed)
    proxy: {
      "/api": process.env.VITE_DEV_API_TARGET ?? "http://127.0.0.1:8000",
    },
  },
})
