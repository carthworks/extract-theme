/* Tailwind v3 config extracted from https://appark.ai/ */
/** @type {import('tailwindcss').Config} */
module.exports = {
  "content": [
    "./src/**/*.{js,ts,jsx,tsx,html}"
  ],
  "theme": {
    "extend": {
      "colors": {
        "white": "#ffffff",
        "neutral-950-a88": "rgb(0 0 0 / 0.88)",
        "neutral-300-a25": "rgb(0 0 0 / 0.25)",
        "neutral-50-a4": "rgb(0 0 0 / 0.04)",
        "neutral-500-a45": "rgb(0 0 0 / 0.451)",
        "stone-300-a40": "rgb(113 63 18 / 0.4)",
        "black": "#000000",
        "neutral-800-a65": "rgb(0 0 0 / 0.651)",
        "white-a0": "rgb(239 246 255 / 0.0)",
        "neutral-50-a5": "rgb(9 92 255 / 0.051)",
        "neutral-200-a15": "rgb(0 0 0 / 0.15)",
        "neutral-50-a60": "rgb(229 231 235 / 0.6)",
        "neutral": {
          "50": "#f0f0f0",
          "200": "#d9d9d9",
          "500": "#8c8c8c"
        },
        "blue": {
          "600": "#1677ff",
          "400": "#4096ff",
          "500": "#3b82f6",
          "700": "#0958d9",
          "300": "#91caff"
        },
        "red": {
          "400": "#ff4d4f",
          "600": "#d9363e",
          "500": "#ef4444",
          "300": "#ffa39e"
        },
        "slate": {
          "400": "#9ca3af",
          "800": "#475569",
          "950": "#111827",
          "100": "#dbeafe",
          "900": "#334155",
          "600": "#64748b"
        },
        "red-400": {
          "2": "#ff7875"
        },
        "slate-950": {
          "2": "#1e293b"
        },
        "amber": {
          "300": "#faad14"
        },
        "blue-400": {
          "2": "#60a5fa"
        },
        "blue-600": {
          "2": "#2563eb"
        },
        "lime": {
          "400": "#52c41a"
        },
        "orange": {
          "400": "#f97316"
        },
        "green": {
          "400": "#22c55e",
          "700": "#15803d"
        },
        "yellow": {
          "50": "#fef3c7"
        },
        "background": "#ffffff",
        "foreground": "#000000",
        "muted-foreground": "#475569",
        "primary": "#1677ff",
        "accent": "#ff4d4f",
        "border": "#f0f0f0",
        "destructive": "#ff4d4f",
        "warning": "#faad14",
        "success": "#52c41a",
        "info": "#4096ff"
      },
      "fontFamily": {
        "sans": [
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "Noto Sans",
          "sans-serif",
          "Apple Color Emoji",
          "Segoe UI Emoji",
          "Segoe UI Symbol",
          "Noto Color Emoji"
        ],
        "mono": [
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Monaco",
          "Consolas",
          "Liberation Mono",
          "Courier New",
          "monospace"
        ],
        "sans-2": [
          "ui-sans-serif",
          "system-ui",
          "sans-serif",
          "Apple Color Emoji",
          "Segoe UI Emoji",
          "Segoe UI Symbol",
          "Noto Color Emoji"
        ],
        "sans-3": [
          "-apple-system",
          "BlinkMacSystemFont",
          "PingFang SC",
          "Hiragino Sans GB",
          "Microsoft YaHei",
          "Segoe UI",
          "Roboto",
          "Oxygen",
          "Ubuntu",
          "Cantarell",
          "Open Sans",
          "Helvetica Neue",
          "sans-serif"
        ],
        "sans-4": [
          "Arial",
          "Helvetica",
          "sans-serif"
        ],
        "mono-2": [
          "monospace",
          "monospace"
        ]
      },
      "fontSize": {
        "xs": "12px",
        "sm": "14px",
        "base": "16px",
        "lg": "18px",
        "xl": "1.25rem",
        "2xl": "1.5rem",
        "3xl": "1.875rem",
        "4xl": "2.25rem",
        "5xl": "3rem"
      },
      "fontWeight": {
        "semibold": "600",
        "medium": "500",
        "bold": "700",
        "normal": "400",
        "black": "900"
      },
      "lineHeight": {
        "none": "1",
        "tight": "1.25rem",
        "snug": "22px",
        "normal": "1.5",
        "relaxed": "1.5714285714285714",
        "loose": "30px"
      },
      "letterSpacing": {
        "tight": "-.025em",
        "normal": "0",
        "wider": ".05em",
        "widest": "2px"
      },
      "spacing": {
        "0": "0px",
        "1px": "1px",
        "2px": "2px",
        "1": "4px",
        "6px": "6px",
        "7px": "7px",
        "2": "8px",
        "10px": "10px",
        "11px": "11px",
        "3": "12px",
        "14px": "14px",
        "4": "16px",
        "18px": "18px",
        "5": "20px",
        "6": "24px",
        "7": "28px",
        "8": "32px",
        "10": "40px",
        "46px": "46px",
        "12": "48px",
        "14": "56px",
        "16": "64px",
        "20": "80px",
        "40": "160px"
      },
      "borderRadius": {
        "none": "0",
        "sm": "3px",
        "DEFAULT": "4px",
        "md": "6px",
        "lg": "8px",
        "xl": "12px",
        "2xl": "1rem",
        "3xl": "28px",
        "full": "50%"
      },
      "boxShadow": {
        "xs": "0 0 0 0 currentcolor",
        "sm": "0 0 0 2px rgba(5, 145, 255, 0.1)",
        "DEFAULT": "0 0 0 2px rgba(255, 38, 5, 0.06)",
        "md": "0 0 0 2px rgba(255, 215, 5, 0.1)",
        "lg": "0 2px 0 rgba(0, 0, 0, 0.02)",
        "xl": "0 0 0 2px #1890ff33",
        "2xl": "0 2px 0 rgba(5, 145, 255, 0.1)"
      },
      "screens": {
        "sm": "640px",
        "md": "768px",
        "lg": "1024px",
        "xl": "1200px",
        "xl-1280": "1280px",
        "2xl": "1480px",
        "2xl-1536": "1536px"
      }
    }
  },
  "plugins": []
};
