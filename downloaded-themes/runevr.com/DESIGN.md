# Design System & UI Specifications — runevr.com

Extracted from [https://runevr.com/](https://runevr.com/) using `extract-theme`.
Generated on: 2026-09-15T21:52:35

> **AI SYSTEM PROMPT FOR VIBE CODING & UI DEVELOPMENT**
> You are an expert frontend engineer and UI/UX designer. When building pages, components, or screens for this project, you MUST strictly adhere to the design system rules, tokens, and aesthetic principles defined below.

---

## 🎨 Color Palette & Hex Tokens

### Brand Palette
- `white`: `#ffffff`
- `fuchsia-600`: `#ba00d9`
- `neutral-100`: `#ececf1`
- `black`: `#000000`
- `sky-600`: `#0085cf`
- `slate-950`: `#0f172b`
- `cyan-300`: `#39c8eb`
- `slate-950-2`: `#0b0b14`
- `slate-200`: `#e3d9f8`
- `violet-600`: `#7c3aed`
- `purple-900`: `#59168b`
- `slate-700`: `#5b5b6b`
- `neutral-600`: `#808080`
- `neutral-950`: `#1a1a1a`
- `white-a0`: `rgb(0 0 0 / 0.0)`
- `white-a78`: `rgb(255 255 255 / 0.78)`
- `emerald-200`: `#a7f3d0`
- `rose-300`: `#fca5a5`
- `violet-300`: `#c4b5fd`
- `green-300`: `#4bde5c`
- `slate-200-2`: `#c6e2f8`
- `neutral-400`: `#a7a7a7`
- `neutral-200`: `#d1d5dc`
- `yellow-100`: `#fee685`
- `sky-400`: `#38bdf8`
- `blue-400`: `#60a5fa`
- `purple-600`: `#9810fa`
- `fuchsia-300`: `#f0abfc`
- `purple-700`: `#8200db`
- `slate-900`: `#364153`
- `lime-300`: `#a1d45e`
- `blue-500`: `#2b7fff`
- `yellow-300`: `#fbbf24`
- `amber-300`: `#fe9a00`
- `purple-500`: `#ad46ff`
- `slate-400`: `#99a1af`
- `slate-800`: `#4a5565`
- `cyan-200`: `#67e8f9`
- `indigo-400`: `#818cf8`
- `indigo-300`: `#a5b4fc`

### Semantic UI Roles
- `--background`: `white`
- `--foreground`: `slate-950-2`
- `--muted-foreground`: `slate-950`
- `--primary`: `fuchsia-600`
- `--accent`: `sky-600`
- `--border`: `neutral-100`
- `--destructive`: `rose-300`
- `--warning`: `yellow-300`
- `--success`: `green-300`
- `--info`: `sky-600`

---

## 🔤 Typography & Font System

### Font Families
- `sans`: `"Instrument Sans",sans-serif`
- `mono`: `ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace`
- `sans-2`: `"Twemoji","Inter",ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif`
- `sans-3`: `"Instrument Sans", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`
- `sans-4`: `"Inter", system-ui, sans-serif`

### Type Scale (Font Sizes)
- `xs`: `13px`
- `sm`: `14.5px`
- `base`: `16px`
- `lg`: `18px`
- `xl`: `1.25rem`
- `2xl`: `24px`
- `3xl`: `1.875rem`
- `4xl`: `2.25rem`
- `5xl`: `3rem`
- `6xl`: `64px`
- `7xl`: `72px`

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
- `11px`: `11px`
- `13_6px`: `13.6px`
- `4`: `16px`
- `18px`: `18px`
- `5`: `20px`
- `21px`: `21px`
- `22px`: `22px`
- `6`: `24px`
- `26px`: `26px`
- `37px`: `37px`
- `10`: `40px`
- `13`: `52px`
- `14`: `56px`
- `15`: `60px`

### Border Radius
- `none`: `0`
- `sm`: `2px`
- `DEFAULT`: `.25rem`
- `md`: `6px 6px 6px 6px`
- `lg`: `.6rem`
- `xl`: `.75rem`
- `2xl`: `18px`
- `3xl`: `22px`
- `full`: `9999px`

### Shadows & Elevation
- `xs`: `0 0 6px 2px #6BA9FE90`
- `sm`: `0 0 6px 2px #C084FC90`
- `DEFAULT`: `0 0 6px 2px #34D39990`
- `md`: `0 0 6px 2px #A78BFA90`
- `lg`: `0 0 6px 2px #F59E0B90`
- `xl`: `9px 6px 11px rgba(0, 0, 0, 0.21)`
- `2xl`: `0 6px 24px #0b0b140d`

---

## 💻 Tech Stack & Context
- **Primary Source**: https://runevr.com/
- **Detected Frameworks**: Astro, Tailwind CSS

---

## 🚀 Copy-Paste AI Prompt

```markdown
Role: Senior Frontend Engineer
Task: Build modern, pixel-perfect, accessible UI components for runevr.com.

Design System Guidelines:
- Primary Color Palette: white: #ffffff, fuchsia-600: #ba00d9, neutral-100: #ececf1, black: #000000, sky-600: #0085cf, slate-950: #0f172b, cyan-300: #39c8eb, slate-950-2: #0b0b14
- Fonts: sans ("Instrument Sans",sans-serif), mono (ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace), sans-2 ("Twemoji","Inter",ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif), sans-3 ("Instrument Sans", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif), sans-4 ("Inter", system-ui, sans-serif)
- Layout: Use consistent 4px grid spacing. Rounded corners using none=0, sm=2px, DEFAULT=.25rem.
- WCAG Accessibility: Ensure text elements have ≥4.5:1 contrast against surfaces.

Instructions:
1. Write clean, accessible, modern code matching this design language.
2. Use CSS custom properties or Tailwind CSS classes matching these tokens.
```
