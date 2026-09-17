# Design System & UI Specifications — www.armorcode.com

Extracted from [https://www.armorcode.com/](https://www.armorcode.com/) using `extract-theme`.
Generated on: 2026-09-17T18:53:37

> **AI SYSTEM PROMPT FOR VIBE CODING & UI DEVELOPMENT**
> You are an expert frontend engineer and UI/UX designer. When building pages, components, or screens for this project, you MUST strictly adhere to the design system rules, tokens, and aesthetic principles defined below.

---

## 🎨 Color Palette & Hex Tokens

### Brand Palette
- `slate-50`: `#f3f3ff`
- `white`: `#ffffff`
- `indigo-700`: `#5f36f1`
- `orange-400`: `#ff6900`
- `amber-300`: `#f99c07`
- `violet-400`: `#a183fa`
- `black`: `#000000`
- `slate-200`: `#cbd5e1`
- `stone-50`: `#fbf5df`
- `sky-500`: `#0693e3`
- `emerald-400`: `#00d084`
- `red-600`: `#cf2e2e`
- `yellow-300`: `#fcb900`
- `purple-600`: `#9b51e0`
- `slate-300`: `#abb8c3`
- `emerald-300`: `#7bdcb5`
- `slate-900`: `#334155`
- `red-500`: `#d66b5d`
- `slate-950`: `#0f172a`
- `rose-600`: `#df2a4a`
- `violet-200`: `#d6d5ff`
- `slate-600`: `#64748b`
- `violet-600`: `#7259f9`
- `slate-800`: `#475569`
- `neutral-100`: `#e2e8f0`
- `indigo-800`: `#5025dc`
- `indigo-900`: `#35198e`
- `slate-100`: `#c2e9ff`
- `yellow-50`: `#fff0b8`
- `red-200`: `#ffccc5`
- `slate-400`: `#94a3b8`
- `zinc-50`: `#defae8`
- `stone-100`: `#ffe5e1`
- `green-300`: `#6cdc92`
- `green-600`: `#1e9b49`
- `pink-400`: `#f084b8`
- `pink-600`: `#d32f71`
- `violet-600-2`: `#8b5cf6`
- `sky-600`: `#0082cd`
- `violet-700`: `#7a00df`

### Semantic UI Roles
- `--background`: `white`
- `--foreground`: `slate-900`
- `--muted-foreground`: `slate-600`
- `--primary`: `indigo-700`
- `--accent`: `orange-400`
- `--border`: `slate-50`
- `--destructive`: `orange-400`
- `--warning`: `amber-300`
- `--success`: `emerald-400`
- `--info`: `sky-500`

---

## 🔤 Typography & Font System

### Font Families
- `sans`: `MatterSQ,sans-serif`
- `mono`: `ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace`

### Type Scale (Font Sizes)
- `xs`: `13px`
- `sm`: `.875rem`
- `base`: `1rem`
- `lg`: `1.125rem`
- `xl`: `1.25rem`
- `2xl`: `1.5rem`
- `3xl`: `2rem`
- `4xl`: `42px`
- `5xl`: `3rem`
- `6xl`: `3.5rem`
- `8xl`: `6rem`
- `9xl`: `8.4em`

---

## 📏 Spacing, Layout & Elevation

### Spacing Scale
- `0`: `0px`
- `0_8px`: `0.8px`
- `1_6px`: `1.6px`
- `2px`: `2px`
- `1`: `4px`
- `5px`: `5px`
- `2`: `8px`
- `10px`: `10px`
- `10_67px`: `10.67px`
- `3`: `12px`
- `14px`: `14px`
- `15px`: `15px`
- `4`: `16px`
- `5`: `20px`
- `21_33px`: `21.33px`
- `23px`: `23px`
- `6`: `24px`
- `8`: `32px`
- `38px`: `38px`
- `10`: `40px`
- `12`: `48px`
- `14`: `56px`
- `16`: `64px`
- `20`: `80px`

### Border Radius
- `none`: `0`
- `DEFAULT`: `4px`
- `md`: `.375rem`
- `lg`: `.5rem`
- `xl`: `.75rem`
- `2xl`: `1rem`
- `3xl`: `1.5rem`
- `full`: `9999px`

### Shadows & Elevation
- `xs`: `0 0 0 5px #19f`
- `sm`: `inset 0 0 0 2px #fff,inset 0 0 0 calc(2px + 2px) rgb(95 54 241 / 1),0 1px 3px -1px rgb(15 23 42 / .1), 0 0 1px rgb(15 23 42 / .1)`
- `DEFAULT`: `0 17.579px 41.018px -17.579px rgba(68, 68, 68, 0.16)`

---

## 💻 Tech Stack & Context
- **Primary Source**: https://www.armorcode.com/
- **Detected Frameworks**: Tailwind CSS, jQuery

---

## 📊 Intelligence & Health Scorecard
- **Security Rating**: Grade F (Score: 25/100)
- **Accessibility (WCAG 2.1)**: 84/100 (Needs Remediation)
- **SEO Optimization**: 100/100
- **Performance Rating**: 85/100

---

## 🧩 Detected Component Architecture
- **Navbar / Header** (nav/header): 2 instances — Horizontal flex/grid navigation bar with logo and menu links
- **Hero Section** (section/div.hero): 1 instances — High-impact visual banner with primary title and primary call to action
- **Buttons** (button / a.btn): 24 instances — Rounded interactive click targets with hover states and micro-interactions
- **Forms & Inputs** (form / input): 0 instances — Input fields with custom borders, active focus ring, and placeholder text
- **Call-to-Action (CTA)** (section.cta): 2 instances — Prominent conversion sections with contrast background and headline
- **Footer** (footer): 1 instances — Multi-column link lists with copyright attribution and legal policies
- **Badges / Pills** (span.badge): 16 instances — Compact rounded indicators for status, categories, or featured highlights
- **Testimonials** (blockquote / .testimonial): 7 instances — Customer endorsement cards with quote text, avatar image, and author credentials

---

## 🔐 Security Headers Audit
| Security Header | Status | Observation |
| :--- | :--- | :--- |
| HTTPS Protocol | Secure | Connection is encrypted using TLS |
| Strict-Transport-Security (HSTS) | Not detected | Vulnerable to SSL stripping attacks |
| Content-Security-Policy (CSP) | Not detected | Missing restriction against XSS and injection |
| X-Frame-Options | Not detected | May be vulnerable to clickjacking if not controlled by CSP |
| X-Content-Type-Options | Not detected | MIME sniffing prevention not explicitly enabled |
| Referrer-Policy | Not detected | Browser default referrer rules apply |

---

## ♿ Accessibility Audit (WCAG 2.1 AA)
- [Warning] **Images & Multimedia**: 2 of 87 image(s) lack an `alt` attribute. *(Remediation: Add descriptive `alt='...'` or `alt=''` for decorative elements.)*
- [Info] **Document Structure**: Multiple <h1> tags detected (2 found). Single H1 is recommended. *(Remediation: Maintain a single primary H1 and use H2/H3 for subsequent sections.)*
- [Warning] **Document Structure**: Heading hierarchy skips levels (e.g. H1 followed directly by H3). *(Remediation: Do not skip heading levels. Ensure nested structure follows H1 → H2 → H3.)*

---

## 🤖 AI Design Insights & Archetype
- **Aesthetic Archetype**: Playful / Consumer Friendly
- **Consistency Index**: 92/100
- **Hierarchy Analysis**: Strong contrast between primary actions and body surfaces; typography scale creates a clear reading hierarchy.
- **Notable Patterns**: CSS Grid multi-column bento layouts, Soft layered elevation shadows, Chromatic ambient gradients

---

## ⚖️ Brand Ownership & Copyright Attribution
- **Brand / Entity**: ArmorCode
- **Copyright Notice**: © 2026 Ar
- **Attribution Policy**: All trademarks, logos, brand names, and design tokens belong to ArmorCode. Extracted for design system analysis and interoperability.

---

## 🚀 Copy-Paste AI Prompt

```markdown
Role: Senior Frontend Engineer
Task: Build modern, pixel-perfect, accessible UI components for www.armorcode.com.

Design System Guidelines:
- Primary Color Palette: slate-50: #f3f3ff, white: #ffffff, indigo-700: #5f36f1, orange-400: #ff6900, amber-300: #f99c07, violet-400: #a183fa, black: #000000, slate-200: #cbd5e1
- Fonts: sans (MatterSQ,sans-serif), mono (ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace)
- Layout: Use consistent 4px grid spacing. Rounded corners using none=0, DEFAULT=4px, md=.375rem.
- WCAG Accessibility: Ensure text elements have ≥4.5:1 contrast against surfaces.

Instructions:
1. Write clean, accessible, modern code matching this design language.
2. Use CSS custom properties or Tailwind CSS classes matching these tokens.
```
