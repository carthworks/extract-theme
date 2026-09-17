/* Tailwind v3 config extracted from https://texmo.com/ */
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
        "neutral-300-a30": "rgb(0 0 0 / 0.3)",
        "orange": {
          "400": "#ff6900",
          "500": "#e55e20",
          "200": "#fecda5"
        },
        "red": {
          "600": "#cf2e2e",
          "500": "#fe2d2d",
          "400": "#fb6962"
        },
        "slate": {
          "300": "#abb8c3",
          "950": "#181822"
        },
        "yellow": {
          "300": "#fcb900",
          "50": "#fef84c"
        },
        "sky": {
          "500": "#0693e3",
          "300": "#8ed1fc"
        },
        "purple": {
          "600": "#9b51e0"
        },
        "emerald": {
          "300": "#7bdcb5",
          "400": "#00d084"
        },
        "pink": {
          "300": "#f78da7",
          "500": "#ee2c82",
          "200": "#ffceec",
          "900": "#6b003e"
        },
        "neutral": {
          "900": "#32373c",
          "100": "#eeeeee",
          "200": "#dbdbdb"
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
        "amber": {
          "200": "#ffcb70"
        },
        "indigo": {
          "700": "#4158d0"
        },
        "yellow-50": {
          "2": "#fff5cb"
        },
        "zinc": {
          "200": "#b6e3d4"
        },
        "cyan": {
          "400": "#33a7b5"
        },
        "lime": {
          "100": "#caf880"
        },
        "green": {
          "300": "#71ce7e"
        },
        "blue": {
          "950": "#020381",
          "600": "#2874fc"
        },
        "neutral-900": {
          "2": "#424244"
        },
        "background": "#ffffff",
        "foreground": "#000000",
        "muted-foreground": "#32373c",
        "primary": "#ff6900",
        "accent": "#cf2e2e",
        "border": "#abb8c3",
        "destructive": "#ff6900",
        "warning": "#fcb900",
        "success": "#7bdcb5",
        "info": "#0693e3"
      },
      "fontFamily": {
        "mono": [
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
        "sm": "14px",
        "base": "16px",
        "lg": "1.125em",
        "xl": "20px",
        "2xl": "1.5em",
        "3xl": "1.7rem",
        "4xl": "36px",
        "5xl": "47px"
      },
      "fontWeight": {
        "bold": "bold",
        "light": "300",
        "normal": "400",
        "black": "900",
        "semibold": "600"
      },
      "lineHeight": {
        "none": "1",
        "tight": "1.2",
        "snug": "1.4",
        "normal": "1.5",
        "relaxed": "1.6",
        "loose": "2.5rem"
      },
      "letterSpacing": {},
      "spacing": {
        "0": "0px",
        "1px": "1px",
        "2px": "2px",
        "3px": "3px",
        "1": "4px",
        "4_8px": "4.8px",
        "5px": "5px",
        "6px": "6px",
        "7px": "7px",
        "2": "8px",
        "9_6px": "9.6px",
        "10px": "10px",
        "3": "12px",
        "15px": "15px",
        "4": "16px",
        "19_2px": "19.2px",
        "5": "20px",
        "6": "24px",
        "30px": "30px",
        "8": "32px",
        "35px": "35px",
        "10": "40px",
        "12": "48px",
        "65px": "65px"
      },
      "borderRadius": {
        "none": "0",
        "DEFAULT": "0.2rem",
        "2xl": "16px",
        "3xl": "28px",
        "full": "9999px"
      },
      "boxShadow": {
        "xs": "0 0 1px 0 #888",
        "sm": "inset 0px 0px 0px 3px #E55E20",
        "DEFAULT": "1px 1px 4px rgba(0,0,0,.2)"
      },
      "screens": {
        "md": "800px",
        "md-880": "880px",
        "lg": "1120px",
        "xl": "1200px",
        "xl-1280": "1280px",
        "xl-1312": "1312px",
        "2xl": "1500px"
      }
    }
  },
  "plugins": []
};
