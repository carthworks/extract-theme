/* Tailwind v3 config extracted from https://whetstone-cyber.in/ */
/** @type {import('tailwindcss').Config} */
module.exports = {
  "content": [
    "./src/**/*.{js,ts,jsx,tsx,html}"
  ],
  "theme": {
    "extend": {
      "colors": {
        "white": "#ffffff",
        "white-a0": "rgb(255 255 255 / 0.0)",
        "black": "#000000",
        "neutral-50-a4": "rgb(0 0 0 / 0.035)",
        "cyan-400-a54": "rgb(2 113 130 / 0.54)",
        "slate-400-a55": "rgb(0 79 99 / 0.55)",
        "neutral-300-a30": "rgb(0 0 0 / 0.3)",
        "slate": {
          "950": "#1b2f45",
          "900": "#374951",
          "600": "#69727d",
          "300": "#abb8c3"
        },
        "neutral": {
          "50": "#f1f1f1",
          "950": "#121010",
          "800": "#555555",
          "200": "#dddddd",
          "300": "#cccccc",
          "100": "#e7e7e7",
          "500": "#929292"
        },
        "neutral-950": {
          "2": "#333333",
          "3": "#222222"
        },
        "blue": {
          "600": "#2575fc"
        },
        "sky": {
          "400": "#13aff0",
          "500": "#0693e3",
          "600": "#41788c",
          "700": "#2d657a",
          "300": "#8ed1fc"
        },
        "orange": {
          "400": "#ff6900"
        },
        "green": {
          "200": "#29f48f",
          "300": "#61ce70"
        },
        "red": {
          "600": "#cf2e2e",
          "500": "#fe2d2d",
          "300": "#fe8f75"
        },
        "teal": {
          "600": "#238c8c"
        },
        "yellow": {
          "300": "#fcb900"
        },
        "purple": {
          "600": "#9b51e0"
        },
        "emerald": {
          "300": "#4ce09d",
          "400": "#00d084"
        },
        "emerald-300": {
          "2": "#7bdcb5"
        },
        "pink": {
          "300": "#f78da7"
        },
        "zinc": {
          "200": "#b6e3d4"
        },
        "background": "#ffffff",
        "foreground": "#374951",
        "muted-foreground": "#555555",
        "primary": "#2575fc",
        "accent": "#13aff0",
        "border": "#f1f1f1",
        "destructive": "#ff6900",
        "warning": "#fcb900",
        "success": "#61ce70",
        "info": "#13aff0"
      },
      "fontFamily": {
        "sans": [
          "Gabarito",
          "Sans-serif"
        ],
        "serif": [
          "Playfair Display",
          "serif"
        ],
        "mono": [
          "Courier New",
          "Courier",
          "monospace"
        ],
        "sans-2": [
          "Gabarito"
        ],
        "sans-3": [
          "Cairo",
          "Sans-serif"
        ],
        "sans-4": [
          "Font Awesome 5 Free"
        ],
        "mono-2": [
          "Arial",
          "Baskerville",
          "monospace"
        ],
        "mono-3": [
          "monospace",
          "monospace"
        ]
      },
      "fontSize": {
        "xs": "13px",
        "sm": "14px",
        "base": "1em",
        "lg": "18px",
        "xl": "20px",
        "2xl": "1.5em",
        "3xl": "1.8em",
        "4xl": "42px",
        "5xl": "3em",
        "6xl": "4em",
        "7xl": "69px"
      },
      "fontWeight": {
        "normal": "400",
        "medium": "500",
        "semibold": "600",
        "bold": "700",
        "black": "900",
        "light": "300"
      },
      "lineHeight": {
        "none": "1",
        "tight": "1.2em",
        "snug": "1.4",
        "normal": "normal",
        "relaxed": "1.6em",
        "loose": "40px"
      },
      "letterSpacing": {
        "tighter": "-6px",
        "tight": "-.4px",
        "normal": "0",
        "wide": ".6px",
        "wider": "1px",
        "widest": ".1em"
      },
      "spacing": {
        "0": "0px",
        "2px": "2px",
        "3px": "3px",
        "1": "4px",
        "5px": "5px",
        "6px": "6px",
        "2": "8px",
        "10px": "10px",
        "3": "12px",
        "14px": "14px",
        "15px": "15px",
        "4": "16px",
        "18px": "18px",
        "5": "20px",
        "6": "24px",
        "25px": "25px",
        "30px": "30px",
        "31px": "31px",
        "8": "32px",
        "10": "40px",
        "12": "48px",
        "50px": "50px",
        "16": "64px",
        "20": "80px"
      },
      "borderRadius": {
        "none": "0",
        "sm": "3px",
        "DEFAULT": "5px",
        "md": "6px",
        "lg": "10px",
        "xl": "14px",
        "2xl": "15px",
        "3xl": "30px",
        "full": "50%"
      },
      "boxShadow": {
        "xs": "0 0 0 0 currentColor",
        "sm": "0 0 0 0 rgb(12 90 219 / .2)",
        "DEFAULT": "0 0 0 0 #fff0",
        "md": "inset 0 0 0 1px currentColor",
        "lg": "inset 0 0 0 1px rgb(0 0 0 / .1)",
        "xl": "inset 0 0 0 1px rgba(0,0,0,.1)",
        "2xl": "0 0 0 2px rgb(51 51 51 / .1)"
      },
      "screens": {
        "sm": "480px",
        "sm-481": "481px",
        "sm-568": "568px",
        "md": "766px",
        "md-767": "767px",
        "md-768": "768px",
        "lg": "959px",
        "lg-992": "992px",
        "lg-1025": "1025px"
      }
    }
  },
  "plugins": []
};
