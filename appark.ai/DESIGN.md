# Design System & UI Specifications — appark.ai

Extracted from [https://appark.ai/](https://appark.ai/) using `extract-theme`.
Generated on: 2026-08-27T18:40:48

> **AI SYSTEM PROMPT FOR VIBE CODING & UI DEVELOPMENT**
> You are an expert frontend engineer and UI/UX designer. When building pages, components, or screens for this project, you MUST strictly adhere to the design system rules, tokens, and aesthetic principles defined below.

---

## 🎨 Color Palette & Hex Tokens

### Brand Palette
- `white`: `#ffffff`
- `neutral-50`: `#f0f0f0`
- `neutral-200`: `#d9d9d9`
- `blue-600`: `#1677ff`
- `neutral-950-a88`: `rgb(0 0 0 / 0.88)`
- `neutral-300-a25`: `rgb(0 0 0 / 0.25)`
- `blue-400`: `#4096ff`
- `neutral-50-a4`: `rgb(0 0 0 / 0.04)`
- `neutral-500-a45`: `rgb(0 0 0 / 0.451)`
- `stone-300-a40`: `rgb(113 63 18 / 0.4)`
- `red-400`: `#ff4d4f`
- `blue-500`: `#3b82f6`
- `blue-700`: `#0958d9`
- `black`: `#000000`
- `slate-400`: `#9ca3af`
- `slate-800`: `#475569`
- `neutral-800-a65`: `rgb(0 0 0 / 0.651)`
- `red-400-2`: `#ff7875`
- `slate-950`: `#111827`
- `slate-950-2`: `#1e293b`
- `amber-300`: `#faad14`
- `blue-400-2`: `#60a5fa`
- `blue-600-2`: `#2563eb`
- `slate-100`: `#dbeafe`
- `slate-900`: `#334155`
- `red-600`: `#d9363e`
- `white-a0`: `rgb(239 246 255 / 0.0)`
- `neutral-50-a5`: `rgb(9 92 255 / 0.051)`
- `lime-400`: `#52c41a`
- `red-500`: `#ef4444`
- `orange-400`: `#f97316`
- `red-300`: `#ffa39e`
- `green-400`: `#22c55e`
- `yellow-50`: `#fef3c7`
- `blue-300`: `#91caff`
- `neutral-500`: `#8c8c8c`
- `neutral-200-a15`: `rgb(0 0 0 / 0.15)`
- `neutral-50-a60`: `rgb(229 231 235 / 0.6)`
- `slate-600`: `#64748b`
- `green-700`: `#15803d`

### Semantic UI Roles
- `--background`: `white`
- `--foreground`: `black`
- `--muted-foreground`: `slate-800`
- `--primary`: `blue-600`
- `--accent`: `red-400`
- `--border`: `neutral-50`
- `--destructive`: `red-400`
- `--warning`: `amber-300`
- `--success`: `lime-400`
- `--info`: `blue-400`

---

## 🔤 Typography & Font System

### Font Families
- `sans`: `-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"`
- `mono`: `ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace`
- `sans-2`: `ui-sans-serif,system-ui,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji`
- `sans-3`: `-apple-system,BlinkMacSystemFont,PingFang SC,Hiragino Sans GB,Microsoft YaHei,Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,Open Sans,Helvetica Neue,sans-serif`
- `sans-4`: `Arial,Helvetica,sans-serif`
- `mono-2`: `monospace,monospace`

### Type Scale (Font Sizes)
- `xs`: `12px`
- `sm`: `14px`
- `base`: `16px`
- `lg`: `18px`
- `xl`: `1.25rem`
- `2xl`: `1.5rem`
- `3xl`: `1.875rem`
- `4xl`: `2.25rem`
- `5xl`: `3rem`

---

## 📏 Spacing, Layout & Elevation

### Spacing Scale
- `0`: `0px`
- `1px`: `1px`
- `2px`: `2px`
- `1`: `4px`
- `6px`: `6px`
- `7px`: `7px`
- `2`: `8px`
- `10px`: `10px`
- `11px`: `11px`
- `3`: `12px`
- `14px`: `14px`
- `4`: `16px`
- `18px`: `18px`
- `5`: `20px`
- `6`: `24px`
- `7`: `28px`
- `8`: `32px`
- `10`: `40px`
- `46px`: `46px`
- `12`: `48px`
- `14`: `56px`
- `16`: `64px`
- `20`: `80px`
- `40`: `160px`

### Border Radius
- `none`: `0`
- `sm`: `3px`
- `DEFAULT`: `4px`
- `md`: `6px`
- `lg`: `8px`
- `xl`: `12px`
- `2xl`: `1rem`
- `3xl`: `28px`
- `full`: `50%`

### Shadows & Elevation
- `xs`: `0 0 0 0 currentcolor`
- `sm`: `0 0 0 2px rgba(5, 145, 255, 0.1)`
- `DEFAULT`: `0 0 0 2px rgba(255, 38, 5, 0.06)`
- `md`: `0 0 0 2px rgba(255, 215, 5, 0.1)`
- `lg`: `0 2px 0 rgba(0, 0, 0, 0.02)`
- `xl`: `0 0 0 2px #1890ff33`
- `2xl`: `0 2px 0 rgba(5, 145, 255, 0.1)`

---

## 💻 Tech Stack & Context
- **Primary Source**: https://appark.ai/
- **Detected Frameworks**: Vue, Nuxt, Tailwind CSS

---

## 🚀 Copy-Paste AI Prompt

```markdown
Role: Senior Frontend Engineer
Task: Build modern, pixel-perfect, accessible UI components for appark.ai.

Design System Guidelines:
- Primary Color Palette: white: #ffffff, neutral-50: #f0f0f0, neutral-200: #d9d9d9, blue-600: #1677ff, neutral-950-a88: rgb(0 0 0 / 0.88), neutral-300-a25: rgb(0 0 0 / 0.25), blue-400: #4096ff, neutral-50-a4: rgb(0 0 0 / 0.04)
- Fonts: sans (-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"), mono (ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace), sans-2 (ui-sans-serif,system-ui,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji), sans-3 (-apple-system,BlinkMacSystemFont,PingFang SC,Hiragino Sans GB,Microsoft YaHei,Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,Open Sans,Helvetica Neue,sans-serif), sans-4 (Arial,Helvetica,sans-serif), mono-2 (monospace,monospace)
- Layout: Use consistent 4px grid spacing. Rounded corners using none=0, sm=3px, DEFAULT=4px.
- WCAG Accessibility: Ensure text elements have ≥4.5:1 contrast against surfaces.

Instructions:
1. Write clean, accessible, modern code matching this design language.
2. Use CSS custom properties or Tailwind CSS classes matching these tokens.
```
