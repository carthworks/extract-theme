/* Tailwind v3 config extracted from https://www.pitowings.com/ */
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
          "2": "rgb(0 0 0 / 0.0)"
        },
        "stone-100-a14": "rgb(225 29 63 / 0.139)",
        "stone-50-a8": "rgb(225 29 63 / 0.076)",
        "white-a35": "rgb(255 255 255 / 0.35)",
        "stone": {
          "100": "#ffe0e4"
        },
        "rose": {
          "600": "#e11d3f",
          "200": "#ffc6cf",
          "400": "#f65a76",
          "300": "#ff9aab",
          "800": "#a50d26",
          "700": "#c8102e"
        },
        "neutral": {
          "950": "#1b1418"
        },
        "zinc": {
          "400": "#a999aa"
        },
        "background": "#ffffff",
        "foreground": "#1b1418",
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
