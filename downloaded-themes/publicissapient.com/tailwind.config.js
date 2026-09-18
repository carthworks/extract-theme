/* Tailwind v3 config extracted from https://www.publicissapient.com/ */
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
        "white-a33": "rgb(255 255 255 / 0.333)",
        "white-a0": "rgb(0 0 0 / 0.0)",
        "neutral-50-a5": "rgb(0 0 0 / 0.051)",
        "red": {
          "600": "#e90130",
          "800": "#9f0712"
        },
        "neutral": {
          "100": "#e5e7eb",
          "900": "#444444",
          "200": "#d1d5dc",
          "700": "#666666",
          "500": "#949494"
        },
        "blue": {
          "700": "#0c63ea",
          "500": "#2b7fff"
        },
        "slate": {
          "800": "#4a5565",
          "400": "#99a1af",
          "950": "#101828",
          "600": "#6a7282"
        },
        "slate-950": {
          "2": "#030712",
          "3": "#1e2939"
        },
        "yellow": {
          "100": "#fee685"
        },
        "orange": {
          "400": "#ff6900"
        },
        "green": {
          "400": "#00c950"
        },
        "background": "#ffffff",
        "foreground": "#000000",
        "muted-foreground": "#444444",
        "primary": "#e90130",
        "accent": "#0c63ea",
        "border": "#e5e7eb",
        "destructive": "#e90130",
        "success": "#00c950"
      },
      "fontFamily": {
        "sans": [
          "ui-sans-serif",
          "system-ui",
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
        ]
      },
      "fontSize": {
        "xs": "11px",
        "sm": "14px",
        "base": "1rem",
        "lg": "1.125rem",
        "xl": "22px",
        "2xl": "1.5rem",
        "3xl": "28px",
        "4xl": "42px",
        "5xl": "50px",
        "6xl": "3.75rem",
        "7xl": "4.5rem"
      },
      "fontWeight": {
        "normal": "400",
        "bold": "700",
        "light": "300",
        "medium": "500",
        "semibold": "600"
      },
      "lineHeight": {
        "none": "1",
        "tight": "1.25em",
        "snug": "1.33333",
        "normal": "1.5",
        "loose": "30px"
      },
      "letterSpacing": {
        "tighter": "-2.4px",
        "tight": "-.025em",
        "wide": ".025em",
        "wider": ".05em",
        "widest": ".1em"
      },
      "spacing": {
        "0": "0px",
        "1px": "1px",
        "1_6px": "1.6px",
        "2px": "2px",
        "1": "4px",
        "5px": "5px",
        "6px": "6px",
        "7px": "7px",
        "2": "8px",
        "9_71px": "9.71px",
        "10px": "10px",
        "3": "12px",
        "4": "16px",
        "19px": "19px",
        "5": "20px",
        "6": "24px",
        "7": "28px",
        "30px": "30px",
        "8": "32px",
        "10": "40px",
        "12": "48px",
        "16": "64px",
        "20": "80px"
      },
      "borderRadius": {
        "none": "0",
        "sm": "3px",
        "DEFAULT": ".25rem",
        "md": ".375rem",
        "lg": ".5rem",
        "xl": ".75rem",
        "2xl": "1rem",
        "3xl": "1.5rem",
        "full": "9999px"
      },
      "boxShadow": {
        "xs": "0 0 #0000,0 0 #0000,inset0 0 0 2px#fff,inset0 0 0 calc(2px + 2px)#e90130,0 0 #0000",
        "sm": "inset 0 0 0 1px #000",
        "DEFAULT": "inset 0 0 0 1px #0000",
        "md": "inset 0 0 0 1px #e90130",
        "lg": "0 0 1px #888",
        "xl": "0 0 1px #0003",
        "2xl": "0 0 0 2px #0c63ea"
      },
      "screens": {
        "sm": "360px",
        "sm-639": "639px",
        "sm-640": "640px",
        "sm-672": "672px",
        "md": "768px",
        "lg": "1024px",
        "xl": "1153px",
        "xl-1280": "1280px",
        "xl-1281": "1281px",
        "xl-1356": "1356px",
        "2xl": "1536px"
      }
    }
  },
  "plugins": []
};
