# Design System & UI Specifications — stripe.com

Extracted from [https://stripe.com/in](https://stripe.com/in) using `extract-theme`.
Generated on: 2026-09-16T14:46:42

> **AI SYSTEM PROMPT FOR VIBE CODING & UI DEVELOPMENT**
> You are an expert frontend engineer and UI/UX designer. When building pages, components, or screens for this project, you MUST strictly adhere to the design system rules, tokens, and aesthetic principles defined below.

---

## 🎨 Color Palette & Hex Tokens

### Brand Palette
- `white`: `#ffffff`
- `indigo-700`: `#533afd`
- `indigo-950`: `#122054`
- `indigo-950-2`: `#0d1738`
- `indigo-600`: `#5d64fe`
- `neutral-100`: `#e5edf5`
- `blue-950`: `#0a2540`
- `indigo-500`: `#7389ff`
- `indigo-950-3`: `#182659`
- `slate-950`: `#061b31`
- `blue-600`: `#6480b2`
- `neutral-50`: `#f2f7fe`
- `white-a0`: `rgb(255 255 255 / 0.0)`
- `blue-700`: `#45639d`
- `blue-400`: `#839bc8`
- `slate-200`: `#d4dee9`
- `indigo-900`: `#2e2b8c`
- `red-400`: `#ff6118`
- `teal-300`: `#0de4e4`
- `rose-500`: `#ea2261`
- `indigo-800`: `#4032c8`
- `indigo-300`: `#a8bfff`
- `slate-300`: `#a3b5d6`
- `indigo-900-2`: `#362baa`
- `indigo-900-3`: `#23356e`
- `slate-600`: `#64748d`
- `slate-900`: `#273951`
- `blue-950-2`: `#0c2e4e`
- `indigo-500-2`: `#7f7dfc`
- `slate-100`: `#e8e9ff`
- `violet-300`: `#b9b9f9`
- `pink-400`: `#f44bcc`
- `slate-700`: `#50617a`
- `slate-200-2`: `#d6d9fc`
- `indigo-300-2`: `#92adff`
- `slate-300-a30`: `rgb(66 71 112 / 0.3)`
- `teal-200`: `#1df5e9`
- `slate-300-2`: `#adbdcc`
- `violet-500`: `#9966ff`
- `stone-100`: `#ffe6f5`

### Semantic UI Roles
- `--background`: `indigo-950-2`
- `--foreground`: `white`
- `--muted-foreground`: `neutral-100`
- `--primary`: `indigo-700`
- `--accent`: `indigo-500`
- `--border`: `blue-950`
- `--destructive`: `red-400`

---

## 🔤 Typography & Font System

### Font Families
- `sans`: `"sohne-var","SF Pro Display",sans-serif`
- `mono`: `"SourceCodePro","SFMono-Regular",monospace`
- `sans-2`: `-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Ubuntu,sans-serif`

### Type Scale (Font Sizes)
- `xs`: `10px`
- `sm`: `14px`
- `base`: `1rem`
- `lg`: `1.125rem`
- `xl`: `1.25rem`
- `2xl`: `24px`
- `3xl`: `1.75rem`
- `4xl`: `2.125rem`
- `5xl`: `3rem`
- `6xl`: `62px`
- `8xl`: `110px`

---

## 📏 Spacing, Layout & Elevation

### Spacing Scale
- `0`: `0px`
- `1px`: `1px`
- `2px`: `2px`
- `3px`: `3px`
- `1`: `4px`
- `5px`: `5px`
- `6px`: `6px`
- `7px`: `7px`
- `2`: `8px`
- `10px`: `10px`
- `3`: `12px`
- `13px`: `13px`
- `14px`: `14px`
- `15px`: `15px`
- `4`: `16px`
- `18px`: `18px`
- `5`: `20px`
- `22px`: `22px`
- `6`: `24px`
- `26px`: `26px`
- `30px`: `30px`
- `8`: `32px`
- `10`: `40px`
- `12`: `48px`

### Border Radius
- `none`: `1px`
- `sm`: `3px`
- `DEFAULT`: `4px`
- `md`: `6px`
- `lg`: `8px`
- `xl`: `12px`
- `2xl`: `16px`
- `3xl`: `32px`
- `full`: `50%`

### Shadows & Elevation
- `xs`: `#e5edf5`
- `sm`: `0 -1px 0 0 #e5edf5`
- `DEFAULT`: `0 -1px 0 0 #182659`
- `md`: `inset 0 0 0 2px #fff`
- `lg`: `0 0 0 3px rgba(99,91,255,.1)`
- `xl`: `0 0 0 2px #4d90fe,inset 0 0 0 2px hsla(0,0%,100%,0.9)`
- `2xl`: `4.5px 0 0 0 #3f4b66,9px 0 0 0 #3f4b66`

---

## 💻 Tech Stack & Context
- **Primary Source**: https://stripe.com/in
- **Detected Frameworks**: Next.js

---

## ⚖️ Brand Ownership & Copyright Attribution
- **Brand / Entity**: Stripe
- **Copyright Notice**: copyright hd
- **Attribution Policy**: All trademarks, logos, brand names, and design tokens belong to Stripe. Extracted for design system analysis and interoperability.

---

## 🚀 Copy-Paste AI Prompt

```markdown
Role: Senior Frontend Engineer
Task: Build modern, pixel-perfect, accessible UI components for stripe.com.

Design System Guidelines:
- Primary Color Palette: white: #ffffff, indigo-700: #533afd, indigo-950: #122054, indigo-950-2: #0d1738, indigo-600: #5d64fe, neutral-100: #e5edf5, blue-950: #0a2540, indigo-500: #7389ff
- Fonts: sans ("sohne-var","SF Pro Display",sans-serif), mono ("SourceCodePro","SFMono-Regular",monospace), sans-2 (-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Ubuntu,sans-serif)
- Layout: Use consistent 4px grid spacing. Rounded corners using none=1px, sm=3px, DEFAULT=4px.
- WCAG Accessibility: Ensure text elements have ≥4.5:1 contrast against surfaces.

Instructions:
1. Write clean, accessible, modern code matching this design language.
2. Use CSS custom properties or Tailwind CSS classes matching these tokens.
```
