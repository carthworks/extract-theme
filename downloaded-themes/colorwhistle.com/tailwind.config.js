/* Tailwind v3 config extracted from https://colorwhistle.com/ */
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
        "white-a0": "rgb(255 255 255 / 0.0)",
        "sky-200-a35": "rgb(5 131 216 / 0.349)",
        "red": {
          "600": "#e62f30",
          "400": "#fb6962",
          "500": "#fe2d2d"
        },
        "orange": {
          "400": "#ff6900",
          "200": "#fecda5"
        },
        "red-600": {
          "2": "#cf2e2e"
        },
        "slate": {
          "300": "#abb8c3",
          "600": "#6c757d"
        },
        "blue": {
          "600": "#0d6efd",
          "950": "#020381"
        },
        "sky": {
          "500": "#0693e3",
          "300": "#8ed1fc"
        },
        "emerald": {
          "400": "#00d084",
          "300": "#7bdcb5",
          "600": "#198754"
        },
        "yellow": {
          "300": "#fcb900",
          "50": "#fff5cb"
        },
        "purple": {
          "600": "#9b51e0"
        },
        "neutral": {
          "100": "#eeeeee",
          "950": "#212529",
          "200": "#d3d3d3",
          "50": "#f8f8f8"
        },
        "neutral-100": {
          "2": "#dee2e6"
        },
        "blue-600": {
          "2": "#0583d8"
        },
        "pink": {
          "300": "#f78da7",
          "500": "#ee2c82",
          "200": "#ffceec",
          "900": "#6b003e"
        },
        "neutral-950": {
          "2": "#333333"
        },
        "rose": {
          "600": "#dc3545"
        },
        "teal": {
          "200": "#4aeadc"
        },
        "violet": {
          "500": "#9778d1",
          "400": "#9896f0"
        },
        "fuchsia": {
          "600": "#cf2aba",
          "500": "#c751c0"
        },
        "yellow-50": {
          "2": "#fef84c"
        },
        "amber": {
          "200": "#ffcb70"
        },
        "indigo": {
          "700": "#4158d0"
        },
        "zinc": {
          "200": "#b6e3d4"
        },
        "cyan": {
          "400": "#33a7b5",
          "300": "#0dcaf0"
        },
        "lime": {
          "100": "#caf880"
        },
        "green": {
          "300": "#71ce7e"
        },
        "yellow-300": {
          "2": "#ffc107"
        },
        "background": "#ffffff",
        "foreground": "#000000",
        "muted-foreground": "#212529",
        "primary": "#e62f30",
        "accent": "#0d6efd",
        "border": "#abb8c3",
        "destructive": "#e62f30",
        "warning": "#fcb900",
        "success": "#00d084",
        "info": "#0693e3"
      },
      "fontFamily": {
        "sans": [
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "Noto Sans",
          "Liberation Sans",
          "sans-serif",
          "Apple Color Emoji",
          "Segoe UI Emoji",
          "Segoe UI Symbol",
          "Noto Color Emoji"
        ],
        "mono": [
          "SFMono-Regular",
          "Menlo",
          "Monaco",
          "Consolas",
          "Liberation Mono",
          "Courier New",
          "monospace"
        ],
        "sans-2": [
          "Source Sans Pro",
          "sans-serif"
        ],
        "sans-3": [
          "Material Symbols Outlined"
        ],
        "sans-4": [
          "Arial",
          "Helvetica",
          "sans-serif"
        ],
        "mono-2": [
          "monospace",
          "monospace"
        ],
        "mono-3": [
          "Courier 10 Pitch",
          "Courier",
          "monospace"
        ],
        "mono-4": [
          "Monaco",
          "Consolas",
          "Andale Mono",
          "DejaVu Sans Mono",
          "monospace"
        ]
      },
      "fontSize": {
        "xs": "13px",
        "sm": "14px",
        "base": "16px",
        "lg": "18px",
        "xl": "20px",
        "2xl": "24px",
        "3xl": "32px",
        "4xl": "42px",
        "5xl": "45px",
        "6xl": "4rem",
        "7xl": "5rem"
      },
      "fontWeight": {
        "semibold": "600",
        "normal": "400",
        "bold": "700",
        "light": "300",
        "medium": "500",
        "extrabold": "800"
      },
      "lineHeight": {
        "none": "1",
        "tight": "1.2",
        "snug": "1.4",
        "normal": "1.5",
        "relaxed": "1.6",
        "loose": "32px"
      },
      "letterSpacing": {
        "tighter": "-1px",
        "tight": "-.5px",
        "normal": "0",
        "wide": ".5px",
        "wider": "1.2px",
        "widest": ".12em"
      },
      "spacing": {
        "0": "0px",
        "2px": "2px",
        "1": "4px",
        "5px": "5px",
        "6px": "6px",
        "2": "8px",
        "9px": "9px",
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
        "8": "32px",
        "35px": "35px",
        "10": "40px",
        "12": "48px",
        "50px": "50px",
        "15": "60px",
        "20": "80px"
      },
      "borderRadius": {
        "none": "0",
        "sm": "3px",
        "DEFAULT": ".25rem",
        "md": "6px",
        "lg": "10px",
        "xl": "12px",
        "2xl": "20px",
        "3xl": "24px",
        "full": "50%"
      },
      "boxShadow": {
        "xs": "unset",
        "sm": "0 0 1px #fff0",
        "DEFAULT": "inset 0 -1px 0 rgba(0,0,0,.125)",
        "md": "0 0 0 3px rgb(217 119 6 / .12)",
        "lg": "0 0 0 .25rem rgba(13,110,253,.25)",
        "xl": "0 0 0 .25rem rgba(220,53,69,.25)",
        "2xl": "0 0 0 .25rem rgba(25,135,84,.25)"
      },
      "screens": {
        "sm": "576px",
        "sm-600": "600px",
        "md": "767px",
        "md-768": "768px",
        "md-769": "769px",
        "md-801": "801px",
        "lg": "992px",
        "lg-1024": "1024px",
        "lg-1110": "1110px",
        "xl": "1199px",
        "xl-1200": "1200px",
        "xl-1399": "1399px",
        "xl-1400": "1400px"
      }
    }
  },
  "plugins": []
};
