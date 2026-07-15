import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#1F2A24",
        paper: "#F6F3EA",
        porcelain: "#FEFCF6",
        harbor: "#145C6D",
        sea: "#2E8B8F",
        moss: "#4F7D46",
        amber: "#D98B2B",
        ember: "#B84A38",
        plum: "#6A4C7B"
      },
      fontFamily: {
        sans: ["Aptos", "ui-sans-serif", "system-ui", "sans-serif"],
        display: ["Optima", "Aptos Display", "ui-serif", "serif"],
        mono: ["SFMono-Regular", "Cascadia Code", "ui-monospace", "monospace"]
      },
      boxShadow: {
        ledger: "0 1px 0 rgba(31,42,36,0.08), 0 18px 55px rgba(31,42,36,0.08)"
      }
    }
  },
  plugins: []
};

export default config;
