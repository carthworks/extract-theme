/* Tailwind v3 config extracted from https://akitra.com/ */
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
        "neutral-100-a10": "rgb(0 0 0 / 0.1)",
        "stone-100-a15": "rgb(241 90 36 / 0.15)",
        "white-a0": {
          "2": "rgb(0 0 0 / 0.0)"
        },
        "neutral-600-a50": "rgb(0 0 0 / 0.5)",
        "neutral-700-a60": "rgb(0 0 0 / 0.6)",
        "neutral": {
          "100": "#e3e5eb",
          "50": "#eff1f6",
          "950": "#212327",
          "300": "#cccccc",
          "200": "#dddddd",
          "800": "#555555",
          "600": "#767676"
        },
        "red": {
          "500": "#f15a24",
          "600": "#cf2e2e",
          "800": "#aa0000"
        },
        "slate": {
          "600": "#757c8e",
          "900": "#41454f",
          "300": "#abb8c3",
          "950": "#222b30"
        },
        "orange": {
          "400": "#ff6900",
          "500": "#de5517"
        },
        "neutral-950": {
          "2": "#333333"
        },
        "yellow": {
          "300": "#fcb900"
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
        "blue": {
          "600": "#2874fc",
          "950": "#020381"
        },
        "red-500": {
          "2": "#f44337",
          "3": "#ff0000",
          "4": "#fe2d2d",
          "5": "#da4f49"
        },
        "amber": {
          "400": "#ed9700"
        },
        "green": {
          "500": "#24a148",
          "300": "#71ce7e"
        },
        "pink": {
          "300": "#f78da7",
          "500": "#ee2c82"
        },
        "sky-500": {
          "2": "#2098d1"
        },
        "teal": {
          "200": "#4aeadc"
        },
        "violet": {
          "700": "#720eec",
          "500": "#9778d1"
        },
        "neutral-600": {
          "2": "#707070"
        },
        "fuchsia": {
          "600": "#cf2aba"
        },
        "background": "#ffffff",
        "foreground": "#212327",
        "muted-foreground": "#757c8e",
        "primary": "#f15a24",
        "accent": "#fcb900",
        "border": "#e3e5eb",
        "destructive": "#f15a24",
        "warning": "#fcb900",
        "success": "#7bdcb5",
        "info": "#0693e3"
      },
      "fontFamily": {
        "sans": [
          "Font Awesome 5 Free"
        ],
        "serif": [
          "Alegreya",
          "serif"
        ],
        "mono": [
          "Courier Prime",
          "monospace"
        ],
        "sans-2": [
          "Font Awesome 5 Brands"
        ],
        "sans-3": [
          "WooCommerce"
        ],
        "sans-4": [
          "tutor"
        ],
        "serif-2": [
          "Arvo",
          "serif"
        ],
        "serif-3": [
          "Bodoni Moda",
          "serif"
        ],
        "serif-4": [
          "Cormorant",
          "serif"
        ],
        "mono-2": [
          "DM Mono",
          "monospace"
        ],
        "mono-3": [
          "IBM Plex Mono",
          "monospace"
        ],
        "mono-4": [
          "Noto Sans Mono",
          "sans-serif"
        ]
      },
      "fontSize": {
        "xs": "13px",
        "sm": "14px",
        "base": "16px",
        "lg": "18px",
        "xl": "20px",
        "2xl": "24px",
        "3xl": "30px",
        "4xl": "40px",
        "5xl": "50px",
        "6xl": "60px",
        "7xl": "80px"
      },
      "fontWeight": {
        "normal": "400",
        "medium": "500",
        "bold": "700",
        "semibold": "600",
        "extrabold": "800",
        "light": "300",
        "black": "900"
      },
      "lineHeight": {
        "none": "1",
        "tight": "20px",
        "snug": "1.4",
        "normal": "1.5",
        "relaxed": "162%",
        "loose": "48px"
      },
      "letterSpacing": {
        "normal": "normal",
        "wide": ".3px",
        "wider": "1px",
        "widest": ".1em"
      },
      "spacing": {
        "0": "0px",
        "2px": "2px",
        "1": "4px",
        "5px": "5px",
        "2": "8px",
        "10px": "10px",
        "3": "12px",
        "15px": "15px",
        "4": "16px",
        "5": "20px",
        "6": "24px",
        "7": "28px",
        "8": "32px",
        "9": "36px",
        "10": "40px",
        "11": "44px",
        "12": "48px",
        "13": "52px",
        "14": "56px",
        "15": "60px",
        "16": "64px",
        "17": "68px",
        "18": "72px",
        "20": "80px"
      },
      "borderRadius": {
        "none": "0",
        "sm": "3px",
        "DEFAULT": "4px",
        "md": "6px",
        "lg": "8px",
        "xl": "14px",
        "2xl": "20px",
        "3xl": "50px",
        "full": "50%"
      },
      "boxShadow": {
        "xs": "unset",
        "sm": "0 0 0 0 rgba(241, 90, 36,.1)",
        "DEFAULT": "0 0 rgba(0,0,0,.1)",
        "md": "0 0 0",
        "lg": "0 0 0 0 currentColor",
        "xl": "0 0 0 0 rgba(12,90,219,.2)",
        "2xl": "0 0 0 0 rgba(12,90,219,0)"
      },
      "screens": {
        "sm": "420px",
        "sm-500": "500px",
        "sm-576": "576px",
        "sm-577": "577px",
        "sm-600": "600px",
        "sm-620": "620px",
        "sm-673": "673px",
        "md": "710px",
        "md-766": "766px",
        "md-767": "767px",
        "md-768": "768px",
        "md-800": "800px",
        "lg": "910px",
        "lg-955": "955px",
        "lg-992": "992px",
        "lg-1023": "1023px",
        "lg-1024": "1024px",
        "lg-1025": "1025px",
        "lg-1040": "1040px",
        "lg-1110": "1110px",
        "xl": "1200px",
        "xl-1218": "1218px",
        "xl-1400": "1400px"
      }
    }
  },
  "plugins": []
};
