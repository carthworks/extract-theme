/* Tailwind v3 config extracted from https://runevr.com/ */
/** @type {import('tailwindcss').Config} */
module.exports = {
  "content": [
    "./src/**/*.{js,ts,jsx,tsx,html}"
  ],
  "theme": {
    "extend": {
      "colors": {
        "white": "#ffffff",
        "black": "#000000",
        "white-a0": "rgb(0 0 0 / 0.0)",
        "white-a78": "rgb(255 255 255 / 0.78)",
        "fuchsia": {
          "600": "#ba00d9",
          "300": "#f0abfc"
        },
        "neutral": {
          "100": "#ececf1",
          "600": "#808080",
          "950": "#1a1a1a",
          "400": "#a7a7a7",
          "200": "#d1d5dc"
        },
        "sky": {
          "600": "#0085cf",
          "400": "#38bdf8"
        },
        "slate": {
          "950": "#0f172b",
          "200": "#e3d9f8",
          "700": "#5b5b6b",
          "900": "#364153",
          "400": "#99a1af",
          "800": "#4a5565"
        },
        "cyan": {
          "300": "#39c8eb",
          "200": "#67e8f9"
        },
        "slate-950": {
          "2": "#0b0b14"
        },
        "violet": {
          "600": "#7c3aed",
          "300": "#c4b5fd"
        },
        "purple": {
          "900": "#59168b",
          "600": "#9810fa",
          "700": "#8200db",
          "500": "#ad46ff"
        },
        "emerald": {
          "200": "#a7f3d0"
        },
        "rose": {
          "300": "#fca5a5"
        },
        "green": {
          "300": "#4bde5c"
        },
        "slate-200": {
          "2": "#c6e2f8"
        },
        "yellow": {
          "100": "#fee685",
          "300": "#fbbf24"
        },
        "blue": {
          "400": "#60a5fa",
          "500": "#2b7fff"
        },
        "lime": {
          "300": "#a1d45e"
        },
        "amber": {
          "300": "#fe9a00"
        },
        "indigo": {
          "400": "#818cf8",
          "300": "#a5b4fc"
        },
        "background": "#ffffff",
        "foreground": "#0b0b14",
        "muted-foreground": "#0f172b",
        "primary": "#ba00d9",
        "accent": "#0085cf",
        "border": "#ececf1",
        "destructive": "#fca5a5",
        "warning": "#fbbf24",
        "success": "#4bde5c",
        "info": "#0085cf"
      },
      "fontFamily": {
        "sans": [
          "Instrument Sans",
          "sans-serif"
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
          "Twemoji",
          "Inter",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "sans-serif"
        ],
        "sans-3": [
          "Instrument Sans",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Roboto",
          "sans-serif"
        ],
        "sans-4": [
          "Inter",
          "system-ui",
          "sans-serif"
        ]
      },
      "fontSize": {
        "xs": "13px",
        "sm": "14.5px",
        "base": "16px",
        "lg": "18px",
        "xl": "1.25rem",
        "2xl": "24px",
        "3xl": "1.875rem",
        "4xl": "2.25rem",
        "5xl": "3rem",
        "6xl": "64px",
        "7xl": "72px"
      },
      "fontWeight": {
        "semibold": "600",
        "normal": "400",
        "medium": "500",
        "bold": "700"
      },
      "lineHeight": {
        "none": "18px",
        "tight": "21px",
        "snug": "1.375",
        "normal": "1.5",
        "relaxed": "28px"
      },
      "letterSpacing": {
        "tighter": "-1px",
        "tight": "-.03em",
        "normal": "-0.01em",
        "wide": ".025em",
        "wider": ".05em",
        "widest": ".08em"
      },
      "spacing": {
        "0": "0px",
        "1px": "1px",
        "2px": "2px",
        "3px": "3px",
        "1": "4px",
        "5px": "5px",
        "6px": "6px",
        "7px": "7px",
        "2": "8px",
        "10px": "10px",
        "11px": "11px",
        "13_6px": "13.6px",
        "4": "16px",
        "18px": "18px",
        "5": "20px",
        "21px": "21px",
        "22px": "22px",
        "6": "24px",
        "26px": "26px",
        "37px": "37px",
        "10": "40px",
        "13": "52px",
        "14": "56px",
        "15": "60px"
      },
      "borderRadius": {
        "none": "0",
        "sm": "2px",
        "DEFAULT": ".25rem",
        "md": "6px 6px 6px 6px",
        "lg": ".6rem",
        "xl": ".75rem",
        "2xl": "18px",
        "3xl": "22px",
        "full": "9999px"
      },
      "boxShadow": {
        "xs": "0 0 6px 2px #6BA9FE90",
        "sm": "0 0 6px 2px #C084FC90",
        "DEFAULT": "0 0 6px 2px #34D39990",
        "md": "0 0 6px 2px #A78BFA90",
        "lg": "0 0 6px 2px #F59E0B90",
        "xl": "9px 6px 11px rgba(0, 0, 0, 0.21)",
        "2xl": "0 6px 24px #0b0b140d"
      },
      "screens": {
        "sm": "640px",
        "md": "768px",
        "lg": "1024px",
        "xl": "1280px",
        "2xl": "1536px"
      }
    }
  },
  "plugins": []
};
