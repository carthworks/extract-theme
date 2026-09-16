/* Tailwind v3 config extracted from https://stripe.com/in */
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
        "slate-300-a30": "rgb(66 71 112 / 0.3)",
        "indigo": {
          "700": "#533afd",
          "950": "#122054",
          "600": "#5d64fe",
          "500": "#7389ff",
          "900": "#2e2b8c",
          "800": "#4032c8",
          "300": "#a8bfff"
        },
        "indigo-950": {
          "2": "#0d1738",
          "3": "#182659"
        },
        "neutral": {
          "100": "#e5edf5",
          "50": "#f2f7fe"
        },
        "blue": {
          "950": "#0a2540",
          "600": "#6480b2",
          "700": "#45639d",
          "400": "#839bc8"
        },
        "slate": {
          "950": "#061b31",
          "200": "#d4dee9",
          "300": "#a3b5d6",
          "600": "#64748d",
          "900": "#273951",
          "100": "#e8e9ff",
          "700": "#50617a"
        },
        "red": {
          "400": "#ff6118"
        },
        "teal": {
          "300": "#0de4e4",
          "200": "#1df5e9"
        },
        "rose": {
          "500": "#ea2261"
        },
        "indigo-900": {
          "2": "#362baa",
          "3": "#23356e"
        },
        "blue-950": {
          "2": "#0c2e4e"
        },
        "indigo-500": {
          "2": "#7f7dfc"
        },
        "violet": {
          "300": "#b9b9f9",
          "500": "#9966ff"
        },
        "pink": {
          "400": "#f44bcc"
        },
        "slate-200": {
          "2": "#d6d9fc"
        },
        "indigo-300": {
          "2": "#92adff"
        },
        "slate-300": {
          "2": "#adbdcc"
        },
        "stone": {
          "100": "#ffe6f5"
        },
        "background": "#0d1738",
        "foreground": "#ffffff",
        "muted-foreground": "#e5edf5",
        "primary": "#533afd",
        "accent": "#7389ff",
        "border": "#0a2540",
        "destructive": "#ff6118"
      },
      "fontFamily": {
        "sans": [
          "sohne-var",
          "SF Pro Display",
          "sans-serif"
        ],
        "mono": [
          "SourceCodePro",
          "SFMono-Regular",
          "monospace"
        ],
        "sans-2": [
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Ubuntu",
          "sans-serif"
        ]
      },
      "fontSize": {
        "xs": "10px",
        "sm": "14px",
        "base": "1rem",
        "lg": "1.125rem",
        "xl": "1.25rem",
        "2xl": "24px",
        "3xl": "1.75rem",
        "4xl": "2.125rem",
        "5xl": "3rem",
        "6xl": "62px",
        "8xl": "110px"
      },
      "fontWeight": {
        "light": "300",
        "normal": "400",
        "semibold": "600",
        "medium": "500",
        "extralight": "200",
        "bold": "700"
      },
      "lineHeight": {
        "none": "1",
        "tight": "1.2",
        "snug": "1.4",
        "normal": "1.5",
        "relaxed": "28px"
      },
      "letterSpacing": {
        "tight": "-.0308em",
        "normal": "-.01em"
      },
      "spacing": {
        "0": "0px",
        "1px": "1px",
        "2px": "2px",
        "3px": "3px",
        "1": "4px",
        "5px": "5px",
        "6px": "6px",
        "7px": "7px",
        "2": "8px",
        "10px": "10px",
        "3": "12px",
        "13px": "13px",
        "14px": "14px",
        "15px": "15px",
        "4": "16px",
        "18px": "18px",
        "5": "20px",
        "22px": "22px",
        "6": "24px",
        "26px": "26px",
        "30px": "30px",
        "8": "32px",
        "10": "40px",
        "12": "48px"
      },
      "borderRadius": {
        "none": "1px",
        "sm": "3px",
        "DEFAULT": "4px",
        "md": "6px",
        "lg": "8px",
        "xl": "12px",
        "2xl": "16px",
        "3xl": "32px",
        "full": "50%"
      },
      "boxShadow": {
        "xs": "#e5edf5",
        "sm": "0 -1px 0 0 #e5edf5",
        "DEFAULT": "0 -1px 0 0 #182659",
        "md": "inset 0 0 0 2px #fff",
        "lg": "0 0 0 3px rgba(99,91,255,.1)",
        "xl": "0 0 0 2px #4d90fe,inset 0 0 0 2px hsla(0,0%,100%,0.9)",
        "2xl": "4.5px 0 0 0 #3f4b66,9px 0 0 0 #3f4b66"
      },
      "screens": {
        "sm": "350px",
        "sm-400": "400px",
        "sm-480": "480px",
        "sm-600": "600px",
        "sm-640": "640px",
        "md": "840px",
        "lg": "899px",
        "lg-900": "900px",
        "lg-901": "901px",
        "lg-940": "940px",
        "lg-970": "970px",
        "lg-1000": "1000px",
        "lg-1020": "1020px",
        "lg-1051": "1051px",
        "lg-1112": "1112px",
        "lg-1115": "1115px",
        "xl": "1264px",
        "xl-1300": "1300px"
      }
    }
  },
  "plugins": []
};
