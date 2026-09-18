# Design System & UI Specifications — www.vdartdigital.com

Extracted from [https://www.vdartdigital.com/](https://www.vdartdigital.com/) using `extract-theme`.
Generated on: 2026-09-18T17:10:47

> **AI SYSTEM PROMPT FOR VIBE CODING & UI DEVELOPMENT**
> You are an expert frontend engineer and UI/UX designer. When building pages, components, or screens for this project, you MUST strictly adhere to the design system rules, tokens, and aesthetic principles defined below.

---

## 🎨 Color Palette & Hex Tokens

### Brand Palette
- `white`: `#ffffff`
- `sky-950`: `#003049`
- `black`: `#000000`
- `white-a0`: `rgb(255 255 255 / 0.0)`
- `neutral-100`: `#eeeeee`
- `neutral-950`: `#232323`
- `neutral-700`: `#616161`
- `rose-600`: `#e91e63`
- `neutral-950-2`: `#333333`
- `neutral-200`: `#d2d2d2`
- `orange-400`: `#ff6900`
- `neutral-400`: `#999999`
- `violet-700`: `#7347db`
- `violet-950`: `#330072`
- `red-600`: `#cf2e2e`
- `yellow-300`: `#fcb900`
- `slate-300`: `#abb8c3`
- `emerald-400`: `#00d084`
- `sky-500`: `#0693e3`
- `purple-600`: `#9b51e0`
- `emerald-300`: `#7bdcb5`
- `neutral-900`: `#444444`
- `pink-700`: `#a81d84`
- `neutral-200-2`: `#dddddd`
- `neutral-600`: `#777777`
- `red-500`: `#fe2d2d`
- `yellow-200`: `#fddd00`
- `fuchsia-700`: `#9c27b0`
- `slate-700`: `#636e78`
- `sky-300`: `#00c9ff`
- `emerald-300-2`: `#62d69e`
- `pink-300`: `#f78da7`
- `sky-300-2`: `#8ed1fc`
- `blue-600`: `#2874fc`
- `blue-600-2`: `#007acc`
- `white-a0-2`: `rgb(0 0 0 / 0.0)`
- `slate-900`: `#293e4b`
- `rose-600-2`: `#ea0048`
- `yellow-50`: `#fff5cb`
- `yellow-50-2`: `#fef84c`

### Semantic UI Roles
- `--background`: `white`
- `--foreground`: `black`
- `--muted-foreground`: `neutral-950`
- `--primary`: `sky-950`
- `--accent`: `rose-600`
- `--border`: `neutral-100`
- `--destructive`: `rose-600`
- `--warning`: `yellow-300`
- `--success`: `emerald-400`
- `--info`: `sky-500`

---

## 🔤 Typography & Font System

### Font Families
- `sans`: `"Proxima-nova", sans-serif`
- `serif`: `"Roboto Slab","Times New Roman",serif`
- `mono`: `monospace,monospace`
- `sans-2`: `"Proxima-nova",sans-serif`
- `sans-3`: `"Proxima-nova", Sans-serif`
- `sans-4`: `"proxima-nova", sans-serif`
- `serif-2`: `Georgia, "Proxima-nova", Times, serif`
- `mono-2`: `Menlo,Monaco,Consolas,"Courier New",monospace`

### Type Scale (Font Sizes)
- `xs`: `12px`
- `sm`: `14px`
- `base`: `16px`
- `lg`: `18px`
- `xl`: `20px`
- `2xl`: `24px`
- `3xl`: `30px`
- `4xl`: `40px`
- `5xl`: `50px`
- `6xl`: `60px`
- `9xl`: `8rem`

---

## 📏 Spacing, Layout & Elevation

### Spacing Scale
- `0`: `0px`
- `2px`: `2px`
- `3px`: `3px`
- `1`: `4px`
- `5px`: `5px`
- `6px`: `6px`
- `7px`: `7px`
- `2`: `8px`
- `10px`: `10px`
- `3`: `12px`
- `14_85px`: `14.85px`
- `15px`: `15px`
- `4`: `16px`
- `17px`: `17px`
- `5`: `20px`
- `6`: `24px`
- `25px`: `25px`
- `29_71px`: `29.71px`
- `30px`: `30px`
- `34px`: `34px`
- `10`: `40px`
- `50px`: `50px`
- `15`: `60px`
- `70px`: `70px`

### Border Radius
- `none`: `0px`
- `sm`: `3px`
- `DEFAULT`: `5px`
- `md`: `7px`
- `lg`: `10px`
- `2xl`: `20px`
- `3xl`: `30px`
- `full`: `50%`

### Shadows & Elevation
- `xs`: `inset 0 -1px 0 rgb(0 0 0 / .25)`
- `sm`: `inset 0 1px 0 rgb(255 255 255 / .1)`
- `DEFAULT`: `inset 0 0 0 1px rgb(0 0 0 / .1)`
- `md`: `inset 0 1px 1px rgb(0 0 0 / .075)`
- `lg`: `inset 0 1px 0 rgb(255 255 255 / .1),0 1px 0 rgb(255 255 255 / .1)`
- `xl`: `0 0 2px 2px rgb(0 0 0 / .6)`
- `2xl`: `0 0 5px rgb(0 0 0 / .3)`

---

## 💻 Tech Stack & Context
- **Primary Source**: https://www.vdartdigital.com/
- **Detected Frameworks**: Bootstrap 4, jQuery

---

## 📊 Intelligence & Health Scorecard
- **Security Rating**: Grade B (Score: 70/100)
- **Accessibility (WCAG 2.1)**: 78/100 (Needs Remediation)
- **SEO Optimization**: 100/100
- **Performance Rating**: 69/100

---

## 🧩 Detected Component Architecture
- **Navbar / Header** (nav/header): 9 instances — Horizontal flex/grid navigation bar with logo and menu links
- **Hero Section** (section/div.hero): 1 instances — High-impact visual banner with primary title and primary call to action
- **Buttons** (button / a.btn): 16 instances — Rounded interactive click targets with hover states and micro-interactions
- **Cards / Tiles** (div.card / article): 5 instances — Content surfaces with border-radius, elevation shadows, and structured padding
- **Footer** (footer): 2 instances — Multi-column link lists with copyright attribution and legal policies
- **FAQ / Accordion** (details / div.faq): 11 instances — Expandable question & answer pairs with accordion toggle icons
- **Testimonials** (blockquote / .testimonial): 67 instances — Customer endorsement cards with quote text, avatar image, and author credentials

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
- [Critical] **Images & Multimedia**: 4 of 207 image(s) lack an `alt` attribute. *(Remediation: Add descriptive `alt='...'` or `alt=''` for decorative elements.)*
- [Warning] **Document Structure**: Page has no <h1> heading tag. *(Remediation: Include a single <h1> heading describing the page purpose.)*

---

## 🤖 AI Design Insights & Archetype
- **Aesthetic Archetype**: Editorial & Refined
- **Consistency Index**: 84/100
- **Hierarchy Analysis**: Strong contrast between primary actions and body surfaces; typography scale creates a clear reading hierarchy.
- **Notable Patterns**: CSS Grid multi-column bento layouts, Soft layered elevation shadows, Chromatic ambient gradients

---

## ⚖️ Brand Ownership & Copyright Attribution
- **Brand / Entity**: VDart Digital
- **Copyright Notice**: © 2026 VDart Digital. All rights reserved.
- **Attribution Policy**: All trademarks, logos, brand names, and design tokens belong to VDart Digital. Extracted for design system analysis and interoperability.

---

## 🚀 Copy-Paste AI Prompt

```markdown
Role: Senior Frontend Engineer
Task: Build modern, pixel-perfect, accessible UI components for www.vdartdigital.com.

Design System Guidelines:
- Primary Color Palette: white: #ffffff, sky-950: #003049, black: #000000, white-a0: rgb(255 255 255 / 0.0), neutral-100: #eeeeee, neutral-950: #232323, neutral-700: #616161, rose-600: #e91e63
- Fonts: sans ("Proxima-nova", sans-serif), serif ("Roboto Slab","Times New Roman",serif), mono (monospace,monospace), sans-2 ("Proxima-nova",sans-serif), sans-3 ("Proxima-nova", Sans-serif), sans-4 ("proxima-nova", sans-serif), serif-2 (Georgia, "Proxima-nova", Times, serif), mono-2 (Menlo,Monaco,Consolas,"Courier New",monospace)
- Layout: Use consistent 4px grid spacing. Rounded corners using none=0px, sm=3px, DEFAULT=5px.
- WCAG Accessibility: Ensure text elements have ≥4.5:1 contrast against surfaces.

Instructions:
1. Write clean, accessible, modern code matching this design language.
2. Use CSS custom properties or Tailwind CSS classes matching these tokens.
```
