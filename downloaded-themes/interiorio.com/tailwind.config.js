/* Tailwind v3 config extracted from https://interiorio.com/ */
/** @type {import('tailwindcss').Config} */
module.exports = {
  "content": [
    "./src/**/*.{js,ts,jsx,tsx,html}"
  ],
  "theme": {
    "extend": {
      "colors": {
        "white": "#ffffff",
        "stone-50-a8": {
          "2": "rgb(245 158 11 / 0.08)",
          "3": "rgb(239 68 68 / 0.08)"
        },
        "neutral-50-a8": {
          "2": "rgb(59 130 246 / 0.08)"
        },
        "white-a95": "rgb(255 255 255 / 0.95)",
        "slate-50-a8": "rgb(139 92 246 / 0.08)",
        "white-a85": "rgb(255 255 255 / 0.85)",
        "stone-100-a15": "rgb(220 38 38 / 0.15)",
        "neutral-50-a5": "rgb(0 0 0 / 0.05)",
        "white-a0": "rgb(255 255 255 / 0.0)",
        "stone-200-a20": "rgb(220 38 38 / 0.2)",
        "white-a12": "rgb(255 255 255 / 0.12)",
        "white-a20": "rgb(255 255 255 / 0.2)",
        "white-a75": "rgb(255 255 255 / 0.75)",
        "red": {
          "600": "#dc2626",
          "700": "#b91c1c",
          "500": "#ef4444",
          "900": "#7f1d1d"
        },
        "slate": {
          "600": "#64748b",
          "950": "#0f172a",
          "900": "#334155",
          "400": "#94a3b8"
        },
        "neutral": {
          "100": "#e5e7eb",
          "50": "#f1f5f9",
          "200": "#d1d5db"
        },
        "emerald": {
          "400": "#10b981",
          "700": "#047857",
          "600": "#059669"
        },
        "amber": {
          "300": "#f59e0b"
        },
        "violet": {
          "600": "#8b5cf6"
        },
        "rose": {
          "200": "#fecaca"
        },
        "blue": {
          "500": "#3b82f6",
          "600": "#2563eb",
          "300": "#93c5fd",
          "700": "#1d4ed8"
        },
        "green": {
          "500": "#16a34a"
        },
        "neutral-50": {
          "2": "#fff8f0"
        },
        "orange": {
          "600": "#b45309",
          "500": "#d97706"
        },
        "violet-600": {
          "2": "#7c3aed"
        },
        "background": "#ffffff",
        "foreground": "#0f172a",
        "muted-foreground": "#64748b",
        "primary": "#dc2626",
        "accent": "#10b981",
        "border": "#e5e7eb",
        "destructive": "#dc2626",
        "warning": "#f59e0b",
        "success": "#10b981",
        "info": "#93c5fd"
      },
      "fontFamily": {
        "sans": [
          "Inter",
          "sans-serif"
        ],
        "sans-2": [
          "Inter",
          "sans-serif"
        ],
        "sans-3": [
          "Phosphor"
        ],
        "sans-4": [
          "Phosphor-Bold"
        ]
      },
      "fontSize": {
        "xs": "13px",
        "sm": "14px",
        "base": "16px",
        "lg": "18px",
        "xl": "22px",
        "2xl": "24px",
        "3xl": "28px",
        "4xl": "36px",
        "5xl": "48px",
        "6xl": "56px"
      },
      "fontWeight": {
        "semibold": "600",
        "bold": "700",
        "extrabold": "800",
        "medium": "500",
        "normal": "normal"
      },
      "lineHeight": {
        "none": "1",
        "tight": "1.2",
        "snug": "1.4",
        "normal": "1.55",
        "relaxed": "1.6"
      },
      "letterSpacing": {
        "tighter": "-1px",
        "tight": "-0.5px",
        "normal": "0",
        "wide": "0.3px",
        "wider": "0.06em",
        "widest": "0.08em"
      },
      "spacing": {
        "0": "0px",
        "2px": "2px",
        "1": "4px",
        "6px": "6px",
        "2": "8px",
        "10px": "10px",
        "3": "12px",
        "14px": "14px",
        "4": "16px",
        "18px": "18px",
        "5": "20px",
        "22px": "22px",
        "6": "24px",
        "7": "28px",
        "8": "32px",
        "9": "36px",
        "10": "40px",
        "12": "48px",
        "14": "56px",
        "15": "60px",
        "16": "64px",
        "20": "80px",
        "25": "100px",
        "30": "120px"
      },
      "borderRadius": {
        "none": "0",
        "sm": "2px",
        "md": "6px",
        "lg": "8px",
        "xl": "12px",
        "2xl": "16px",
        "3xl": "100px",
        "full": "50%"
      },
      "boxShadow": {
        "xs": "0 0 0 0 rgba(245,158,11,0.6)",
        "sm": "0 0 0 0 rgba(220,38,38,0.30)",
        "DEFAULT": "0 0 0 0 rgba(220,38,38,0.25)",
        "md": "0 0 0 3px rgba(220,38,38,0.08)",
        "lg": "0 0 0 4px rgba(220,38,38,0.10)",
        "xl": "0 0 0 5px rgba(220,38,38,0.10)",
        "2xl": "0 1px 3px rgba(15,23,42,0.04),0 1px 2px rgba(15,23,42,0.02)"
      },
      "screens": {}
    }
  },
  "plugins": []
};
