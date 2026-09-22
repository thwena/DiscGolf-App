import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: "prompt",
      manifest: {
        name: "Disc Golf Tracker",
        short_name: "DGT",
        description: "Self-hosted scoring, inventory, and flight tracking",
        theme_color: "#153b2e",
        background_color: "#f4f1e8",
        display: "standalone",
        start_url: "/",
        icons: [
          { src: "/icon.svg", sizes: "any", type: "image/svg+xml", purpose: "any maskable" }
        ]
      },
      workbox: {
        navigateFallback: "/index.html",
        runtimeCaching: []
      }
    })
  ],
  server: {
    proxy: { "/api": "http://127.0.0.1:8080" }
  }
});
