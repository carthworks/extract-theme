# 🎨 ExtractDesign Studio — Reverse-Engineer Design Systems & Website Intelligence

> **Reverse-engineer design systems, UI components & website intelligence from any live URL.**

**ExtractDesign Studio** is a comprehensive Python CLI tool and Web UI Workbench that crawls any website, parses its CSS stylesheet architecture using `tinycss2`, normalizes visual tokens, performs multi-dimensional audits (Accessibility, Performance, SEO, Security), and outputs complete, production-ready design systems with interactive style guides.

![ExtractDesign Studio](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_v3_%26_v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

![ExtractDesign Studio Web Workbench](homepage.png)

---

## ✨ Features & Capabilities

- 🎨 **Color Palette Normalization**: Groups and converts colors to OKLab perceptual space, merges near-identical shades (`--color-tolerance`), and infers semantic roles (`--bg`, `--surface`, `--ink`, `--accent`, `--line`).
- 🔤 **Typography & Font Extraction**: Extracts font families, type scales, font weights, line-heights, letter-spacing, and automatically downloads original `@font-face` binary files (`.woff2`, `.woff`, `.ttf`) to `fonts/`.
- 🖼️ **Site Logo & Icon Extraction**: Automatically finds and saves SVG logos, header `<img>` logotypes (with Next.js image optimizer support), apple-touch-icons, and high-resolution favicons.
- 💻 **Tech Stack & Framework Detection**: Detects 17+ frontend frameworks and libraries from script signatures and stylesheet declarations (`Next.js`, `React`, `Vue`, `Nuxt`, `Angular`, `Svelte`, `Tailwind CSS`, `Bootstrap`, `MUI`, `Framer Motion`, `GSAP`, `jQuery`).
- 📊 **WCAG 2.1 Contrast Matrix**: Evaluates color pair combinations against WCAG 2.1 AA, AA Large, and AAA accessibility standards.
- ✨ **Gradients & Keyframe Animations**: Scans and indexes linear/radial gradients, `@keyframes` animation names, duration scales, and custom `cubic-bezier` easing curves.
- 🤖 **AI-Ready `DESIGN.md` Prompt**: Emits a structured `DESIGN.md` system prompt reference containing explicit guidelines for AI tools (Antigravity, Cursor, Vibe Coding, Claude, ChatGPT).
- 🚀 **ExtractDesign Studio Web UI**: Hostable web dashboard (`server.py` + `http://localhost:8000`) with interactive flag sliders, URL presets, live chunked terminal output, and a theme folder explorer with live color swatches.

---

## 📁 Output Folder Structure

Running a scan on `https://example.com` creates a domain folder containing:

```
example.com/
├── style-guide.html      # Interactive, self-contained HTML style guide
├── DESIGN.md             # AI system prompt & UI design guidelines
├── design-tokens.json    # Machine-readable JSON design tokens
├── theme.css             # :root CSS custom properties & dark scope
├── components.css        # Buttons, cards, inputs, & badges built on tokens
├── tailwind.theme.css    # Tailwind v4 @theme block
├── tailwind.config.js    # Tailwind v3 config file
├── logo.png / logo.svg   # Extracted site logo / favicon asset
├── fonts/                # Extracted @font-face binary font files (.woff2)
└── raw/
    ├── combined.css      # Consolidated & absolutised stylesheet
    └── sheet-001.css     # Raw fetched stylesheets
```

---

## ⚡ Quickstart & Installation

### 1. Requirements & Setup

Ensure Python 3.9+ is installed, then install required dependencies:

```bash
pip install -r requirements.txt
```

---

### 2. Using the CLI

Run `extract_theme.py` with a target domain:

```bash
# Basic single-page extraction
python extract_theme.py https://stripe.com

# Crawl 5 same-site pages with custom max colors
python extract_theme.py https://linear.app --crawl 5 --max-colors 48

# Override output folder name
python extract_theme.py https://vercel.com -o ./my-vercel-theme
```

#### CLI Options & Flags

| Flag | Default | Description |
|---|---|---|
| `--crawl <N>` | `1` | Number of same-site pages to crawl for CSS discovery |
| `--max-colors <N>` | `40` | Maximum distinct colors in extracted palette |
| `--min-count <N>` | `2` | Minimum usage count for a color to be kept |
| `--color-tolerance <N>` | `0.03` | Color merging threshold in OKLab space |
| `--root-font-size <N>` | `16` | Base pixel ratio for `rem` calculations |
| `-o / --out <path>` | Domain Name | Output directory path |
| `--no-verify` | `False` | Disable SSL certificate verification |

---

### 3. Launching the Web UI Studio

**Windows (One-Click Launch):**
Double-click `app-run.bat` or run:
```cmd
app-run.bat
```
This automatically verifies dependencies, releases port 8000, starts the server, and opens your default browser to `http://localhost:8000`.

**Cross-Platform / CLI:**
```bash
python server.py
```

Open **`http://localhost:8000`** in your browser to access the **ExtractDesign Studio Workbench**:
- Interactive extraction controls & live terminal streaming
- Multi-dimensional website intelligence dashboard with 14 in-depth audit tabs
- Output directory explorer with visual theme swatches and token inspection
- One-click launch for `style-guide.html`, Next.js component generator, and modal code viewer for `DESIGN.md`, tokens, and CSS variables.

---

## 🤝 License

Apache-2.0 License. Developed by Karthikeyan T (@carthworks). Built for designers, frontend developers, and AI-driven UI workflows.
