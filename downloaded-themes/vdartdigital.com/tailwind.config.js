/* Tailwind v3 config extracted from https://www.vdartdigital.com/ */
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
        "white-a0": {
          "2": "rgb(0 0 0 / 0.0)"
        },
        "sky": {
          "950": "#003049",
          "500": "#0693e3",
          "300": "#00c9ff"
        },
        "neutral": {
          "100": "#eeeeee",
          "950": "#232323",
          "700": "#616161",
          "200": "#d2d2d2",
          "400": "#999999",
          "900": "#444444",
          "600": "#777777"
        },
        "rose": {
          "600": "#e91e63"
        },
        "neutral-950": {
          "2": "#333333"
        },
        "orange": {
          "400": "#ff6900"
        },
        "violet": {
          "700": "#7347db",
          "950": "#330072"
        },
        "red": {
          "600": "#cf2e2e",
          "500": "#fe2d2d"
        },
        "yellow": {
          "300": "#fcb900",
          "200": "#fddd00",
          "50": "#fff5cb"
        },
        "slate": {
          "300": "#abb8c3",
          "700": "#636e78",
          "900": "#293e4b"
        },
        "emerald": {
          "400": "#00d084",
          "300": "#7bdcb5"
        },
        "purple": {
          "600": "#9b51e0"
        },
        "pink": {
          "700": "#a81d84",
          "300": "#f78da7"
        },
        "neutral-200": {
          "2": "#dddddd"
        },
        "fuchsia": {
          "700": "#9c27b0"
        },
        "emerald-300": {
          "2": "#62d69e"
        },
        "sky-300": {
          "2": "#8ed1fc"
        },
        "blue": {
          "600": "#2874fc"
        },
        "blue-600": {
          "2": "#007acc"
        },
        "rose-600": {
          "2": "#ea0048"
        },
        "yellow-50": {
          "2": "#fef84c"
        },
        "background": "#ffffff",
        "foreground": "#000000",
        "muted-foreground": "#232323",
        "primary": "#003049",
        "accent": "#e91e63",
        "border": "#eeeeee",
        "destructive": "#e91e63",
        "warning": "#fcb900",
        "success": "#00d084",
        "info": "#0693e3"
      },
      "fontFamily": {
        "sans": [
          "Proxima-nova",
          "sans-serif"
        ],
        "serif": [
          "Roboto Slab",
          "Times New Roman",
          "serif"
        ],
        "mono": [
          "monospace",
          "monospace"
        ],
        "sans-2": [
          "Proxima-nova",
          "sans-serif"
        ],
        "sans-3": [
          "Proxima-nova",
          "Sans-serif"
        ],
        "sans-4": [
          "proxima-nova",
          "sans-serif"
        ],
        "serif-2": [
          "Georgia",
          "Proxima-nova",
          "Times",
          "serif"
        ],
        "mono-2": [
          "Menlo",
          "Monaco",
          "Consolas",
          "Courier New",
          "monospace"
        ]
      },
      "fontSize": {
        "xs": "12px",
        "sm": "14px",
        "base": "16px",
        "lg": "18px",
        "xl": "20px",
        "2xl": "24px",
        "3xl": "30px",
        "4xl": "40px",
        "5xl": "50px",
        "6xl": "60px",
        "9xl": "8rem"
      },
      "fontWeight": {
        "normal": "400",
        "bold": "700",
        "extrabold": "800",
        "semibold": "600",
        "medium": "500",
        "black": "900",
        "light": "300"
      },
      "lineHeight": {
        "none": "1em",
        "tight": "20px",
        "snug": "22px",
        "normal": "24px",
        "relaxed": "28px",
        "loose": "46px"
      },
      "letterSpacing": {
        "normal": "0",
        "wide": ".4px",
        "wider": "0.84px",
        "widest": ".1em"
      },
      "spacing": {
        "0": "0px",
        "2px": "2px",
        "3px": "3px",
        "1": "4px",
        "5px": "5px",
        "6px": "6px",
        "7px": "7px",
        "2": "8px",
        "10px": "10px",
        "3": "12px",
        "14_85px": "14.85px",
        "15px": "15px",
        "4": "16px",
        "17px": "17px",
        "5": "20px",
        "6": "24px",
        "25px": "25px",
        "29_71px": "29.71px",
        "30px": "30px",
        "34px": "34px",
        "10": "40px",
        "50px": "50px",
        "15": "60px",
        "70px": "70px"
      },
      "borderRadius": {
        "none": "0px",
        "sm": "3px",
        "DEFAULT": "5px",
        "md": "7px",
        "lg": "10px",
        "2xl": "20px",
        "3xl": "30px",
        "full": "50%"
      },
      "boxShadow": {
        "xs": "inset 0 -1px 0 rgb(0 0 0 / .25)",
        "sm": "inset 0 1px 0 rgb(255 255 255 / .1)",
        "DEFAULT": "inset 0 0 0 1px rgb(0 0 0 / .1)",
        "md": "inset 0 1px 1px rgb(0 0 0 / .075)",
        "lg": "inset 0 1px 0 rgb(255 255 255 / .1),0 1px 0 rgb(255 255 255 / .1)",
        "xl": "0 0 2px 2px rgb(0 0 0 / .6)",
        "2xl": "0 0 5px rgb(0 0 0 / .3)"
      },
      "screens": {
        "sm": "480px",
        "sm-481": "481px",
        "sm-601": "601px",
        "sm-640": "640px",
        "sm-641": "641px",
        "md": "749px",
        "md-768": "768px",
        "md-769": "769px",
        "md-783": "783px",
        "md-820": "820px",
        "lg": "960px",
        "lg-992": "992px",
        "lg-1025": "1025px",
        "xl": "1200px",
        "2xl": "1600px"
      }
    }
  },
  "plugins": []
};
