# Design System & UI Specifications — www.pitowings.com

Extracted from [https://www.pitowings.com/](https://www.pitowings.com/) using `extract-theme`.
Generated on: 2026-09-18T17:16:25

> **AI SYSTEM PROMPT FOR VIBE CODING & UI DEVELOPMENT**
> You are an expert frontend engineer and UI/UX designer. When building pages, components, or screens for this project, you MUST strictly adhere to the design system rules, tokens, and aesthetic principles defined below.

---

## 🎨 Color Palette & Hex Tokens

### Brand Palette
- `white`: `#ffffff`
- `stone-100`: `#ffe0e4`
- `white-a0`: `rgb(255 255 255 / 0.0)`
- `stone-100-a14`: `rgb(225 29 63 / 0.139)`
- `white-a0-2`: `rgb(0 0 0 / 0.0)`
- `rose-600`: `#e11d3f`
- `rose-200`: `#ffc6cf`
- `rose-400`: `#f65a76`
- `rose-300`: `#ff9aab`
- `rose-800`: `#a50d26`
- `stone-50-a8`: `rgb(225 29 63 / 0.076)`
- `rose-700`: `#c8102e`
- `neutral-950`: `#1b1418`
- `zinc-400`: `#a999aa`
- `white-a35`: `rgb(255 255 255 / 0.35)`

### Semantic UI Roles
- `--background`: `white`
- `--foreground`: `neutral-950`
- `--primary`: `rose-600`
- `--accent`: `rose-300`
- `--border`: `stone-100`
- `--destructive`: `rose-600`

---

## 🔤 Typography & Font System

### Font Families
- `sans`: `"Poppins",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif`
- `mono`: `ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono","Courier New",monospace`

### Type Scale (Font Sizes)
- `xs`: `.75rem`
- `sm`: `.875rem`
- `base`: `1rem`
- `lg`: `1.125rem`
- `xl`: `1.25rem`
- `2xl`: `1.5rem`
- `3xl`: `1.875rem`
- `4xl`: `2.25rem`
- `5xl`: `3rem`
- `6xl`: `3.75rem`
- `7xl`: `4.5rem`

---

## 📏 Spacing, Layout & Elevation

### Spacing Scale
- `0`: `0px`
- `1px`: `1px`
- `2_56px`: `2.56px`
- `3px`: `3px`
- `1`: `4px`
- `4_48px`: `4.48px`
- `4_8px`: `4.8px`
- `8_8px`: `8.8px`
- `9_6px`: `9.6px`
- `14_4px`: `14.4px`
- `17_6px`: `17.6px`
- `5`: `20px`
- `23_2px`: `23.2px`
- `27px`: `27px`
- `7`: `28px`
- `50_4px`: `50.4px`
- `13`: `52px`
- `62_4px`: `62.4px`
- `70_4px`: `70.4px`

### Border Radius
- `none`: `0`
- `DEFAULT`: `.25rem`
- `lg`: `.5rem`
- `xl`: `.75rem`
- `2xl`: `1rem`
- `3xl`: `1.5rem`

### Shadows & Elevation
- `xs`: `0 0 #0000,0 0 #0000,0 0 #0000,initial 0 0 0 calc(4px + 0px) oklch(93.6% .032 17.717),0 8px 24px -16px initial`
- `sm`: `0 20px 50px -28px #1b141859`
- `DEFAULT`: `0 22px 60px -22px #c8102e73`

---

## 💻 Tech Stack & Context
- **Primary Source**: https://www.pitowings.com/
- **Detected Frameworks**: Next.js, Tailwind CSS

---

## 📊 Intelligence & Health Scorecard
- **Security Rating**: Grade B (Score: 65/100)
- **Accessibility (WCAG 2.1)**: 88/100 (AA Compliant)
- **SEO Optimization**: 88/100
- **Performance Rating**: 90/100

---

## 🧩 Detected Component Architecture
- **Navbar / Header** (nav/header): 2 instances — Horizontal flex/grid navigation bar with logo and menu links
- **Hero Section** (section/div.hero): 1 instances — High-impact visual banner with primary title and primary call to action
- **Buttons** (button / a.btn): 8 instances — Rounded interactive click targets with hover states and micro-interactions
- **Footer** (footer): 1 instances — Multi-column link lists with copyright attribution and legal policies
- **Testimonials** (blockquote / .testimonial): 5 instances — Customer endorsement cards with quote text, avatar image, and author credentials

---

## 🔐 Security Headers Audit
| Security Header | Status | Observation |
| :--- | :--- | :--- |
| HTTPS Protocol | Secure | Connection is encrypted using TLS |
| Strict-Transport-Security (HSTS) | Enabled | max-age=63072000; includeSubDomains; preload |
| Content-Security-Policy (CSP) | Not detected | Missing restriction against XSS and injection |
| X-Frame-Options | Not detected | May be vulnerable to clickjacking if not controlled by CSP |
| X-Content-Type-Options | Protected | nosniff |
| Referrer-Policy | Configured | strict-origin-when-cross-origin |

---

## ♿ Accessibility Audit (WCAG 2.1 AA)
- [Warning] **Visual Contrast**: 29 extracted color combination(s) fail WCAG AA (4.5:1 ratio). *(Remediation: Increase lightness difference between text and surface backgrounds.)*

---

## 🤖 AI Design Insights & Archetype
- **Aesthetic Archetype**: Developer Tooling / Technical
- **Consistency Index**: 92/100
- **Hierarchy Analysis**: Strong contrast between primary actions and body surfaces; typography scale creates a clear reading hierarchy.
- **Notable Patterns**: CSS Grid multi-column bento layouts, Soft layered elevation shadows, Chromatic ambient gradients

---

## ⚖️ Brand Ownership & Copyright Attribution
- **Brand / Entity**: PITOWINGS
- **Copyright Notice**: © 2026 PITOWINGS. All rights reserved.
- **Attribution Policy**: All trademarks, logos, brand names, and design tokens belong to PITOWINGS. Extracted for design system analysis and interoperability.

---

## 🚀 Copy-Paste AI Prompt

```markdown
Role: Senior Frontend Engineer
Task: Build modern, pixel-perfect, accessible UI components for www.pitowings.com.

Design System Guidelines:
- Primary Color Palette: white: #ffffff, stone-100: #ffe0e4, white-a0: rgb(255 255 255 / 0.0), stone-100-a14: rgb(225 29 63 / 0.139), white-a0-2: rgb(0 0 0 / 0.0), rose-600: #e11d3f, rose-200: #ffc6cf, rose-400: #f65a76
- Fonts: sans ("Poppins",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif), mono (ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono","Courier New",monospace)
- Layout: Use consistent 4px grid spacing. Rounded corners using none=0, DEFAULT=.25rem, lg=.5rem.
- WCAG Accessibility: Ensure text elements have ≥4.5:1 contrast against surfaces.

Instructions:
1. Write clean, accessible, modern code matching this design language.
2. Use CSS custom properties or Tailwind CSS classes matching these tokens.
```
