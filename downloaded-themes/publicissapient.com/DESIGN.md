# Design System & UI Specifications — www.publicissapient.com

Extracted from [https://www.publicissapient.com/](https://www.publicissapient.com/) using `extract-theme`.
Generated on: 2026-09-18T17:25:33

> **AI SYSTEM PROMPT FOR VIBE CODING & UI DEVELOPMENT**
> You are an expert frontend engineer and UI/UX designer. When building pages, components, or screens for this project, you MUST strictly adhere to the design system rules, tokens, and aesthetic principles defined below.

---

## 🎨 Color Palette & Hex Tokens

### Brand Palette
- `white`: `#ffffff`
- `black`: `#000000`
- `red-600`: `#e90130`
- `white-a33`: `rgb(255 255 255 / 0.333)`
- `neutral-100`: `#e5e7eb`
- `white-a0`: `rgb(0 0 0 / 0.0)`
- `blue-700`: `#0c63ea`
- `neutral-900`: `#444444`
- `slate-800`: `#4a5565`
- `neutral-200`: `#d1d5dc`
- `slate-400`: `#99a1af`
- `neutral-700`: `#666666`
- `slate-950`: `#101828`
- `slate-600`: `#6a7282`
- `neutral-500`: `#949494`
- `slate-950-2`: `#030712`
- `blue-500`: `#2b7fff`
- `slate-950-3`: `#1e2939`
- `red-800`: `#9f0712`
- `yellow-100`: `#fee685`
- `neutral-50-a5`: `rgb(0 0 0 / 0.051)`
- `orange-400`: `#ff6900`
- `green-400`: `#00c950`

### Semantic UI Roles
- `--background`: `white`
- `--foreground`: `black`
- `--muted-foreground`: `neutral-900`
- `--primary`: `red-600`
- `--accent`: `blue-700`
- `--border`: `neutral-100`
- `--destructive`: `red-600`
- `--success`: `green-400`

---

## 🔤 Typography & Font System

### Font Families
- `sans`: `ui-sans-serif,system-ui,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"`
- `mono`: `ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace`

### Type Scale (Font Sizes)
- `xs`: `11px`
- `sm`: `14px`
- `base`: `1rem`
- `lg`: `1.125rem`
- `xl`: `22px`
- `2xl`: `1.5rem`
- `3xl`: `28px`
- `4xl`: `42px`
- `5xl`: `50px`
- `6xl`: `3.75rem`
- `7xl`: `4.5rem`

---

## 📏 Spacing, Layout & Elevation

### Spacing Scale
- `0`: `0px`
- `1px`: `1px`
- `1_6px`: `1.6px`
- `2px`: `2px`
- `1`: `4px`
- `5px`: `5px`
- `6px`: `6px`
- `7px`: `7px`
- `2`: `8px`
- `9_71px`: `9.71px`
- `10px`: `10px`
- `3`: `12px`
- `4`: `16px`
- `19px`: `19px`
- `5`: `20px`
- `6`: `24px`
- `7`: `28px`
- `30px`: `30px`
- `8`: `32px`
- `10`: `40px`
- `12`: `48px`
- `16`: `64px`
- `20`: `80px`

### Border Radius
- `none`: `0`
- `sm`: `3px`
- `DEFAULT`: `.25rem`
- `md`: `.375rem`
- `lg`: `.5rem`
- `xl`: `.75rem`
- `2xl`: `1rem`
- `3xl`: `1.5rem`
- `full`: `9999px`

### Shadows & Elevation
- `xs`: `0 0 #0000,0 0 #0000,inset0 0 0 2px#fff,inset0 0 0 calc(2px + 2px)#e90130,0 0 #0000`
- `sm`: `inset 0 0 0 1px #000`
- `DEFAULT`: `inset 0 0 0 1px #0000`
- `md`: `inset 0 0 0 1px #e90130`
- `lg`: `0 0 1px #888`
- `xl`: `0 0 1px #0003`
- `2xl`: `0 0 0 2px #0c63ea`

---

## 💻 Tech Stack & Context
- **Primary Source**: https://www.publicissapient.com/
- **Detected Frameworks**: Tailwind CSS

---

## 📊 Intelligence & Health Scorecard
- **Security Rating**: Grade B (Score: 70/100)
- **Accessibility (WCAG 2.1)**: 84/100 (Needs Remediation)
- **SEO Optimization**: 100/100
- **Performance Rating**: 69/100

---

## 🧩 Detected Component Architecture
- **Navbar / Header** (nav/header): 4 instances — Horizontal flex/grid navigation bar with logo and menu links
- **Hero Section** (section/div.hero): 1 instances — High-impact visual banner with primary title and primary call to action
- **Buttons** (button / a.btn): 23 instances — Rounded interactive click targets with hover states and micro-interactions
- **Cards / Tiles** (div.card / article): 20 instances — Content surfaces with border-radius, elevation shadows, and structured padding
- **Forms & Inputs** (form / input): 1 instances — Input fields with custom borders, active focus ring, and placeholder text
- **Footer** (footer): 1 instances — Multi-column link lists with copyright attribution and legal policies
- **Badges / Pills** (span.badge): 3 instances — Compact rounded indicators for status, categories, or featured highlights

---

## 🔐 Security Headers Audit
| Security Header | Status | Observation |
| :--- | :--- | :--- |
| HTTPS Protocol | Secure | Connection is encrypted using TLS |
| Strict-Transport-Security (HSTS) | Enabled | max-age=31536000 |
| Content-Security-Policy (CSP) | Not detected | Missing restriction against XSS and injection |
| X-Frame-Options | Protected | SAMEORIGIN |
| X-Content-Type-Options | Protected | nosniff |
| Referrer-Policy | Not detected | Browser default referrer rules apply |

---

## ♿ Accessibility Audit (WCAG 2.1 AA)
- [Critical] **Forms & Inputs**: 1 form input(s) lack an associated label or aria-label. *(Remediation: Pair all form controls with explicit <label for='...'> or aria-label.)*
- [Warning] **Visual Contrast**: 8 extracted color combination(s) fail WCAG AA (4.5:1 ratio). *(Remediation: Increase lightness difference between text and surface backgrounds.)*

---

## 🤖 AI Design Insights & Archetype
- **Aesthetic Archetype**: Playful / Consumer Friendly
- **Consistency Index**: 92/100
- **Hierarchy Analysis**: Strong contrast between primary actions and body surfaces; typography scale creates a clear reading hierarchy.
- **Notable Patterns**: CSS Grid multi-column bento layouts, Soft layered elevation shadows, Chromatic ambient gradients

---

## ⚖️ Brand Ownership & Copyright Attribution
- **Brand / Entity**: Publicis Sapient
- **Copyright Notice**: copyrightTe
- **Attribution Policy**: All trademarks, logos, brand names, and design tokens belong to Publicis Sapient. Extracted for design system analysis and interoperability.

---

## 🚀 Copy-Paste AI Prompt

```markdown
Role: Senior Frontend Engineer
Task: Build modern, pixel-perfect, accessible UI components for www.publicissapient.com.

Design System Guidelines:
- Primary Color Palette: white: #ffffff, black: #000000, red-600: #e90130, white-a33: rgb(255 255 255 / 0.333), neutral-100: #e5e7eb, white-a0: rgb(0 0 0 / 0.0), blue-700: #0c63ea, neutral-900: #444444
- Fonts: sans (ui-sans-serif,system-ui,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"), mono (ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace)
- Layout: Use consistent 4px grid spacing. Rounded corners using none=0, sm=3px, DEFAULT=.25rem.
- WCAG Accessibility: Ensure text elements have ≥4.5:1 contrast against surfaces.

Instructions:
1. Write clean, accessible, modern code matching this design language.
2. Use CSS custom properties or Tailwind CSS classes matching these tokens.
```
