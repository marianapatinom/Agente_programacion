/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#05070d",
        panel: "rgba(12, 18, 31, 0.72)",
        line: "rgba(148, 163, 184, 0.18)",
        electric: "#2563eb",
        cyanline: "#22d3ee",
        emeraldline: "#10b981",
      },
      boxShadow: {
        glow: "0 0 32px rgba(34, 211, 238, 0.16)",
        panel: "0 20px 60px rgba(0, 0, 0, 0.34)",
      },
      fontFamily: {
        sans: [
          "Inter",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "sans-serif",
        ],
      },
    },
  },
  plugins: [],
};
