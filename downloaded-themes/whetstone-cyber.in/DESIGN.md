# Design System & UI Specifications — whetstone-cyber.in

Extracted from [https://whetstone-cyber.in/](https://whetstone-cyber.in/) using `extract-theme`.
Generated on: 2026-09-18T17:37:18

> **AI SYSTEM PROMPT FOR VIBE CODING & UI DEVELOPMENT**
> You are an expert frontend engineer and UI/UX designer. When building pages, components, or screens for this project, you MUST strictly adhere to the design system rules, tokens, and aesthetic principles defined below.

---

## 🎨 Color Palette & Hex Tokens

### Brand Palette
- `white`: `#ffffff`
- `slate-950`: `#1b2f45`
- `neutral-50`: `#f1f1f1`
- `white-a0`: `rgb(255 255 255 / 0.0)`
- `slate-900`: `#374951`
- `black`: `#000000`
- `neutral-950`: `#121010`
- `neutral-950-2`: `#333333`
- `blue-600`: `#2575fc`
- `neutral-800`: `#555555`
- `neutral-200`: `#dddddd`
- `sky-400`: `#13aff0`
- `orange-400`: `#ff6900`
- `slate-600`: `#69727d`
- `slate-300`: `#abb8c3`
- `green-200`: `#29f48f`
- `red-600`: `#cf2e2e`
- `teal-600`: `#238c8c`
- `yellow-300`: `#fcb900`
- `green-300`: `#61ce70`
- `neutral-50-a4`: `rgb(0 0 0 / 0.035)`
- `cyan-400-a54`: `rgb(2 113 130 / 0.54)`
- `sky-500`: `#0693e3`
- `purple-600`: `#9b51e0`
- `emerald-300`: `#4ce09d`
- `emerald-300-2`: `#7bdcb5`
- `emerald-400`: `#00d084`
- `slate-400-a55`: `rgb(0 79 99 / 0.55)`
- `sky-600`: `#41788c`
- `neutral-300`: `#cccccc`
- `sky-700`: `#2d657a`
- `red-500`: `#fe2d2d`
- `neutral-100`: `#e7e7e7`
- `pink-300`: `#f78da7`
- `sky-300`: `#8ed1fc`
- `red-300`: `#fe8f75`
- `neutral-950-3`: `#222222`
- `neutral-500`: `#929292`
- `zinc-200`: `#b6e3d4`
- `neutral-300-a30`: `rgb(0 0 0 / 0.3)`

### Semantic UI Roles
- `--background`: `white`
- `--foreground`: `slate-900`
- `--muted-foreground`: `neutral-800`
- `--primary`: `blue-600`
- `--accent`: `sky-400`
- `--border`: `neutral-50`
- `--destructive`: `orange-400`
- `--warning`: `yellow-300`
- `--success`: `green-300`
- `--info`: `sky-400`

---

## 🔤 Typography & Font System

### Font Families
- `sans`: `"Gabarito",Sans-serif`
- `serif`: `"Playfair Display",serif`
- `mono`: `"Courier New",Courier,monospace`
- `sans-2`: `"Gabarito"`
- `sans-3`: `"Cairo",Sans-serif`
- `sans-4`: `"Font Awesome 5 Free"`
- `mono-2`: `Arial,Baskerville,monospace`
- `mono-3`: `monospace,monospace`

### Type Scale (Font Sizes)
- `xs`: `13px`
- `sm`: `14px`
- `base`: `1em`
- `lg`: `18px`
- `xl`: `20px`
- `2xl`: `1.5em`
- `3xl`: `1.8em`
- `4xl`: `42px`
- `5xl`: `3em`
- `6xl`: `4em`
- `7xl`: `69px`

---

## 📏 Spacing, Layout & Elevation

### Spacing Scale
- `0`: `0px`
- `2px`: `2px`
- `3px`: `3px`
- `1`: `4px`
- `5px`: `5px`
- `6px`: `6px`
- `2`: `8px`
- `10px`: `10px`
- `3`: `12px`
- `14px`: `14px`
- `15px`: `15px`
- `4`: `16px`
- `18px`: `18px`
- `5`: `20px`
- `6`: `24px`
- `25px`: `25px`
- `30px`: `30px`
- `31px`: `31px`
- `8`: `32px`
- `10`: `40px`
- `12`: `48px`
- `50px`: `50px`
- `16`: `64px`
- `20`: `80px`

### Border Radius
- `none`: `0`
- `sm`: `3px`
- `DEFAULT`: `5px`
- `md`: `6px`
- `lg`: `10px`
- `xl`: `14px`
- `2xl`: `15px`
- `3xl`: `30px`
- `full`: `50%`

### Shadows & Elevation
- `xs`: `0 0 0 0 currentColor`
- `sm`: `0 0 0 0 rgb(12 90 219 / .2)`
- `DEFAULT`: `0 0 0 0 #fff0`
- `md`: `inset 0 0 0 1px currentColor`
- `lg`: `inset 0 0 0 1px rgb(0 0 0 / .1)`
- `xl`: `inset 0 0 0 1px rgba(0,0,0,.1)`
- `2xl`: `0 0 0 2px rgb(51 51 51 / .1)`

---

## 💻 Tech Stack & Context
- **Primary Source**: https://whetstone-cyber.in/
- **Detected Frameworks**: jQuery

---

## 📊 Intelligence & Health Scorecard
- **Security Rating**: Grade C (Score: 45/100)
- **Accessibility (WCAG 2.1)**: 79/100 (Needs Remediation)
- **SEO Optimization**: 100/100
- **Performance Rating**: 85/100

---

## 🧩 Detected Component Architecture
- **Navbar / Header** (nav/header): 3 instances — Horizontal flex/grid navigation bar with logo and menu links
- **Hero Section** (section/div.hero): 1 instances — High-impact visual banner with primary title and primary call to action
- **Buttons** (button / a.btn): 17 instances — Rounded interactive click targets with hover states and micro-interactions
- **Cards / Tiles** (div.card / article): 1 instances — Content surfaces with border-radius, elevation shadows, and structured padding
- **Forms & Inputs** (form / input): 1 instances — Input fields with custom borders, active focus ring, and placeholder text
- **Footer** (footer): 1 instances — Multi-column link lists with copyright attribution and legal policies
- **Pricing Table** (div.pricing): 1 instances — Comparative tier grid displaying pricing numbers, feature checklists, and action buttons

---

## 🔐 Security Headers Audit
| Security Header | Status | Observation |
| :--- | :--- | :--- |
| HTTPS Protocol | Secure | Connection is encrypted using TLS |
| Strict-Transport-Security (HSTS) | Not detected | Vulnerable to SSL stripping attacks |
| Content-Security-Policy (CSP) | Configured | upgrade-insecure-requests |
| X-Frame-Options | Not detected | May be vulnerable to clickjacking if not controlled by CSP |
| X-Content-Type-Options | Not detected | MIME sniffing prevention not explicitly enabled |
| Referrer-Policy | Not detected | Browser default referrer rules apply |

---

## ♿ Accessibility Audit (WCAG 2.1 AA)
- [Warning] **Document Structure**: Heading hierarchy skips levels (e.g. H1 followed directly by H3). *(Remediation: Do not skip heading levels. Ensure nested structure follows H1 → H2 → H3.)*
- [Critical] **Forms & Inputs**: 2 form input(s) lack an associated label or aria-label. *(Remediation: Pair all form controls with explicit <label for='...'> or aria-label.)*
- [Warning] **Visual Contrast**: 4 extracted color combination(s) fail WCAG AA (4.5:1 ratio). *(Remediation: Increase lightness difference between text and surface backgrounds.)*

---

## 🤖 AI Design Insights & Archetype
- **Aesthetic Archetype**: Editorial & Refined
- **Consistency Index**: 84/100
- **Hierarchy Analysis**: Strong contrast between primary actions and body surfaces; typography scale creates a clear reading hierarchy.
- **Notable Patterns**: CSS Grid multi-column bento layouts, Soft layered elevation shadows, Chromatic ambient gradients

---

## ⚖️ Brand Ownership & Copyright Attribution
- **Brand / Entity**: Whetstone Cyber Solutions Pvt. Ltd.
- **Copyright Notice**: © 2026 Wh
- **Attribution Policy**: All trademarks, logos, brand names, and design tokens belong to Whetstone Cyber Solutions Pvt. Ltd.. Extracted for design system analysis and interoperability.

---

## 🚀 Copy-Paste AI Prompt

```markdown
Role: Senior Frontend Engineer
Task: Build modern, pixel-perfect, accessible UI components for whetstone-cyber.in.

Design System Guidelines:
- Primary Color Palette: white: #ffffff, slate-950: #1b2f45, neutral-50: #f1f1f1, white-a0: rgb(255 255 255 / 0.0), slate-900: #374951, black: #000000, neutral-950: #121010, neutral-950-2: #333333
- Fonts: sans ("Gabarito",Sans-serif), serif ("Playfair Display",serif), mono ("Courier New",Courier,monospace), sans-2 ("Gabarito"), sans-3 ("Cairo",Sans-serif), sans-4 ("Font Awesome 5 Free"), mono-2 (Arial,Baskerville,monospace), mono-3 (monospace,monospace)
- Layout: Use consistent 4px grid spacing. Rounded corners using none=0, sm=3px, DEFAULT=5px.
- WCAG Accessibility: Ensure text elements have ≥4.5:1 contrast against surfaces.

Instructions:
1. Write clean, accessible, modern code matching this design language.
2. Use CSS custom properties or Tailwind CSS classes matching these tokens.
```
