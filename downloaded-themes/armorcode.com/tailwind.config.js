/* Tailwind v3 config extracted from https://www.armorcode.com/ */
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
        "slate": {
          "50": "#f3f3ff",
          "200": "#cbd5e1",
          "300": "#abb8c3",
          "900": "#334155",
          "950": "#0f172a",
          "600": "#64748b",
          "800": "#475569",
          "100": "#c2e9ff",
          "400": "#94a3b8"
        },
        "indigo": {
          "700": "#5f36f1",
          "800": "#5025dc",
          "900": "#35198e"
        },
        "orange": {
          "400": "#ff6900"
        },
        "amber": {
          "300": "#f99c07"
        },
        "violet": {
          "400": "#a183fa",
          "200": "#d6d5ff",
          "600": "#7259f9",
          "700": "#7a00df"
        },
        "stone": {
          "50": "#fbf5df",
          "100": "#ffe5e1"
        },
        "sky": {
          "500": "#0693e3",
          "600": "#0082cd"
        },
        "emerald": {
          "400": "#00d084",
          "300": "#7bdcb5"
        },
        "red": {
          "600": "#cf2e2e",
          "500": "#d66b5d",
          "200": "#ffccc5"
        },
        "yellow": {
          "300": "#fcb900",
          "50": "#fff0b8"
        },
        "purple": {
          "600": "#9b51e0"
        },
        "rose": {
          "600": "#df2a4a"
        },
        "neutral": {
          "100": "#e2e8f0"
        },
        "zinc": {
          "50": "#defae8"
        },
        "green": {
          "300": "#6cdc92",
          "600": "#1e9b49"
        },
        "pink": {
          "400": "#f084b8",
          "600": "#d32f71"
        },
        "violet-600": {
          "2": "#8b5cf6"
        },
        "background": "#ffffff",
        "foreground": "#334155",
        "muted-foreground": "#64748b",
        "primary": "#5f36f1",
        "accent": "#ff6900",
        "border": "#f3f3ff",
        "destructive": "#ff6900",
        "warning": "#f99c07",
        "success": "#00d084",
        "info": "#0693e3"
      },
      "fontFamily": {
        "sans": [
          "MatterSQ",
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
        ]
      },
      "fontSize": {
        "xs": "13px",
        "sm": ".875rem",
        "base": "1rem",
        "lg": "1.125rem",
        "xl": "1.25rem",
        "2xl": "1.5rem",
        "3xl": "2rem",
        "4xl": "42px",
        "5xl": "3rem",
        "6xl": "3.5rem",
        "8xl": "6rem",
        "9xl": "8.4em"
      },
      "fontWeight": {
        "semibold": "600",
        "normal": "400",
        "medium": "500",
        "thin": "100",
        "light": "300"
      },
      "lineHeight": {
        "none": "1",
        "tight": "1.2",
        "snug": "1.4",
        "normal": "1.5",
        "relaxed": "1.6",
        "loose": "2.5"
      },
      "letterSpacing": {
        "tighter": "-1px",
        "tight": "-0.5px",
        "normal": "0px",
        "widest": "2px"
      },
      "spacing": {
        "0": "0px",
        "0_8px": "0.8px",
        "1_6px": "1.6px",
        "2px": "2px",
        "1": "4px",
        "5px": "5px",
        "2": "8px",
        "10px": "10px",
        "10_67px": "10.67px",
        "3": "12px",
        "14px": "14px",
        "15px": "15px",
        "4": "16px",
        "5": "20px",
        "21_33px": "21.33px",
        "23px": "23px",
        "6": "24px",
        "8": "32px",
        "38px": "38px",
        "10": "40px",
        "12": "48px",
        "14": "56px",
        "16": "64px",
        "20": "80px"
      },
      "borderRadius": {
        "none": "0",
        "DEFAULT": "4px",
        "md": ".375rem",
        "lg": ".5rem",
        "xl": ".75rem",
        "2xl": "1rem",
        "3xl": "1.5rem",
        "full": "9999px"
      },
      "boxShadow": {
        "xs": "0 0 0 5px #19f",
        "sm": "inset 0 0 0 2px #fff,inset 0 0 0 calc(2px + 2px) rgb(95 54 241 / 1),0 1px 3px -1px rgb(15 23 42 / .1), 0 0 1px rgb(15 23 42 / .1)",
        "DEFAULT": "0 17.579px 41.018px -17.579px rgba(68, 68, 68, 0.16)"
      },
      "screens": {
        "sm": "640px",
        "md": "768px",
        "md-782": "782px",
        "lg": "960px",
        "lg-992": "992px",
        "lg-1024": "1024px",
        "xl": "1200px",
        "xl-1280": "1280px",
        "xl-1360": "1360px"
      }
    }
  },
  "plugins": []
};
