/* Tailwind v3 config extracted from https://www.linkedin.com/ */
/** @type {import('tailwindcss').Config} */
module.exports = {
  "content": [
    "./src/**/*.{js,ts,jsx,tsx,html}"
  ],
  "theme": {
    "extend": {
      "colors": {
        "white-a0": "rgb(0 0 0 / 0.0)",
        "neutral-950-a90": "rgb(0 0 0 / 0.9)",
        "white": "#ffffff",
        "neutral-300-a30": "rgb(0 0 0 / 0.3)",
        "neutral-100-a8": "rgb(0 0 0 / 0.08)",
        "neutral-900-a75": "rgb(0 0 0 / 0.75)",
        "neutral-700-a60": "rgb(0 0 0 / 0.6)",
        "white-a60": "rgb(255 255 255 / 0.6)",
        "white-a90": "rgb(255 255 255 / 0.9)",
        "white-a8": "rgb(255 255 255 / 0.08)",
        "white-a30": "rgb(255 255 255 / 0.3)",
        "black": "#000000",
        "slate-100-a20": "rgb(112 181 249 / 0.2)",
        "blue": {
          "900": "#004182",
          "700": "#0a66c2",
          "200": "#a8d4ff"
        },
        "green": {
          "900": "#004d2a",
          "700": "#057642"
        },
        "red": {
          "700": "#cf0007",
          "900": "#762812",
          "200": "#fdc2b1"
        },
        "slate": {
          "900": "#38434f",
          "700": "#56687a",
          "100": "#efe0ff"
        },
        "red-700": {
          "2": "#b93a04"
        },
        "violet": {
          "900": "#592099"
        },
        "neutral": {
          "100": "#eae6df",
          "50": "#f3f2f0",
          "300": "#b0b0b0",
          "600": "#7f7f7f"
        },
        "sky": {
          "700": "#0073b1",
          "800": "#006097"
        },
        "red-900": {
          "2": "#8a0005"
        },
        "purple": {
          "700": "#8344cc"
        },
        "amber": {
          "700": "#915907",
          "900": "#5c3b09"
        },
        "blue-900": {
          "2": "#004b7c"
        },
        "cyan": {
          "900": "#114951"
        },
        "fuchsia": {
          "900": "#711c6d"
        },
        "lime": {
          "900": "#3f4618"
        },
        "background": "#ffffff",
        "foreground": "#0073b1",
        "muted-foreground": "#7f7f7f",
        "primary": "#004182",
        "accent": "#004d2a",
        "border": "#eae6df",
        "destructive": "#cf0007",
        "warning": "#915907",
        "success": "#004d2a",
        "info": "#004182"
      },
      "fontFamily": {
        "sans": [
          "-apple-system",
          "system-ui",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Fira Sans",
          "Ubuntu",
          "Oxygen",
          "Oxygen Sans",
          "Cantarell",
          "Droid Sans",
          "Apple Color Emoji",
          "Segoe UI Emoji",
          "Segoe UI Emoji",
          "Segoe UI Symbol",
          "Lucida Grande",
          "Helvetica",
          "Arial",
          "sans-serif"
        ],
        "mono": [
          "monospace",
          "serif"
        ],
        "sans-2": [
          "-apple-system",
          "system-ui",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Fira Sans",
          "Ubuntu",
          "Oxygen",
          "Oxygen Sans",
          "Cantarell",
          "Droid Sans",
          "Apple Color Emoji",
          "Segoe UI Emoji",
          "Segoe UI Emoji",
          "Segoe UI Symbol",
          "Lucida Grande",
          "Helvetica",
          "Arial",
          "sans-serif"
        ],
        "sans-3": [
          "Google Sans",
          "arial",
          "sans-serif"
        ],
        "sans-4": [
          "Roboto-Regular",
          "arial",
          "sans-serif"
        ],
        "mono-2": [
          "Consolas",
          "Monaco",
          "Andale Mono",
          "Ubuntu Mono",
          "monospace"
        ]
      },
      "fontSize": {
        "xs": "12px",
        "sm": "14px",
        "base": "16px",
        "lg": "18px",
        "xl": "20px",
        "2xl": "1.6rem",
        "3xl": "2rem",
        "4xl": "2.4rem",
        "5xl": "48px",
        "6xl": "64px",
        "7xl": "76px",
        "8xl": "100px"
      },
      "fontWeight": {
        "semibold": "600",
        "normal": "400",
        "bold": "bold",
        "medium": "500",
        "extralight": "200",
        "light": "300"
      },
      "lineHeight": {
        "none": "1",
        "tight": "1.25",
        "snug": "22px",
        "normal": "1.5",
        "relaxed": "1.625",
        "loose": "48px"
      },
      "letterSpacing": {
        "tight": "-0.02em",
        "normal": "0px",
        "wide": "0.25px",
        "widest": "4px"
      },
      "spacing": {
        "0": "0px",
        "1px": "1px",
        "2px": "2px",
        "3px": "3px",
        "1": "4px",
        "5px": "5px",
        "6px": "6px",
        "6_4px": "6.4px",
        "7px": "7px",
        "2": "8px",
        "10px": "10px",
        "3": "12px",
        "12_8px": "12.8px",
        "14px": "14px",
        "15px": "15px",
        "4": "16px",
        "5": "20px",
        "6": "24px",
        "8": "32px",
        "10": "40px",
        "12": "48px",
        "14": "56px",
        "15": "60px",
        "16": "64px"
      },
      "borderRadius": {
        "none": "0",
        "sm": "2px",
        "DEFAULT": "4px",
        "lg": "8px",
        "xl": "13px",
        "2xl": "16px",
        "3xl": "24px",
        "full": "50%"
      },
      "boxShadow": {
        "xs": "0 0 0 1px rgba(0, 0, 0, 0)",
        "sm": "0 0 0 1px rgba(0, 0, 0, 0.9)",
        "DEFAULT": "0 0 0 1px rgba(0, 0, 0, 0.75)",
        "md": "0 0 0 1px #0a66c2",
        "lg": "0 0 0 1px #8a0005",
        "xl": "inset 0 0 0 1px rgba(0,115,177,0.35)",
        "2xl": "inset 0 0 0 1px rgba(0,0,0,0.25)"
      },
      "screens": {
        "sm": "330px",
        "sm-480": "480px",
        "sm-512": "512px",
        "sm-576": "576px",
        "sm-616": "616px",
        "md": "720px",
        "md-768": "768px",
        "md-769": "769px",
        "md-809": "809px",
        "lg": "992px",
        "lg-1024": "1024px",
        "lg-1128": "1128px",
        "xl": "1161px",
        "xl-1163": "1163px",
        "xl-1192": "1192px",
        "xl-1200": "1200px",
        "2xl": "1440px",
        "2xl-1680": "1680px",
        "2xl-1920": "1920px"
      }
    }
  },
  "plugins": []
};
