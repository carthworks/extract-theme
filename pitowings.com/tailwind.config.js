/* Tailwind v3 config extracted from https://www.pitowings.com */
/** @type {import('tailwindcss').Config} */
module.exports = {
  "content": [
    "./src/**/*.{js,ts,jsx,tsx,html}"
  ],
  "theme": {
    "extend": {
      "colors": {
        "white": "#ffffff",
        "white-a0": {
          "2": "rgb(0 0 0 / 0.0)",
          "3": "rgb(225 29 63 / 0.0)"
        },
        "stone-100-a14": "rgb(225 29 63 / 0.139)",
        "stone-50-a8": "rgb(225 29 63 / 0.076)",
        "stone-200-a20": "rgb(225 29 63 / 0.197)",
        "white-a35": "rgb(255 255 255 / 0.35)",
        "white-a70": "rgb(255 255 255 / 0.702)",
        "neutral-50-a6": "rgb(200 16 46 / 0.059)",
        "white-a80": "rgb(255 255 255 / 0.8)",
        "stone-100-a80": "rgb(255 224 228 / 0.8)",
        "neutral-50-a50": "rgb(255 241 243 / 0.502)",
        "neutral-50-a4": "rgb(246 90 118 / 0.043)",
        "white-a40": "rgb(255 255 255 / 0.4)",
        "stone-50-a30": "rgb(255 198 207 / 0.302)",
        "white-a10": "rgb(255 255 255 / 0.102)",
        "white-a95": "rgb(255 255 255 / 0.949)",
        "white-a85": "rgb(255 255 255 / 0.851)",
        "stone-100-a70": "rgb(255 224 228 / 0.702)",
        "stone-100-a50": "rgb(255 198 207 / 0.502)",
        "neutral-50-a40": {
          "2": "rgb(255 224 228 / 0.4)"
        },
        "neutral-50-a60": "rgb(255 241 243 / 0.6)",
        "neutral-50-a80": "rgb(255 241 243 / 0.8)",
        "stone-50-a45": "rgb(255 224 228 / 0.451)",
        "stone-50-a50": "rgb(255 224 228 / 0.502)",
        "stone-50-a60": "rgb(255 224 228 / 0.6)",
        "stone-100-a40": "rgb(255 198 207 / 0.4)",
        "stone": {
          "100": "#ffe0e4",
          "50": "#fff1f3",
          "950": "#3a2f35",
          "700": "#6b5b62"
        },
        "rose": {
          "200": "#ffc6cf",
          "600": "#e11d3f",
          "300": "#ff9aab",
          "800": "#a50d26",
          "400": "#f65a76",
          "700": "#c8102e",
          "900": "#7a0c1f",
          "950": "#5c0a17"
        },
        "neutral": {
          "100": "#f3e9ea",
          "950": "#1b1418"
        },
        "zinc": {
          "400": "#a999aa"
        },
        "red": {
          "500": "#fb2c36",
          "600": "#e7000b"
        },
        "rose-400": {
          "2": "#ff6467"
        },
        "stone-100": {
          "2": "#ffe6da"
        },
        "background": "#ffffff",
        "foreground": "#1b1418",
        "muted-foreground": "#3a2f35",
        "primary": "#e11d3f",
        "accent": "#ff9aab",
        "border": "#ffe0e4",
        "destructive": "#e11d3f"
      },
      "fontFamily": {
        "sans": [
          "Poppins",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Roboto",
          "Helvetica",
          "Arial",
          "sans-serif"
        ],
        "mono": [
          "ui-monospace",
          "SFMono-Regular",
          "SF Mono",
          "Menlo",
          "Consolas",
          "Liberation Mono",
          "Courier New",
          "monospace"
        ]
      },
      "fontSize": {
        "xs": ".75rem",
        "sm": ".875rem",
        "base": "1rem",
        "lg": "1.125rem",
        "xl": "1.25rem",
        "2xl": "1.5rem",
        "3xl": "1.875rem",
        "4xl": "2.25rem",
        "5xl": "3rem",
        "6xl": "3.75rem",
        "7xl": "4.5rem"
      },
      "fontWeight": {
        "medium": "500",
        "semibold": "600",
        "bold": "700",
        "extrabold": "800",
        "black": "900"
      },
      "lineHeight": {
        "none": "1",
        "tight": "1.25",
        "snug": "1.375",
        "normal": "1.5",
        "relaxed": "1.65"
      },
      "letterSpacing": {
        "tight": "-.025em",
        "normal": "0em",
        "wide": ".025em",
        "wider": ".06em",
        "widest": ".1em"
      },
      "spacing": {
        "0": "0px",
        "1px": "1px",
        "2_56px": "2.56px",
        "3px": "3px",
        "1": "4px",
        "4_48px": "4.48px",
        "4_8px": "4.8px",
        "8_8px": "8.8px",
        "9_6px": "9.6px",
        "14_4px": "14.4px",
        "17_6px": "17.6px",
        "5": "20px",
        "23_2px": "23.2px",
        "27px": "27px",
        "7": "28px",
        "50_4px": "50.4px",
        "13": "52px",
        "62_4px": "62.4px",
        "70_4px": "70.4px"
      },
      "borderRadius": {
        "none": "0",
        "DEFAULT": ".25rem",
        "lg": ".5rem",
        "xl": ".75rem",
        "2xl": "1rem",
        "3xl": "1.5rem"
      },
      "boxShadow": {
        "xs": "0 0 #0000,0 0 #0000,0 0 #0000,initial 0 0 0 calc(4px + 0px) oklch(93.6% .032 17.717),0 8px 24px -16px initial",
        "sm": "0 20px 50px -28px #1b141859",
        "DEFAULT": "0 22px 60px -22px #c8102e73"
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
