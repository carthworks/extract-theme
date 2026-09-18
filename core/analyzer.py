"""
analyzer.py — Deep Website Intelligence & Design System Analyzer for ExtractTheme Studio.

Extracts multi-dimensional website intelligence:
1.  🎨 Design System: Colors, typography, spacing, radius, shadows, CSS variables/tokens
2.  🧩 Component Detection: Navbar, Hero, Buttons, Cards, Forms, CTA, Footer, Pricing, FAQ, etc.
3.  📐 Layout Analysis: Containers, Grids, Flexbox, spacing conventions, breakpoints, visual structure
4.  🖼 Asset Analyzer: Images, SVGs, icons, dimensions, formats, alt text, optimization issues
5.  📱 Responsive Analysis: Mobile/Tablet/Desktop setups, viewport meta, fixed width/overflow hazards
6.  ♿ Accessibility Audit (WCAG 2.1): Contrast ratios, alt text, heading hierarchy, form labels, ARIA
7.  ⚡ Performance Audit: Transfer size, requests count, asset breakdown, render-blocking scripts, hints
8.  🔍 SEO Audit: Title, description, headings, canonical, OG/Twitter tags, robots.txt, sitemap, schema
9.  🔐 Security Headers: HTTPS, HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy
10. 🛠 Technology Detection: Frameworks, CMS, UI libraries, analytics, CDN, hosting, font providers
11. 🔗 Site Structure: Crawled internal link graph, visual hierarchy tree
12. 📝 Content Intelligence: Headlines, CTAs, value proposition, testimonials, pricing, trust signals
13. 🤖 AI Design Insights: Visual style synthesis, hierarchy, consistency, facts vs interpretation
14. 📦 Export: CSS variables, JSON design tokens, Tailwind config, DESIGN.md, React component suggestions

Tier 1 Design Intelligence (NEW):
T1a. 🏷  Semantic Token Naming — assigns role-based CSS variable names (--color-brand-primary) from raw hex
T1b. 📏  Visual Consistency Score — 0–100 grade across color economy, typography, spacing, radius discipline
T1c. 📐  Spacing Grid Detection — identifies 4pt/8pt base unit and adherence %, flags off-grid rogue values
T1d. 🚀  Framework-Aware Exports — generates Tailwind config, TypeScript theme, or CSS vars based on detected stack
"""

from __future__ import annotations

import math
import re
import time
from urllib.parse import urljoin, urlparse
from typing import Any

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


class SiteAnalyzer:
    """Performs deep intelligence analysis on fetched web pages, CSS rules, and HTTP metadata."""

    def __init__(
        self,
        primary_url: str,
        pages: list[tuple[str, str]],
        css_text: str,
        tokens: dict[str, Any],
        http_headers: dict[str, str] | None = None,
        fetch_timing_ms: float = 0.0,
        robots_txt: str | None = None,
        sitemap_xml: str | None = None,
    ):
        self.primary_url = primary_url
        self.pages = pages  # list of (url, html_str)
        self.css_text = css_text or ""
        self.tokens = tokens or {}
        self.headers = {k.lower(): v for k, v in (http_headers or {}).items()}
        self.timing_ms = round(fetch_timing_ms, 1)
        self.robots_txt = robots_txt
        self.sitemap_xml = sitemap_xml
        
        parsed = urlparse(primary_url)
        self.domain = (parsed.netloc or primary_url).removeprefix("www.")
        self.scheme = parsed.scheme or "https"

        # Parsed BeautifulSoups for all pages
        self.soups: list[tuple[str, BeautifulSoup]] = []
        if BeautifulSoup:
            for u, h in self.pages:
                try:
                    self.soups.append((u, BeautifulSoup(h, "html.parser")))
                except Exception:
                    pass
        self.primary_soup = self.soups[0][1] if self.soups else None

    def analyze_all(self) -> dict[str, Any]:
        """Runs all 14 intelligence audits and returns a comprehensive structured report."""
        sec_audit = self.audit_security_headers()
        seo_audit = self.audit_seo()
        perf_audit = self.audit_performance()
        a11y_audit = self.audit_accessibility()
        tech_audit = self.detect_technologies()
        comp_audit = self.detect_components()
        layout_audit = self.analyze_layout()
        asset_audit = self.analyze_assets()
        resp_audit = self.analyze_responsive()
        site_struct = self.analyze_site_structure()
        content_intel = self.analyze_content()
        ai_insights = self.generate_ai_design_insights(
            tech_audit, comp_audit, layout_audit, content_intel
        )
        exports = self.generate_exports()

        # Generate overarching health scores (0-100)
        a11y_score = a11y_audit.get("score", 85)
        seo_score = seo_audit.get("score", 90)
        sec_grade = sec_audit.get("grade", "B")
        perf_score = perf_audit.get("score", 88)

        overview = {
            "domain": self.domain,
            "primary_url": self.primary_url,
            "analyzed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "pages_analyzed": len(self.pages),
            "scores": {
                "accessibility": a11y_score,
                "seo": seo_score,
                "performance": perf_score,
                "security_grade": sec_grade,
            },
            "summary": {
                "components_detected": len(comp_audit.get("detected", [])),
                "assets_count": asset_audit.get("total_assets", 0),
                "technologies_count": len(tech_audit.get("all_detected", [])),
                "internal_links_count": len(site_struct.get("internal_pages", [])),
                "design_style": ai_insights.get("style_archetype", "Modern Web"),
            },
        }

        # Tier 1 Design Intelligence
        design_intelligence = {
            "semantic_tokens": self.name_semantic_tokens(),
            "consistency": self.score_visual_consistency(),
            "spacing_grid": self.detect_spacing_grid(),
        }

        return {
            "overview": overview,
            "design_system": self.format_design_system(),
            "design_intelligence": design_intelligence,
            "components": comp_audit,
            "layout": layout_audit,
            "assets": asset_audit,
            "responsive": resp_audit,
            "accessibility": a11y_audit,
            "performance": perf_audit,
            "seo": seo_audit,
            "security": sec_audit,
            "technology": tech_audit,
            "site_structure": site_struct,
            "content_intelligence": content_intel,
            "ai_insights": ai_insights,
            "exports": self.generate_framework_exports(tech_audit),
        }

    # =========================================================================
    # 1. 🎨 DESIGN SYSTEM
    # =========================================================================
    def format_design_system(self) -> dict[str, Any]:
        """Summarizes extracted design system tokens with CSS variable generation."""
        colors = self.tokens.get("colors", {})
        roles = self.tokens.get("roles", {})
        fonts = self.tokens.get("fonts", {})
        font_sizes = self.tokens.get("font_sizes", {})
        font_weights = self.tokens.get("font_weights", {})
        spacing = self.tokens.get("spacing", {})
        radius = self.tokens.get("radius", {})
        shadows = self.tokens.get("shadows", {})
        gradients = self.tokens.get("gradients", [])

        # Build raw CSS variables
        css_vars = [":root {"]
        for r_name, r_val in roles.items():
            resolved = colors.get(r_val, r_val)
            css_vars.append(f"  --color-{r_name}: {resolved};")
        for c_name, c_hex in list(colors.items())[:20]:
            css_vars.append(f"  --{c_name}: {c_hex};")
        for f_name, f_val in fonts.items():
            if not f_name.startswith("_"):
                css_vars.append(f"  --font-{f_name}: {f_val};")
        for r_k, r_v in radius.items():
            css_vars.append(f"  --radius-{r_k}: {r_v};")
        for s_k, s_v in list(spacing.items())[:12]:
            css_vars.append(f"  --space-{s_k}: {s_v};")
        css_vars.append("}")

        return {
            "colors_count": len(colors),
            "colors": colors,
            "roles": roles,
            "fonts": fonts,
            "font_sizes": font_sizes,
            "font_weights": font_weights,
            "spacing": spacing,
            "radius": radius,
            "shadows": shadows,
            "gradients": gradients,
            "css_variables": "\n".join(css_vars),
        }

    # =========================================================================
    # 2. 🧩 COMPONENT DETECTION
    # =========================================================================
    def detect_components(self) -> dict[str, Any]:
        """Detects Navbar, Hero, Buttons, Cards, Forms, CTA, Footer, Pricing, FAQ, Badges, etc."""
        if not self.primary_soup:
            return {"detected": [], "summary": "Not detected (HTML parsing unavailable)"}

        soup = self.primary_soup
        detected = []

        # 1. Navbar / Header
        nav_elements = soup.find_all(["nav", "header"])
        nav_classes = soup.find_all(class_=re.compile(r"nav|navbar|header|app-bar|menu-bar", re.I))
        if nav_elements or nav_classes:
            items_count = len(soup.select("nav a, header a, .navbar a"))
            has_logo = bool(soup.select("nav img, header img, nav svg, header svg, .logo, [class*='logo']"))
            detected.append({
                "type": "Navbar / Header",
                "tag": "nav/header",
                "count": max(len(nav_elements), 1),
                "items_count": items_count,
                "has_logo": has_logo,
                "sticky": bool(re.search(r"sticky|fixed", self.css_text[:5000], re.I)),
                "styles": "Horizontal flex/grid navigation bar with logo and menu links",
            })

        # 2. Hero Section
        hero = soup.find(class_=re.compile(r"hero|banner|intro|welcome|jumbotron", re.I)) or soup.find("section")
        hero_h1 = hero.find("h1") if hero else soup.find("h1")
        if hero_h1 or hero:
            cta_btn = hero.find(["button", "a"]) if hero else None
            detected.append({
                "type": "Hero Section",
                "tag": "section/div.hero",
                "count": 1 if hero else 0,
                "headline": hero_h1.get_text(strip=True)[:80] if hero_h1 else "Not detected",
                "has_cta": bool(cta_btn),
                "styles": "High-impact visual banner with primary title and primary call to action",
            })

        # 3. Buttons
        buttons = soup.find_all(["button"])
        a_buttons = soup.find_all("a", class_=re.compile(r"btn|button|cta|action", re.I))
        total_buttons = len(buttons) + len(a_buttons)
        if total_buttons > 0:
            sample_labels = [b.get_text(strip=True) for b in (buttons + a_buttons) if b.get_text(strip=True)][:5]
            detected.append({
                "type": "Buttons",
                "tag": "button / a.btn",
                "count": total_buttons,
                "sample_labels": sample_labels,
                "styles": "Rounded interactive click targets with hover states and micro-interactions",
            })

        # 4. Cards
        cards = soup.find_all(class_=re.compile(r"\bcard\b|card-|feature-box|item-box|bento|tile", re.I))
        articles = soup.find_all("article")
        card_count = max(len(cards), len(articles))
        if card_count > 0:
            detected.append({
                "type": "Cards / Tiles",
                "tag": "div.card / article",
                "count": card_count,
                "styles": "Content surfaces with border-radius, elevation shadows, and structured padding",
            })

        # 5. Forms & Inputs
        forms = soup.find_all("form")
        inputs = soup.find_all(["input", "select", "textarea"])
        if forms or inputs:
            detected.append({
                "type": "Forms & Inputs",
                "tag": "form / input",
                "count": len(forms),
                "inputs_count": len(inputs),
                "has_search": bool(soup.find("input", type="search") or soup.find(attrs={"placeholder": re.compile(r"search", re.I)})),
                "styles": "Input fields with custom borders, active focus ring, and placeholder text",
            })

        # 6. Call-to-Action (CTA) Sections
        cta_sections = soup.find_all(class_=re.compile(r"\bcta\b|call-to-action|newsletter|subscribe", re.I))
        if cta_sections:
            detected.append({
                "type": "Call-to-Action (CTA)",
                "tag": "section.cta",
                "count": len(cta_sections),
                "styles": "Prominent conversion sections with contrast background and headline",
            })

        # 7. Footer
        footers = soup.find_all("footer") or soup.find_all(class_=re.compile(r"\bfooter\b", re.I))
        if footers:
            footer_links = len(footers[0].find_all("a")) if footers else 0
            detected.append({
                "type": "Footer",
                "tag": "footer",
                "count": len(footers),
                "links_count": footer_links,
                "styles": "Multi-column link lists with copyright attribution and legal policies",
            })

        # 8. Pricing Tables
        pricing = soup.find_all(class_=re.compile(r"pricing|plan|tier|subscription", re.I))
        if pricing:
            detected.append({
                "type": "Pricing Table",
                "tag": "div.pricing",
                "count": len(pricing),
                "styles": "Comparative tier grid displaying pricing numbers, feature checklists, and action buttons",
            })

        # 9. FAQ / Accordion
        faq = soup.find_all(class_=re.compile(r"\bfaq\b|accordion|collapse", re.I)) or soup.find_all("details")
        if faq:
            detected.append({
                "type": "FAQ / Accordion",
                "tag": "details / div.faq",
                "count": len(faq),
                "styles": "Expandable question & answer pairs with accordion toggle icons",
            })

        # 10. Badges / Pills / Tags
        badges = soup.find_all(class_=re.compile(r"\bbadge\b|\bpill\b|\btag\b|chip", re.I))
        if badges:
            detected.append({
                "type": "Badges / Pills",
                "tag": "span.badge",
                "count": len(badges),
                "styles": "Compact rounded indicators for status, categories, or featured highlights",
            })

        # 11. Testimonials / Reviews
        testimonials = soup.find_all(["blockquote"]) or soup.find_all(class_=re.compile(r"testimonial|review|quote|author", re.I))
        if testimonials:
            detected.append({
                "type": "Testimonials",
                "tag": "blockquote / .testimonial",
                "count": len(testimonials),
                "styles": "Customer endorsement cards with quote text, avatar image, and author credentials",
            })

        # 12. Modals / Dialogs
        modals = soup.find_all(["dialog"]) or soup.find_all(class_=re.compile(r"\bmodal\b|dialog|popup|drawer", re.I))
        if modals:
            detected.append({
                "type": "Modals / Dialogs",
                "tag": "dialog / div.modal",
                "count": len(modals),
                "styles": "Overlay dialog surfaces with blurred backdrop and dismiss control",
            })

        return {
            "detected": detected,
            "total_types": len(detected),
        }

    # =========================================================================
    # 3. 📐 LAYOUT ANALYSIS
    # =========================================================================
    def analyze_layout(self) -> dict[str, Any]:
        """Analyzes page structure, containers, grids, flexbox, and responsive breakpoints."""
        # Detect max-width container values in CSS
        max_widths = re.findall(r"max-width:\s*([0-9]+(?:px|rem|em|%))", self.css_text, re.I)
        containers = [mw for mw in set(max_widths) if "px" in mw and int(re.sub(r"[^\d]", "", mw) or 0) >= 600]
        containers.sort(key=lambda x: int(re.sub(r"[^\d]", "", x) or 0), reverse=True)

        has_grid = bool(re.search(r"display:\s*grid|grid-template-columns", self.css_text, re.I))
        has_flex = bool(re.search(r"display:\s*flex|flex-direction", self.css_text, re.I))

        # Media query breakpoints
        raw_bp = self.tokens.get("breakpoints", [])
        if isinstance(raw_bp, dict):
            breakpoints = [f"{k}: {v}" for k, v in raw_bp.items()]
        elif isinstance(raw_bp, list):
            breakpoints = list(raw_bp)
        else:
            breakpoints = []

        if not breakpoints:
            bp_matches = re.findall(r"@media[^{]*\((?:min|max)-width:\s*([0-9]+(?:px|em|rem))\)", self.css_text, re.I)
            breakpoints = sorted(list(set(bp_matches)), key=lambda x: int(re.sub(r"[^\d]", "", x) or 0))

        # Visual page structure flow
        sections_flow = []
        if self.primary_soup:
            for el in self.primary_soup.find_all(["header", "nav", "main", "section", "article", "aside", "footer"]):
                tag_name = el.name.lower()
                cls = " ".join(el.get("class", []))[:30]
                ident = el.get("id", "")
                label = f"<{tag_name}>"
                if ident:
                    label += f" #{ident}"
                elif cls:
                    label += f" .{cls.split()[0]}"
                if label not in sections_flow and len(sections_flow) < 10:
                    sections_flow.append(label)

        return {
            "containers": containers[:6] if containers else ["1280px (Standard)", "1024px (Compact)"],
            "primary_container": containers[0] if containers else "1280px",
            "layout_engines": {
                "css_grid": has_grid,
                "flexbox": has_flex,
            },
            "breakpoints": breakpoints[:8] if breakpoints else ["640px", "768px", "1024px", "1280px"],
            "spacing_conventions": {
                "section_padding_y": "48px – 96px (Standard)",
                "column_gap": "16px – 32px",
                "container_padding_x": "16px – 24px",
            },
            "page_structure_flow": sections_flow or ["<header>", "<main>", "<section>", "<footer>"],
        }

    # =========================================================================
    # 4. 🖼 ASSET ANALYZER
    # =========================================================================
    def analyze_assets(self) -> dict[str, Any]:
        """Analyzes images, SVGs, formats, dimensions, alt attributes, and flags optimization issues."""
        if not self.primary_soup:
            return {"total_assets": 0, "images": [], "issues": []}

        soup = self.primary_soup
        imgs = soup.find_all("img")
        svgs = soup.find_all("svg")
        sources = soup.find_all("source")

        image_items = []
        issues = []
        format_counts: dict[str, int] = {}
        missing_alt_count = 0
        missing_dimensions_count = 0

        for img in imgs:
            src = img.get("src") or img.get("data-src") or ""
            if not src:
                continue
            alt = img.get("alt", None)
            w = img.get("width")
            h = img.get("height")
            fmt = "unknown"

            clean_src = src.split("?")[0].lower()
            if clean_src.endswith(".webp"):
                fmt = "WEBP"
            elif clean_src.endswith(".avif"):
                fmt = "AVIF"
            elif clean_src.endswith(".svg") or "data:image/svg" in src:
                fmt = "SVG"
            elif clean_src.endswith(".png"):
                fmt = "PNG"
            elif clean_src.endswith((".jpg", ".jpeg")):
                fmt = "JPEG"
            elif clean_src.endswith(".gif"):
                fmt = "GIF"
            else:
                fmt = "WEBP/Dynamic" if "image" in src else "PNG/JPG"

            format_counts[fmt] = format_counts.get(fmt, 0) + 1

            # Check alt text
            if alt is None or alt.strip() == "":
                missing_alt_count += 1

            # Check dimension attributes (CLS prevention)
            if not w or not h:
                missing_dimensions_count += 1

            if len(image_items) < 12:
                image_items.append({
                    "src": src[:120],
                    "alt": alt if alt is not None else "Not provided",
                    "width": w or "Not specified",
                    "height": h or "Not specified",
                    "format": fmt,
                    "loading": img.get("loading", "eager"),
                })

        # Compile issues
        if missing_alt_count > 0:
            issues.append({
                "severity": "Warning",
                "message": f"{missing_alt_count} image(s) missing alt text (accessibility and SEO hazard).",
            })
        if missing_dimensions_count > 0:
            issues.append({
                "severity": "Info",
                "message": f"{missing_dimensions_count} image(s) missing explicit width/height attributes (may cause Cumulative Layout Shift).",
            })
        if format_counts.get("PNG", 0) + format_counts.get("JPEG", 0) > 5:
            issues.append({
                "severity": "Info",
                "message": "Multiple legacy PNG/JPEG assets detected. Modern WebP or AVIF could reduce bandwidth by 30-50%.",
            })

        return {
            "total_assets": len(imgs) + len(svgs),
            "images_count": len(imgs),
            "svgs_count": len(svgs),
            "picture_sources_count": len(sources),
            "format_breakdown": format_counts,
            "missing_alt_count": missing_alt_count,
            "missing_dimensions_count": missing_dimensions_count,
            "sample_assets": image_items,
            "issues": issues,
        }

    # =========================================================================
    # 5. 📱 RESPONSIVE ANALYSIS
    # =========================================================================
    def analyze_responsive(self) -> dict[str, Any]:
        """Analyzes desktop, tablet, and mobile layouts and potential responsive issues."""
        viewport_meta = None
        if self.primary_soup:
            vp = self.primary_soup.find("meta", attrs={"name": re.compile(r"^viewport$", re.I)})
            if vp:
                viewport_meta = vp.get("content", "")

        issues = []
        if not viewport_meta:
            issues.append({
                "severity": "Critical",
                "title": "Missing Viewport Meta Tag",
                "description": "No <meta name='viewport'> tag detected. Mobile browsers will render at desktop scale (980px).",
            })
        elif "width=device-width" not in viewport_meta.lower():
            issues.append({
                "severity": "Warning",
                "title": "Non-Standard Viewport Settings",
                "description": f"Viewport configured as '{viewport_meta}'. Ensure 'width=device-width, initial-scale=1' is included.",
            })

        # Check for wide fixed pixel widths that exceed mobile screen
        fixed_wide_widths = re.findall(r"width:\s*([0-9]{3,4})px", self.css_text, re.I)
        wide_counts = [int(w) for w in fixed_wide_widths if int(w) > 480 and int(w) < 2000]
        if wide_counts:
            issues.append({
                "severity": "Warning",
                "title": "Hardcoded Pixel Widths Detected",
                "description": f"Observed fixed width rules up to {max(wide_counts)}px. Verify max-width: 100% is used to avoid horizontal overflow on mobile.",
            })

        breakpoints = self.tokens.get("breakpoints", ["640px", "768px", "1024px", "1280px"])

        return {
            "viewport_meta": viewport_meta or "Not detected",
            "has_viewport_tag": bool(viewport_meta),
            "breakpoints": breakpoints,
            "views": {
                "mobile": {"width": "< 768px", "status": "Supported" if breakpoints else "Standard"},
                "tablet": {"width": "768px – 1024px", "status": "Supported"},
                "desktop": {"width": "> 1024px", "status": "Optimized"},
            },
            "issues": issues,
            "overall_status": "Responsive Ready" if not any(i["severity"] == "Critical" for i in issues) else "Action Required",
        }

    # =========================================================================
    # 6. ♿ ACCESSIBILITY AUDIT (WCAG 2.1 AA/AAA)
    # =========================================================================
    def audit_accessibility(self) -> dict[str, Any]:
        """Audits contrast, alt text, heading hierarchy, form labels, ARIA landmarks, and focus outlines."""
        issues = []
        score = 100

        if not self.primary_soup:
            return {"score": 80, "grade": "B", "issues": []}

        soup = self.primary_soup

        # 1. Image alt text
        imgs = soup.find_all("img")
        missing_alt = [img for img in imgs if img.get("alt") is None]
        if missing_alt:
            penalty = min(len(missing_alt) * 3, 20)
            score -= penalty
            issues.append({
                "severity": "Critical" if len(missing_alt) > 3 else "Warning",
                "category": "Images & Multimedia",
                "rule": "WCAG 1.1.1 Non-text Content",
                "message": f"{len(missing_alt)} of {len(imgs)} image(s) lack an `alt` attribute.",
                "remediation": "Add descriptive `alt='...'` or `alt=''` for decorative elements.",
            })

        # 2. Heading hierarchy
        headings = soup.find_all(re.compile(r"^h[1-6]$"))
        h1s = soup.find_all("h1")
        if len(h1s) == 0:
            score -= 10
            issues.append({
                "severity": "Warning",
                "category": "Document Structure",
                "rule": "WCAG 1.3.1 Info and Relationships",
                "message": "Page has no <h1> heading tag.",
                "remediation": "Include a single <h1> heading describing the page purpose.",
            })
        elif len(h1s) > 1:
            score -= 5
            issues.append({
                "severity": "Info",
                "category": "Document Structure",
                "rule": "WCAG 2.4.6 Headings and Labels",
                "message": f"Multiple <h1> tags detected ({len(h1s)} found). Single H1 is recommended.",
                "remediation": "Maintain a single primary H1 and use H2/H3 for subsequent sections.",
            })

        # Check skipped heading levels (e.g. h1 -> h3)
        levels = [int(h.name[1]) for h in headings]
        skipped = False
        for i in range(len(levels) - 1):
            if levels[i + 1] > levels[i] + 1:
                skipped = True
                break
        if skipped:
            score -= 5
            issues.append({
                "severity": "Warning",
                "category": "Document Structure",
                "rule": "WCAG 2.4.6 Headings and Labels",
                "message": "Heading hierarchy skips levels (e.g. H1 followed directly by H3).",
                "remediation": "Do not skip heading levels. Ensure nested structure follows H1 → H2 → H3.",
            })

        # 3. Form input labels
        inputs = soup.find_all(["input", "select", "textarea"])
        unlabeled_inputs = 0
        for inp in inputs:
            if inp.get("type") in ("hidden", "submit", "button", "reset"):
                continue
            has_id = inp.get("id")
            has_aria = inp.get("aria-label") or inp.get("aria-labelledby") or inp.get("title")
            has_label = bool(has_id and soup.find("label", attrs={"for": has_id}))
            parent_label = bool(inp.find_parent("label"))
            if not (has_aria or has_label or parent_label):
                unlabeled_inputs += 1

        if unlabeled_inputs > 0:
            score -= min(unlabeled_inputs * 4, 15)
            issues.append({
                "severity": "Critical",
                "category": "Forms & Inputs",
                "rule": "WCAG 3.3.2 Labels or Instructions",
                "message": f"{unlabeled_inputs} form input(s) lack an associated label or aria-label.",
                "remediation": "Pair all form controls with explicit <label for='...'> or aria-label.",
            })

        # 4. Color contrast from tokens
        contrast_data = self.tokens.get("contrast", [])
        low_contrast = [c for c in contrast_data if not c.get("aa_normal", True)]
        if low_contrast:
            score -= min(len(low_contrast) * 2, 12)
            issues.append({
                "severity": "Warning",
                "category": "Visual Contrast",
                "rule": "WCAG 1.4.3 Contrast (Minimum)",
                "message": f"{len(low_contrast)} extracted color combination(s) fail WCAG AA (4.5:1 ratio).",
                "remediation": "Increase lightness difference between text and surface backgrounds.",
            })

        # 5. Language attribute on <html>
        html_tag = soup.find("html")
        if not html_tag or not html_tag.get("lang"):
            score -= 5
            issues.append({
                "severity": "Warning",
                "category": "Language",
                "rule": "WCAG 3.1.1 Language of Page",
                "message": "<html lang='...'> attribute is missing.",
                "remediation": "Add lang='en' (or respective language code) to the root <html> tag.",
            })

        # 6. Outline focus removal
        if re.search(r"outline:\s*(?:0|none)\s*(?:!important)?;", self.css_text, re.I):
            if not re.search(r":focus-visible", self.css_text, re.I):
                score -= 8
                issues.append({
                    "severity": "Critical",
                    "category": "Keyboard Navigation",
                    "rule": "WCAG 2.4.7 Focus Visible",
                    "message": "CSS removes outline focus rings without providing visible :focus-visible replacement.",
                    "remediation": "Provide custom focus indicators with distinct box-shadow or outline.",
                })

        score = max(min(score, 100), 20)
        grade = "A" if score >= 90 else ("B" if score >= 75 else ("C" if score >= 60 else "F"))

        return {
            "score": score,
            "grade": grade,
            "wcag_level": "AA Compliant" if score >= 85 else "Needs Remediation",
            "issues_count": len(issues),
            "critical_count": sum(1 for i in issues if i["severity"] == "Critical"),
            "warning_count": sum(1 for i in issues if i["severity"] == "Warning"),
            "info_count": sum(1 for i in issues if i["severity"] == "Info"),
            "issues": issues,
        }

    # =========================================================================
    # 7. ⚡ PERFORMANCE AUDIT
    # =========================================================================
    def audit_performance(self) -> dict[str, Any]:
        """Audits page size, resource requests, render-blocking scripts, resource hints, and loading metrics."""
        html_bytes = sum(len(h.encode("utf-8", "replace")) for _, h in self.pages)
        css_bytes = len(self.css_text.encode("utf-8", "replace"))

        soup = self.primary_soup
        scripts = soup.find_all("script") if soup else []
        stylesheets = soup.find_all("link", rel=lambda x: x and "stylesheet" in x) if soup else []
        images = soup.find_all("img") if soup else []
        font_files = self.tokens.get("font_files", [])

        render_blocking_scripts = []
        for s in scripts:
            src = s.get("src")
            if src and not s.get("async") and not s.get("defer") and s.get("type") != "module":
                if s.find_parent("head"):
                    render_blocking_scripts.append(src)

        # Resource hints
        resource_hints = []
        if soup:
            for l in soup.find_all("link", rel=True):
                rel_vals = [r.lower() for r in (l.get("rel") if isinstance(l.get("rel"), list) else [l.get("rel")])]
                for r in ("preconnect", "dns-prefetch", "preload", "prefetch"):
                    if r in rel_vals:
                        resource_hints.append(f"{r}: {l.get('href', '')[:60]}")

        # Font-display check in CSS
        has_font_display_swap = bool(re.search(r"font-display:\s*swap", self.css_text, re.I))

        # Lazy loading images
        lazy_images = sum(1 for img in images if img.get("loading") == "lazy")

        score = 100
        if len(render_blocking_scripts) > 2:
            score -= 10
        if html_bytes + css_bytes > 1_500_000:
            score -= 15
        elif html_bytes + css_bytes > 700_000:
            score -= 8
        if len(images) > 10 and lazy_images == 0:
            score -= 7
        # CLS risk: images without explicit width and height
        images_without_dims = [
            img.get("src", "")[:60]
            for img in images
            if not (img.get("width") and img.get("height"))
        ]

        # LCP readiness: check for hero image preload or fetchpriority="high"
        has_lcp_preload = any("preload" in rh and "image" in rh for rh in resource_hints) or any(
            img.get("fetchpriority") == "high" or img.get("priority") is not None
            for img in images[:2]
        )

        # External Google font links (risk of font layout shift vs next/font)
        has_google_font_link = bool(soup and soup.find("link", href=re.compile(r"fonts\.googleapis\.com", re.I)))

        # Next.js performance checklist items & recommendations
        recommendations = []
        if images_without_dims:
            recommendations.append(
                f"Specify explicit width/height or use Next.js <Image> on {len(images_without_dims)} image(s) to eliminate Cumulative Layout Shift (target CLS < 0.1)."
            )
        if not has_lcp_preload and images:
            recommendations.append(
                "Add `priority` prop to primary hero/above-the-fold image to optimize Largest Contentful Paint (target LCP < 2.5s)."
            )
        if has_google_font_link:
            recommendations.append(
                "Migrate Google Fonts from <link> tags to `next/font/google` for zero-shift automatic font preloading."
            )
        if render_blocking_scripts:
            recommendations.append(
                "Eliminate head render-blocking scripts via `next/script` with `strategy='afterInteractive'` or `defer`."
            )
        recommendations.append(
            "Push `'use client'` boundaries down to interactive leaf nodes (buttons, inputs) to reduce client bundle size."
        )

        if len(images_without_dims) > 5:
            score -= 6

        score = max(min(score, 100), 30)

        return {
            "score": score,
            "response_time_ms": self.timing_ms,
            "transfer_sizes": {
                "html_kb": round(html_bytes / 1024, 1),
                "css_kb": round(css_bytes / 1024, 1),
                "total_text_kb": round((html_bytes + css_bytes) / 1024, 1),
            },
            "requests_count": {
                "html_documents": len(self.pages),
                "stylesheets": len(stylesheets),
                "scripts": len(scripts),
                "images": len(images),
                "fonts": len(font_files),
                "total_estimated": len(stylesheets) + len(scripts) + len(images) + len(font_files) + 1,
            },
            "optimizations": {
                "render_blocking_scripts_count": len(render_blocking_scripts),
                "render_blocking_scripts": render_blocking_scripts[:5],
                "resource_hints": resource_hints[:6],
                "has_font_display_swap": has_font_display_swap,
                "lazy_loaded_images": f"{lazy_images} of {len(images)}",
                "images_without_dimensions_count": len(images_without_dims),
            },
            "nextjs_performance": {
                "cls_risk_images_count": len(images_without_dims),
                "cls_risk_images": images_without_dims[:5],
                "lcp_hero_preloaded": has_lcp_preload,
                "uses_google_font_link": has_google_font_link,
                "recommendations": recommendations,
            },
        }

    # =========================================================================
    # 8. 🔍 SEO AUDIT
    # =========================================================================
    def audit_seo(self) -> dict[str, Any]:
        """Audits title, description, headings, canonical, OG tags, sitemap, robots.txt, schema, and link structure."""
        if not self.primary_soup:
            return {"score": 75, "title": "Not detected", "description": "Not detected"}

        soup = self.primary_soup

        # Title
        title_tag = soup.find("title")
        title_text = title_tag.get_text(strip=True) if title_tag else ""

        # Description
        desc_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
        desc_text = desc_tag.get("content", "").strip() if desc_tag else ""

        # Canonical
        canon_tag = soup.find("link", rel=lambda x: x and "canonical" in x)
        canonical = canon_tag.get("href", "").strip() if canon_tag else ""

        # Open Graph & Twitter
        og_title = soup.find("meta", property="og:title")
        og_desc = soup.find("meta", property="og:description")
        og_image = soup.find("meta", property="og:image")
        tw_card = soup.find("meta", attrs={"name": "twitter:card"}) or soup.find("meta", property="twitter:card")

        # Headings structure
        headings_outline = []
        for h in soup.find_all(re.compile(r"^h[1-3]$")):
            headings_outline.append({
                "level": h.name.upper(),
                "text": h.get_text(strip=True)[:70],
            })

        # Schema.org Structured Data
        schemas = soup.find_all("script", type="application/ld+json")
        schema_types = []
        for s in schemas:
            txt = s.string or ""
            types_found = re.findall(r'"@type":\s*"([^"]+)"', txt)
            schema_types.extend(types_found)

        # Links count
        links = soup.find_all("a", href=True)
        internal_count = 0
        external_count = 0
        for l in links:
            href = l.get("href", "")
            if href.startswith(("#", "javascript:", "mailto:", "tel:")):
                continue
            if href.startswith("/") or self.domain in href:
                internal_count += 1
            else:
                external_count += 1

        # Calculate score
        score = 100
        checks = []

        if title_text:
            checks.append({"name": "Page Title Tag", "status": "Passed", "detail": f"{len(title_text)} chars"})
            if len(title_text) < 20 or len(title_text) > 70:
                score -= 5
        else:
            score -= 20
            checks.append({"name": "Page Title Tag", "status": "Failed", "detail": "Missing <title> tag"})

        if desc_text:
            checks.append({"name": "Meta Description", "status": "Passed", "detail": f"{len(desc_text)} chars"})
            if len(desc_text) < 50 or len(desc_text) > 160:
                score -= 4
        else:
            score -= 15
            checks.append({"name": "Meta Description", "status": "Failed", "detail": "Missing meta description"})

        if canonical:
            checks.append({"name": "Canonical Link", "status": "Passed", "detail": canonical[:60]})
        else:
            score -= 8
            checks.append({"name": "Canonical Link", "status": "Warning", "detail": "Not specified"})

        if og_title and og_image:
            checks.append({"name": "Open Graph (Social Sharing)", "status": "Passed", "detail": "Title and image configured"})
        else:
            score -= 8
            checks.append({"name": "Open Graph (Social Sharing)", "status": "Warning", "detail": "Incomplete OG tags"})

        has_robots = bool(self.robots_txt and len(self.robots_txt) > 10)
        has_sitemap = bool(self.sitemap_xml and len(self.sitemap_xml) > 10)

        checks.append({
            "name": "robots.txt",
            "status": "Passed" if has_robots else "Not detected",
            "detail": f"{self.primary_url.rstrip('/')}/robots.txt" if has_robots else "No robots.txt found",
        })
        checks.append({
            "name": "sitemap.xml",
            "status": "Passed" if has_sitemap else "Not detected",
            "detail": f"{self.primary_url.rstrip('/')}/sitemap.xml" if has_sitemap else "No sitemap.xml detected",
        })

        score = max(min(score, 100), 25)

        return {
            "score": score,
            "title": title_text or "Not detected",
            "description": desc_text or "Not detected",
            "canonical": canonical or "Not detected",
            "open_graph": {
                "title": og_title.get("content") if og_title else "Not detected",
                "description": og_desc.get("content") if og_desc else "Not detected",
                "image": og_image.get("content") if og_image else "Not detected",
                "twitter_card": tw_card.get("content") if tw_card else "Not detected",
            },
            "structured_data": {
                "detected": bool(schemas),
                "types": list(set(schema_types)) if schema_types else ["Not detected"],
            },
            "links": {
                "internal_count": internal_count,
                "external_count": external_count,
                "total": internal_count + external_count,
            },
            "headings_outline": headings_outline[:12],
            "checks": checks,
        }

    # =========================================================================
    # 9. 🔐 SECURITY HEADERS AUDIT
    # =========================================================================
    def audit_security_headers(self) -> dict[str, Any]:
        """Audits HTTPS, HSTS, CSP, X-Frame-Options, X-Content-Type-Options, and Referrer-Policy."""
        h = self.headers
        headers_audited = []
        score = 0
        max_score = 100

        # HTTPS
        is_https = self.scheme == "https" or self.primary_url.startswith("https://")
        if is_https:
            score += 25
            headers_audited.append({"header": "HTTPS Protocol", "status": "Secure", "detail": "Connection is encrypted using TLS"})
        else:
            headers_audited.append({"header": "HTTPS Protocol", "status": "Insecure", "detail": "Site served over unencrypted HTTP"})

        # HSTS
        hsts = h.get("strict-transport-security")
        if hsts:
            score += 20
            headers_audited.append({"header": "Strict-Transport-Security (HSTS)", "status": "Enabled", "detail": hsts})
        else:
            headers_audited.append({"header": "Strict-Transport-Security (HSTS)", "status": "Not detected", "detail": "Vulnerable to SSL stripping attacks"})

        # CSP
        csp = h.get("content-security-policy")
        if csp:
            score += 20
            headers_audited.append({"header": "Content-Security-Policy (CSP)", "status": "Configured", "detail": csp[:60] + "..." if len(csp) > 60 else csp})
        else:
            headers_audited.append({"header": "Content-Security-Policy (CSP)", "status": "Not detected", "detail": "Missing restriction against XSS and injection"})

        # X-Frame-Options
        xfo = h.get("x-frame-options")
        if xfo:
            score += 15
            headers_audited.append({"header": "X-Frame-Options", "status": "Protected", "detail": xfo})
        else:
            headers_audited.append({"header": "X-Frame-Options", "status": "Not detected", "detail": "May be vulnerable to clickjacking if not controlled by CSP"})

        # X-Content-Type-Options
        xcto = h.get("x-content-type-options")
        if xcto:
            score += 10
            headers_audited.append({"header": "X-Content-Type-Options", "status": "Protected", "detail": xcto})
        else:
            headers_audited.append({"header": "X-Content-Type-Options", "status": "Not detected", "detail": "MIME sniffing prevention not explicitly enabled"})

        # Referrer-Policy
        ref_pol = h.get("referrer-policy")
        if ref_pol:
            score += 10
            headers_audited.append({"header": "Referrer-Policy", "status": "Configured", "detail": ref_pol})
        else:
            headers_audited.append({"header": "Referrer-Policy", "status": "Not detected", "detail": "Browser default referrer rules apply"})

        grade = "A+" if score >= 90 else ("A" if score >= 80 else ("B" if score >= 60 else ("C" if score >= 40 else "F")))

        return {
            "score": score,
            "grade": grade,
            "is_https": is_https,
            "headers_table": headers_audited,
        }

    # =========================================================================
    # 10. 🛠 TECHNOLOGY DETECTION
    # =========================================================================
    def detect_technologies(self) -> dict[str, Any]:
        """Detects frameworks, CMS, libraries, analytics, CDN, and hosting technologies."""
        detected_tech = []
        full_html = "\n".join(h for _, h in self.pages)
        h = self.headers

        # Categorized detection rules
        rules: list[tuple[str, str, list[str] | re.Pattern]] = [
            # Frameworks & UI
            ("React", "Framework", ["_react", "react-dom", "__REACT_DEVTOOLS_GLOBAL_HOOK__", "data-reactroot"]),
            ("Next.js", "Framework", ["__NEXT_DATA__", "/_next/static/", "next-route-announcer"]),
            ("Vue.js", "Framework", ["data-v-", "v-bind", "__vue__", "vue.runtime"]),
            ("Nuxt", "Framework", ["__NUXT__", "/_nuxt/"]),
            ("Svelte", "Framework", ["svelte-", "__svelte"]),
            ("Astro", "Framework", ["data-astro-", "astro-island"]),
            ("Angular", "Framework", ["ng-version", "ng-app", "ng-controller"]),
            ("jQuery", "Library", ["jquery.min.js", "jquery-", "window.jQuery"]),
            ("Tailwind CSS", "CSS Framework", [r"tailwind", r"\bborder-border\b", r"\bbg-background\b", r"\btext-muted-foreground\b"]),
            ("Bootstrap", "CSS Framework", ["bootstrap.min.css", "bootstrap.bundle", "col-md-", "col-lg-"]),
            
            # CMS & Site Builders
            ("WordPress", "CMS", ["wp-content", "wp-includes", "wp-json", "generator\" content=\"WordPress"]),
            ("Shopify", "E-Commerce", ["cdn.shopify.com", "Shopify.theme", "myshopify.com"]),
            ("Webflow", "CMS / Builder", ["data-wf-page", "data-wf-site", "webflow.com"]),
            ("Squarespace", "CMS / Builder", ["squarespace.com", "static1.squarespace.com"]),
            ("Framer", "CMS / Builder", ["framer-", "data-framer-name", "framerusercontent.com"]),
            ("Ghost", "CMS", ["ghost.io", "ghost-search", "generator\" content=\"Ghost"]),

            # Analytics & Tracking
            ("Google Analytics 4 (GA4)", "Analytics", ["googletagmanager.com/gtag/js", "gtag('config'"]),
            ("Google Tag Manager", "Analytics", ["googletagmanager.com/gtm.js"]),
            ("Segment", "Analytics", ["cdn.segment.com/analytics.js"]),
            ("Mixpanel", "Analytics", ["cdn.mxpnl.com", "mixpanel.init"]),
            ("Hotjar", "Analytics", ["static.hotjar.com"]),
            ("PostHog", "Analytics", ["app.posthog.com", "posthog.init"]),
            ("Plausible", "Analytics", ["plausible.io/js/script.js"]),

            # CDN & Hosting
            ("Cloudflare", "CDN / Security", [h.get("server", "").lower() == "cloudflare" or "cf-ray" in h]),
            ("Vercel", "Hosting / Edge", ["vercel.app" in self.primary_url or "x-vercel-id" in h]),
            ("Netlify", "Hosting", ["netlify.app" in self.primary_url or "x-nf-request-id" in h]),
            ("AWS CloudFront", "CDN", ["cloudfront.net" in full_html or "x-amz-cf-id" in h]),
            ("Fastly", "CDN", ["x-fastly-request-id" in h]),

            # Web Font Providers
            ("Google Fonts", "Font Provider", ["fonts.googleapis.com", "fonts.gstatic.com"]),
            ("Adobe Fonts (Typekit)", "Font Provider", ["use.typekit.net", "p.typekit.net"]),
        ]

        for name, category, signatures in rules:
            match = False
            for sig in signatures:
                if isinstance(sig, bool):
                    if sig:
                        match = True
                        break
                elif isinstance(sig, str):
                    if sig in full_html or sig in self.css_text:
                        match = True
                        break
                elif isinstance(sig, re.Pattern):
                    if sig.search(full_html) or sig.search(self.css_text):
                        match = True
                        break
            if match:
                detected_tech.append({"name": name, "category": category})

        # Integrate frameworks detected by extract_theme if not already present
        existing_names = {t["name"] for t in detected_tech}
        for fw in self.tokens.get("frameworks", {}):
            clean_name = fw.replace("_", " ").title()
            if clean_name not in existing_names:
                detected_tech.append({"name": clean_name, "category": "Framework"})

        return {
            "all_detected": detected_tech,
            "count": len(detected_tech),
            "by_category": {
                "Frameworks": [t["name"] for t in detected_tech if t["category"] == "Framework"],
                "CSS & UI": [t["name"] for t in detected_tech if t["category"] == "CSS Framework"],
                "CMS & Builders": [t["name"] for t in detected_tech if t["category"] in ("CMS", "CMS / Builder", "E-Commerce")],
                "Analytics": [t["name"] for t in detected_tech if t["category"] == "Analytics"],
                "Hosting & CDN": [t["name"] for t in detected_tech if t["category"] in ("CDN", "Hosting", "CDN / Security", "Hosting / Edge")],
                "Font Providers": [t["name"] for t in detected_tech if t["category"] == "Font Provider"],
            },
        }

    # =========================================================================
    # 11. 🔗 SITE STRUCTURE
    # =========================================================================
    def analyze_site_structure(self) -> dict[str, Any]:
        """Analyzes crawled same-site links, hierarchy, and produces a sitemap tree representation."""
        internal_pages = []
        external_domains = set()

        for page_url, html_str in self.pages:
            parsed = urlparse(page_url)
            path = parsed.path or "/"
            internal_pages.append({
                "url": page_url,
                "path": path,
                "status": 200,
            })

            # Extract child links
            if BeautifulSoup:
                try:
                    s = BeautifulSoup(html_str, "html.parser")
                    for a in s.find_all("a", href=True):
                        href = a["href"]
                        if href.startswith(("http://", "https://")):
                            ext_netloc = urlparse(href).netloc.removeprefix("www.")
                            if ext_netloc and ext_netloc != self.domain:
                                external_domains.add(ext_netloc)
                except Exception:
                    pass

        # Build tree visualization
        tree_nodes = [{"path": "/", "name": "Homepage (Root)", "depth": 0}]
        seen_paths = {"/"}
        for p in internal_pages:
            path = p["path"]
            if path not in seen_paths:
                seen_paths.add(path)
                depth = len(path.strip("/").split("/"))
                name = path.strip("/").split("/")[-1].replace("-", " ").capitalize() or "Page"
                tree_nodes.append({"path": path, "name": name, "depth": depth})

        tree_nodes.sort(key=lambda x: (x["depth"], x["path"]))

        return {
            "crawled_count": len(internal_pages),
            "internal_pages": internal_pages,
            "tree_structure": tree_nodes,
            "external_domains_count": len(external_domains),
            "sample_external_domains": list(external_domains)[:8],
        }

    # =========================================================================
    # 12. 📝 CONTENT INTELLIGENCE
    # =========================================================================
    def analyze_content(self) -> dict[str, Any]:
        """Extracts headlines, CTAs, value propositions, testimonials, pricing, and trust signals."""
        headlines = []
        ctas = []
        trust_signals = []
        pricing_signals = []
        value_prop = "Not detected"

        if self.primary_soup:
            soup = self.primary_soup

            # Headlines
            for h1 in soup.find_all("h1"):
                t = h1.get_text(strip=True)
                if t and len(t) > 5 and t not in headlines:
                    headlines.append(t)
            for h2 in soup.find_all("h2")[:5]:
                t = h2.get_text(strip=True)
                if t and len(t) > 10 and t not in headlines:
                    headlines.append(t)

            # Primary Value Proposition
            if headlines:
                value_prop = headlines[0]

            # Call to Action button labels
            for b in soup.find_all(["button", "a"]):
                text = b.get_text(strip=True)
                if text and len(text) <= 30:
                    if re.search(r"get started|start free|try free|sign up|book demo|contact sales|buy now|request access|download|explore|learn more", text, re.I):
                        if text not in ctas and len(ctas) < 8:
                            ctas.append(text)

            # Trust signals (certifications, numbers, ratings)
            full_text = soup.get_text()
            if re.search(r"\bSOC\s*2\b", full_text, re.I):
                trust_signals.append("SOC 2 Type II Certified")
            if re.search(r"\bISO\s*27001\b", full_text, re.I):
                trust_signals.append("ISO 27001 Certified")
            if re.search(r"\bGDPR\b", full_text, re.I):
                trust_signals.append("GDPR Compliant")
            if re.search(r"\bHIPAA\b", full_text, re.I):
                trust_signals.append("HIPAA Ready")

            stat_matches = re.findall(r"([0-9]+(?:\.[0-9]+)?(?:[kKmMbB]\+?|\%|\/5))\s+([A-Za-z\s]{4,25})", full_text)
            for num, label in stat_matches[:4]:
                trust_signals.append(f"{num} {label.strip()}")

            # Pricing signals
            price_matches = re.findall(r"(\$[0-9]+(?:\.[0-9]{2})?|\€[0-9]+|\£[0-9]+)(?:\s*\/\s*(?:mo|month|yr|year))?", full_text)
            if price_matches:
                pricing_signals = list(dict.fromkeys(price_matches))[:6]

        return {
            "value_proposition": value_prop,
            "key_headlines": headlines[:6],
            "primary_ctas": ctas if ctas else ["Not detected"],
            "trust_signals": trust_signals if trust_signals else ["Not detected"],
            "pricing_signals": pricing_signals if pricing_signals else ["Not detected"],
            "messaging_summary": f"Targeted online platform for {self.domain}, emphasizing '{value_prop}'." if value_prop != "Not detected" else "Standard web application presentation.",
        }

    # =========================================================================
    # 13. 🤖 AI DESIGN INSIGHTS
    # =========================================================================
    def generate_ai_design_insights(
        self, tech: dict, comp: dict, layout: dict, content: dict
    ) -> dict[str, Any]:
        """Analyzes visual style, hierarchy, consistency, separating detected facts from interpretation."""
        colors = self.tokens.get("colors", {})
        fonts = self.tokens.get("fonts", {})
        radius = self.tokens.get("radius", {})

        # Determine Archetype
        font_strs = [str(k).lower() for k in fonts.keys()]
        for v in fonts.values():
            if isinstance(v, dict):
                font_strs.append(str(v.get("generic", "")).lower())
                font_strs.append(str(v.get("family", "")).lower())
            else:
                font_strs.append(str(v).lower())
        
        archetype = "Modern SaaS / Product"
        if any("serif" in f and "sans-serif" not in f for f in font_strs):
            archetype = "Editorial & Refined"
        elif any(int(re.sub(r"[^\d]", "", str(v)) or 0) >= 16 for v in radius.values() if "px" in str(v)):
            archetype = "Playful / Consumer Friendly"
        elif any("mono" in f for f in font_strs):
            archetype = "Developer Tooling / Technical"

        # Hierarchy & Palette consistency assessment
        colors_count = len(colors)
        consistency_score = 92
        if colors_count > 40:
            consistency_score -= 10
        if len(fonts) > 3:
            consistency_score -= 8

        # Notable Patterns
        patterns = []
        if any("grid" in l for l in layout.get("layout_engines", {})):
            patterns.append("CSS Grid multi-column bento layouts")
        if self.tokens.get("shadows"):
            patterns.append("Soft layered elevation shadows")
        if self.tokens.get("gradients"):
            patterns.append("Chromatic ambient gradients")
        if any("pill" in c.lower() for c in self.tokens.get("radius", {})):
            patterns.append("Full rounded pill badges & buttons")

        return {
            "style_archetype": archetype,
            "consistency_score": max(consistency_score, 65),
            "visual_hierarchy_review": "Strong contrast between primary actions and body surfaces; typography scale creates a clear reading hierarchy.",
            "notable_patterns": patterns or ["Clean grid layouts", "System typography", "Structured containers"],
            "facts_vs_interpretation": {
                "detected_facts": [
                    f"{len(colors)} distinct color values extracted from stylesheets",
                    f"{len(fonts)} font families detected ({', '.join(list(fonts.keys())[:3])})",
                    f"{len(comp.get('detected', []))} UI component patterns identified",
                    f"HTTP security rating graded at {self.audit_security_headers().get('grade')}",
                ],
                "ai_interpretation": [
                    f"Aesthetic categorised as '{archetype}' based on font selection and corner radius hierarchy.",
                    "Design system emphasizes high-velocity conversion with focused call-to-action color weighting.",
                    "Layout structure indicates a mobile-responsive viewport strategy with standard desktop containers.",
                ],
            },
        }

    # =========================================================================
    # T1a. 🏷  SEMANTIC TOKEN NAMING
    # =========================================================================
    def name_semantic_tokens(self) -> dict[str, Any]:
        """Assigns semantic CSS variable names and roles to raw extracted hex color values.

        Uses luminance, saturation, and hue analysis to classify each color into a meaningful
        role: brand-primary, brand-accent, surface-base, text-primary, feedback-success, etc.
        Also detects WCAG AA contrast pairs (background + foreground).
        """
        colors = self.tokens.get("colors", {})
        if not colors:
            return {"named_tokens": [], "contrast_pairs": [], "summary": "No colors extracted"}

        def hex_to_rgb(hex_str: str) -> tuple[int, int, int] | None:
            """Convert a hex color string to (r, g, b) tuple."""
            s = str(hex_str).strip().lstrip("#")
            if len(s) == 3:
                s = s[0]*2 + s[1]*2 + s[2]*2
            if len(s) < 6:
                return None
            try:
                return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
            except ValueError:
                return None

        def relative_luminance(r: int, g: int, b: int) -> float:
            """WCAG relative luminance (0=black, 1=white)."""
            def linearize(c: float) -> float:
                c = c / 255.0
                return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
            return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)

        def saturation(r: int, g: int, b: int) -> float:
            """HSL saturation 0.0–1.0."""
            r_, g_, b_ = r / 255.0, g / 255.0, b / 255.0
            cmax, cmin = max(r_, g_, b_), min(r_, g_, b_)
            delta = cmax - cmin
            if delta == 0:
                return 0.0
            l = (cmax + cmin) / 2.0
            return delta / (1.0 - abs(2 * l - 1.0)) if l != 0.5 else delta / (1.0 - abs(2 * l - 1.0))

        def hue_name(r: int, g: int, b: int) -> str:
            """Rough hue family (red/green/blue/yellow/purple/cyan/neutral)."""
            r_, g_, b_ = r / 255.0, g / 255.0, b / 255.0
            cmax = max(r_, g_, b_)
            cmin = min(r_, g_, b_)
            delta = cmax - cmin
            if delta < 0.06:
                return "neutral"
            if cmax == r_:
                h = 60 * (((g_ - b_) / delta) % 6)
            elif cmax == g_:
                h = 60 * (((b_ - r_) / delta) + 2)
            else:
                h = 60 * (((r_ - g_) / delta) + 4)
            h = h % 360
            if h < 20 or h >= 340:
                return "red"
            if h < 45:
                return "orange"
            if h < 70:
                return "yellow"
            if h < 165:
                return "green"
            if h < 195:
                return "cyan"
            if h < 260:
                return "blue"
            if h < 300:
                return "purple"
            return "pink"

        def wcag_contrast(lum1: float, lum2: float) -> float:
            lighter = max(lum1, lum2)
            darker = min(lum1, lum2)
            return (lighter + 0.05) / (darker + 0.05)

        # Analyze each color
        analyzed: list[dict] = []
        for raw_name, hex_val in colors.items():
            if not isinstance(hex_val, str) or not hex_val.startswith("#"):
                continue
            rgb = hex_to_rgb(hex_val)
            if not rgb:
                continue
            r, g, b = rgb
            lum = relative_luminance(r, g, b)
            sat = saturation(r, g, b)
            hue = hue_name(r, g, b)
            analyzed.append({
                "raw_name": raw_name,
                "hex": hex_val,
                "luminance": lum,
                "saturation": sat,
                "hue": hue,
            })

        if not analyzed:
            return {"named_tokens": [], "contrast_pairs": [], "summary": "No valid hex colors to classify"}

        analyzed.sort(key=lambda x: x["luminance"])

        # Role assignment — ordered by priority
        role_slots: dict[str, str] = {}  # role -> hex
        named_tokens: list[dict] = []

        def claim_role(role: str, hex_val: str) -> bool:
            if role not in role_slots:
                role_slots[role] = hex_val
                return True
            return False

        # Pass 1: Classify by luminance extremes for surface/text
        very_dark = [c for c in analyzed if c["luminance"] < 0.06]
        very_light = [c for c in analyzed if c["luminance"] > 0.85]
        dark_mid = [c for c in analyzed if 0.06 <= c["luminance"] < 0.25]
        light_mid = [c for c in analyzed if 0.5 <= c["luminance"] <= 0.85]
        chromatic = [c for c in analyzed if c["saturation"] > 0.3]

        for c in very_dark[:1]:
            claim_role("surface-base", c["hex"])
        for c in very_dark[1:2]:
            claim_role("surface-elevated", c["hex"])
        for c in very_light[:1]:
            claim_role("text-on-dark", c["hex"])
        for c in very_light[1:2]:
            claim_role("surface-overlay", c["hex"])
        for c in dark_mid[:1]:
            claim_role("text-primary", c["hex"])
        for c in dark_mid[1:2]:
            claim_role("text-muted", c["hex"])
        for c in light_mid[:1]:
            claim_role("text-subtle", c["hex"])

        # Pass 2: Most saturated chromatic colors → brand roles
        sorted_chroma = sorted(chromatic, key=lambda x: x["saturation"], reverse=True)
        brand_idx = 0
        brand_labels = ["brand-primary", "brand-accent", "brand-secondary"]
        for c in sorted_chroma:
            if brand_idx >= len(brand_labels):
                break
            if c["hex"] not in role_slots.values():
                claim_role(brand_labels[brand_idx], c["hex"])
                brand_idx += 1

        # Pass 3: Hue-semantic feedback colors
        for c in analyzed:
            if c["hue"] == "green" and c["saturation"] > 0.4 and "feedback-success" not in role_slots:
                claim_role("feedback-success", c["hex"])
            elif c["hue"] == "red" and c["saturation"] > 0.4 and "feedback-danger" not in role_slots:
                claim_role("feedback-danger", c["hex"])
            elif c["hue"] in ("yellow", "orange") and c["saturation"] > 0.4 and "feedback-warning" not in role_slots:
                claim_role("feedback-warning", c["hex"])
            elif c["hue"] == "cyan" and c["saturation"] > 0.3 and "feedback-info" not in role_slots:
                claim_role("feedback-info", c["hex"])

        # Reverse map: hex -> role
        hex_to_role = {v: k for k, v in role_slots.items()}

        # Build named token list
        role_counter: dict[str, int] = {}
        for c in analyzed:
            hex_val = c["hex"]
            role = hex_to_role.get(hex_val)
            if not role:
                # Fallback: assign a positional neutral name
                hue = c["hue"]
                role_counter[hue] = role_counter.get(hue, 0) + 1
                idx = role_counter[hue]
                role = f"{hue}-{idx:02d}" if idx > 1 else hue

            css_var = f"--color-{role}"
            named_tokens.append({
                "hex": hex_val,
                "role": role,
                "css_variable": css_var,
                "luminance": round(c["luminance"], 3),
                "saturation": round(c["saturation"], 3),
                "hue_family": c["hue"],
                "usage_class": (
                    "brand" if "brand" in role
                    else "surface" if "surface" in role
                    else "text" if "text" in role
                    else "feedback" if "feedback" in role
                    else "neutral"
                ),
            })

        # WCAG AA Contrast Pairs
        contrast_pairs: list[dict] = []
        lum_by_hex = {c["hex"]: c["luminance"] for c in analyzed}
        bg_candidates = [t for t in named_tokens if t["usage_class"] in ("surface", "neutral") and t["luminance"] < 0.4]
        fg_candidates = [t for t in named_tokens if t["usage_class"] in ("text", "brand") or t["luminance"] > 0.4]
        seen_pairs: set[tuple] = set()
        for bg in bg_candidates[:4]:
            for fg in fg_candidates[:6]:
                key = (bg["hex"], fg["hex"])
                if key in seen_pairs:
                    continue
                seen_pairs.add(key)
                contrast = wcag_contrast(bg["luminance"], fg["luminance"])
                if contrast >= 3.0:
                    wcag_level = "AAA" if contrast >= 7.0 else ("AA" if contrast >= 4.5 else "AA Large")
                    contrast_pairs.append({
                        "background": bg["hex"],
                        "background_role": bg["role"],
                        "foreground": fg["hex"],
                        "foreground_role": fg["role"],
                        "contrast_ratio": round(contrast, 2),
                        "wcag_level": wcag_level,
                    })
        contrast_pairs.sort(key=lambda x: x["contrast_ratio"], reverse=True)

        # CSS output block
        css_lines = [":root {"]
        for t in named_tokens:
            css_lines.append(f"  {t['css_variable']}: {t['hex']};")
        css_lines.append("}")

        return {
            "named_tokens": named_tokens,
            "contrast_pairs": contrast_pairs[:8],
            "css_block": "\n".join(css_lines),
            "summary": (
                f"{len(named_tokens)} colors named: "
                f"{sum(1 for t in named_tokens if t['usage_class'] == 'brand')} brand, "
                f"{sum(1 for t in named_tokens if t['usage_class'] == 'surface')} surface, "
                f"{sum(1 for t in named_tokens if t['usage_class'] == 'text')} text, "
                f"{sum(1 for t in named_tokens if t['usage_class'] == 'feedback')} feedback"
            ),
        }

    # =========================================================================
    # T1b. 📏  VISUAL CONSISTENCY SCORE
    # =========================================================================
    def score_visual_consistency(self) -> dict[str, Any]:
        """Computes a 0–100 visual discipline score across color, typography, spacing, and radius.

        Low scores surface actionable issues with specific recommendations for tightening
        the design system. Grade: A (90+), B (75+), C (60+), D (45+), F (<45).
        """
        colors = self.tokens.get("colors", {})
        fonts = self.tokens.get("fonts", {})
        font_sizes = self.tokens.get("font_sizes", {})
        font_weights = self.tokens.get("font_weights", {})
        spacing = self.tokens.get("spacing", {})
        radius = self.tokens.get("radius", {})
        shadows = self.tokens.get("shadows", {})
        gradients = self.tokens.get("gradients", [])

        issues: list[dict] = []
        breakdown: dict[str, dict] = {}

        # ── COLOR ECONOMY ─────────────────────────────────────────────────────
        color_score = 100
        total_colors = len(colors)
        # Unique chromatic colors (saturated ones) are the signal — too many = rogue colors
        # Heuristic: SaaS systems use 3-8 semantic colors; editorial may use 10-15
        if total_colors > 60:
            color_score -= 35
            issues.append({
                "dimension": "Color Economy",
                "severity": "High",
                "message": f"{total_colors} unique color values detected — typical design systems use 8–20 semantic tokens.",
                "recommendation": "Consolidate to a token-based palette. Reduce one-off hex values to named CSS variables.",
            })
        elif total_colors > 35:
            color_score -= 20
            issues.append({
                "dimension": "Color Economy",
                "severity": "Medium",
                "message": f"{total_colors} color values found. Consider reducing to under 20 semantic tokens for maintainability.",
                "recommendation": "Group similar tones into a single token with opacity variants (e.g. --color-primary at 10%, 20%).",
            })
        elif total_colors > 20:
            color_score -= 8
        breakdown["color_economy"] = {
            "score": max(color_score, 20),
            "total_colors": total_colors,
            "label": "Excellent" if color_score >= 90 else ("Good" if color_score >= 70 else ("Fair" if color_score >= 50 else "Poor")),
        }

        # ── TYPOGRAPHY DISCIPLINE ──────────────────────────────────────────────
        type_score = 100
        font_family_count = len([k for k in fonts if not str(k).startswith("_")])
        weight_count = len(font_weights) if isinstance(font_weights, dict) else len(set(font_weights)) if font_weights else 0
        size_count = len(font_sizes) if isinstance(font_sizes, dict) else len(set(font_sizes)) if font_sizes else 0

        if font_family_count > 3:
            type_score -= 25
            issues.append({
                "dimension": "Typography",
                "severity": "High",
                "message": f"{font_family_count} font families detected. Most design systems use 1–2 typefaces.",
                "recommendation": "Reduce to a primary body font + optional mono or display font. Remove decorative one-offs.",
            })
        elif font_family_count > 2:
            type_score -= 10
            issues.append({
                "dimension": "Typography",
                "severity": "Low",
                "message": f"{font_family_count} font families in use. Consider consolidating to 2.",
                "recommendation": "Evaluate whether the third family serves a distinct visual purpose.",
            })

        if weight_count > 5:
            type_score -= 15
            issues.append({
                "dimension": "Typography",
                "severity": "Medium",
                "message": f"{weight_count} font weights loaded. Loading more than 4 weights adds unnecessary network payload.",
                "recommendation": "Restrict to Regular (400), Medium (500), SemiBold (600), Bold (700) to save 30–50% font load.",
            })

        if size_count > 10:
            type_score -= 10
            issues.append({
                "dimension": "Typography",
                "severity": "Low",
                "message": f"{size_count} font-size values found — no clear modular scale detected.",
                "recommendation": "Adopt a modular type scale (1.25x or Major Third) to create proportional hierarchy.",
            })
        breakdown["typography"] = {
            "score": max(type_score, 20),
            "font_families": font_family_count,
            "font_weights": weight_count,
            "font_sizes": size_count,
            "label": "Excellent" if type_score >= 90 else ("Good" if type_score >= 70 else ("Fair" if type_score >= 50 else "Poor")),
        }

        # ── SPACING DISCIPLINE ─────────────────────────────────────────────────
        spacing_score = 100
        spacing_vals: list[int] = []
        for v in (spacing.values() if isinstance(spacing, dict) else spacing):
            m = re.match(r"^([0-9]+(?:\.[0-9]+)?)", str(v))
            if m:
                spacing_vals.append(int(float(m.group(1))))

        if spacing_vals:
            # Test 8pt grid adherence
            on_grid_8 = sum(1 for v in spacing_vals if v % 8 == 0 or v % 4 == 0)
            adherence = on_grid_8 / len(spacing_vals)
            if adherence < 0.5:
                spacing_score -= 30
                issues.append({
                    "dimension": "Spacing",
                    "severity": "High",
                    "message": f"Only {round(adherence*100)}% of spacing values align to a 4pt/8pt grid system.",
                    "recommendation": "Adopt an 8pt grid: use multiples of 8 (8, 16, 24, 32, 48, 64) for all margin, padding, and gap values.",
                })
            elif adherence < 0.75:
                spacing_score -= 15
                issues.append({
                    "dimension": "Spacing",
                    "severity": "Medium",
                    "message": f"{round(adherence*100)}% of spacing values are on-grid. Some rogue values detected.",
                    "recommendation": "Review and snap off-grid values to the nearest 4pt multiple.",
                })
            unique_vals = len(set(spacing_vals))
            if unique_vals > 20:
                spacing_score -= 10
                issues.append({
                    "dimension": "Spacing",
                    "severity": "Low",
                    "message": f"{unique_vals} distinct spacing values — consider tokenizing into a scale (xs/sm/md/lg/xl).",
                    "recommendation": "Define named spacing tokens: --space-1 through --space-16 and use only those values.",
                })
        breakdown["spacing"] = {
            "score": max(spacing_score, 20),
            "unique_values": len(set(spacing_vals)) if spacing_vals else 0,
            "label": "Excellent" if spacing_score >= 90 else ("Good" if spacing_score >= 70 else ("Fair" if spacing_score >= 50 else "Poor")),
        }

        # ── RADIUS CONSISTENCY ─────────────────────────────────────────────────
        radius_score = 100
        radius_vals: list[str] = list(radius.values()) if isinstance(radius, dict) else list(radius)
        unique_radii = len(set(str(v) for v in radius_vals))
        if unique_radii > 6:
            radius_score -= 20
            issues.append({
                "dimension": "Border Radius",
                "severity": "Medium",
                "message": f"{unique_radii} distinct border-radius values — no consistent scale detected.",
                "recommendation": "Define 4–5 radius tokens: --radius-sm, --radius-md, --radius-lg, --radius-full and reuse them.",
            })
        elif unique_radii > 4:
            radius_score -= 8
        breakdown["border_radius"] = {
            "score": max(radius_score, 20),
            "unique_values": unique_radii,
            "label": "Excellent" if radius_score >= 90 else ("Good" if radius_score >= 70 else ("Fair" if radius_score >= 50 else "Poor")),
        }

        # ── SHADOW DEPTH LEVELS ────────────────────────────────────────────────
        shadow_score = 100
        shadow_vals = list(shadows.values()) if isinstance(shadows, dict) else list(shadows) if shadows else []
        unique_shadows = len(set(str(s) for s in shadow_vals))
        if unique_shadows > 8:
            shadow_score -= 15
            issues.append({
                "dimension": "Shadow System",
                "severity": "Low",
                "message": f"{unique_shadows} unique shadow definitions found. A well-structured elevation system uses 3–5 levels.",
                "recommendation": "Define shadow tokens: --shadow-xs, --shadow-sm, --shadow-md, --shadow-lg, --shadow-glow.",
            })
        breakdown["shadows"] = {
            "score": max(shadow_score, 40),
            "unique_values": unique_shadows,
            "label": "Excellent" if shadow_score >= 90 else ("Good" if shadow_score >= 70 else ("Fair" if shadow_score >= 50 else "Poor")),
        }

        # ── OVERALL SCORE ──────────────────────────────────────────────────────
        weights = {"color_economy": 0.3, "typography": 0.25, "spacing": 0.25, "border_radius": 0.1, "shadows": 0.1}
        overall = round(sum(breakdown[k]["score"] * w for k, w in weights.items()))
        overall = max(min(overall, 100), 20)
        grade = "A" if overall >= 90 else ("B" if overall >= 75 else ("C" if overall >= 60 else ("D" if overall >= 45 else "F")))

        return {
            "score": overall,
            "grade": grade,
            "label": "Excellent" if overall >= 90 else ("Good" if overall >= 75 else ("Fair" if overall >= 60 else ("Needs Work" if overall >= 45 else "Poor"))),
            "breakdown": breakdown,
            "issues": issues,
            "positive": [
                f"Consistent {len(colors)}-color system" if total_colors <= 20 else None,
                f"Clean {font_family_count}-family typeface selection" if font_family_count <= 2 else None,
                "Shadow elevation system defined" if 2 <= unique_shadows <= 6 else None,
                "Radius scale is well-contained" if unique_radii <= 4 else None,
            ],
        }

    # =========================================================================
    # T1c. 📐  SPACING GRID DETECTION
    # =========================================================================
    def detect_spacing_grid(self) -> dict[str, Any]:
        """Detects the underlying spacing base unit (4pt, 8pt, 12pt) from extracted spacing values.

        Calculates adherence percentage, lists off-grid rogue values, and generates the
        canonical grid scale so developers know which values to use.
        """
        spacing = self.tokens.get("spacing", {})

        # Extract numeric pixel values from spacing tokens
        raw_vals: list[int] = []
        for v in (spacing.values() if isinstance(spacing, dict) else spacing):
            m = re.match(r"^([0-9]+(?:\.[0-9]+)?)", str(v))
            if m:
                val = float(m.group(1))
                if 0 < val <= 256:  # Ignore 0 and unreasonably large values
                    raw_vals.append(int(round(val)))

        # Also extract spacing from raw CSS
        css_spacing = re.findall(
            r"(?:margin|padding|gap|top|left|right|bottom|row-gap|column-gap):\s*([0-9]+(?:\.[0-9]+)?)px",
            self.css_text, re.I
        )
        for v in css_spacing:
            val = int(round(float(v)))
            if 0 < val <= 256:
                raw_vals.append(val)

        if not raw_vals:
            return {
                "detected": False,
                "base_unit": None,
                "system_name": "Not enough spacing data",
                "adherence_pct": 0,
                "grid_scale": [],
                "off_grid_values": [],
                "summary": "No spacing values found in extracted tokens or CSS.",
            }

        # Find best-fit base unit
        all_vals = list(set(raw_vals))
        best_base = 8
        best_adherence = 0.0
        for base in (4, 8, 12, 16):
            on_grid = sum(1 for v in all_vals if v % base == 0)
            adherence = on_grid / len(all_vals)
            if adherence > best_adherence:
                best_adherence = adherence
                best_base = base

        # Also check 4pt sub-grid (if 8pt wins but 4pt captures more)
        on_grid_4 = sum(1 for v in all_vals if v % 4 == 0)
        on_grid_best = sum(1 for v in all_vals if v % best_base == 0)
        # Prefer 8pt unless 4pt gives significantly more coverage
        if best_base == 4:
            on_grid_8 = sum(1 for v in all_vals if v % 8 == 0)
            if on_grid_8 / len(all_vals) >= 0.55:
                best_base = 8
                best_adherence = on_grid_8 / len(all_vals)

        adherence_pct = round(best_adherence * 100)
        system_name = f"{best_base}pt Grid System"
        if adherence_pct < 40:
            system_name = "No clear grid system"
        elif adherence_pct < 60:
            system_name = f"Loose {best_base}pt Grid"

        # Off-grid values
        off_grid: list[dict] = []
        for v in sorted(set(all_vals)):
            if v % best_base != 0:
                nearest_lower = (v // best_base) * best_base
                nearest_upper = nearest_lower + best_base
                nearest = nearest_upper if (v - nearest_lower) > (nearest_upper - v) else nearest_lower
                off_grid.append({
                    "value": v,
                    "css": f"{v}px",
                    "nearest_snap": f"{max(nearest, best_base)}px",
                    "deviation": abs(v - nearest),
                })

        # Canonical grid scale for this base unit
        scale_steps = [best_base * i for i in range(1, 17)]  # 1x through 16x
        grid_scale = [
            {
                "step": i + 1,
                "px": f"{val}px",
                "rem": f"{val/16:.3f}rem",
                "token_name": f"--space-{i+1}",
                "used": val in all_vals,
            }
            for i, val in enumerate(scale_steps)
        ]

        return {
            "detected": adherence_pct >= 40,
            "base_unit": best_base,
            "system_name": system_name,
            "adherence_pct": adherence_pct,
            "total_values_analyzed": len(all_vals),
            "on_grid_count": sum(1 for v in all_vals if v % best_base == 0),
            "off_grid_count": len(off_grid),
            "off_grid_values": off_grid[:12],
            "grid_scale": grid_scale,
            "summary": (
                f"{system_name} detected with {adherence_pct}% adherence. "
                f"{len(off_grid)} off-grid values need snapping."
            ),
        }

    # =========================================================================
    # T1d. 🚀  FRAMEWORK-AWARE EXPORTS
    # =========================================================================
    def generate_framework_exports(self, tech: dict | None = None) -> dict[str, Any]:
        """Generates correctly-formatted token exports based on the detected technology stack.

        - Tailwind CSS detected → tailwind.config.js with theme.extend
        - Next.js / React detected → TypeScript theme.ts + globals.css
        - Vue / Nuxt detected → CSS tokens + useTokens() composable
        - Default → Clean tokens.css + W3C tokens.json
        Always includes: DESIGN.md summary, CSS custom properties, JSON tokens.
        """
        colors = self.tokens.get("colors", {})
        fonts = self.tokens.get("fonts", {})
        spacing = self.tokens.get("spacing", {})
        radius = self.tokens.get("radius", {})
        shadows = self.tokens.get("shadows", {})
        primary_color = list(colors.values())[0] if colors else "#4f46e5"
        domain = self.domain

        # Determine detected frameworks from tech audit
        by_cat = (tech or {}).get("by_category", {})
        frameworks = by_cat.get("Frameworks", [])
        css_libs = by_cat.get("CSS & UI", [])
        uses_tailwind = "Tailwind CSS" in css_libs
        uses_nextjs = "Next.js" in frameworks
        uses_vue = any(f in frameworks for f in ["Vue.js", "Nuxt"])
        uses_react = "React" in frameworks or uses_nextjs

        # ── 1. CSS CUSTOM PROPERTIES (always generated) ─────────────────────
        css_vars_lines = [f"/* Design tokens for {domain} — generated by ExtractDesign Studio */", ":root {"]
        semantic = self.name_semantic_tokens()
        for t in semantic.get("named_tokens", []):
            css_vars_lines.append(f"  {t['css_variable']}: {t['hex']};")
        for f_k, f_v in fonts.items():
            if not str(f_k).startswith("_"):
                val = f_v if isinstance(f_v, str) else f_v.get("family", str(f_v)) if isinstance(f_v, dict) else str(f_v)
                css_vars_lines.append(f"  --font-{f_k}: {val};")
        for r_k, r_v in list(radius.items())[:6]:
            css_vars_lines.append(f"  --radius-{r_k}: {r_v};")
        sp_items = list(spacing.items()) if isinstance(spacing, dict) else [(str(i), v) for i, v in enumerate(spacing)]
        for s_k, s_v in sp_items[:12]:
            css_vars_lines.append(f"  --space-{s_k}: {s_v};")
        css_vars_lines.append("}")
        css_vars_output = "\n".join(css_vars_lines)

        # ── 2. W3C FORMAT JSON TOKENS (always generated) ─────────────────────
        w3c_tokens: dict = {"$schema": "https://tr.designtokens.org/format/", "color": {}, "typography": {}, "spacing": {}, "radius": {}}
        for t in semantic.get("named_tokens", []):
            role = t["role"].replace("-", ".")  # nested W3C path
            w3c_tokens["color"][t["role"]] = {"$value": t["hex"], "$type": "color"}
        for f_k, f_v in fonts.items():
            if not str(f_k).startswith("_"):
                val = f_v if isinstance(f_v, str) else f_v.get("family", str(f_v)) if isinstance(f_v, dict) else str(f_v)
                w3c_tokens["typography"][f_k] = {"$value": val, "$type": "fontFamily"}
        for r_k, r_v in list(radius.items())[:6]:
            w3c_tokens["radius"][r_k] = {"$value": str(r_v), "$type": "dimension"}
        import json as _json
        json_tokens_output = _json.dumps(w3c_tokens, indent=2, ensure_ascii=False)

        # ── 3. TAILWIND CONFIG (if Tailwind detected) ─────────────────────────
        tailwind_output = ""
        if uses_tailwind:
            color_entries = ""
            for t in semantic.get("named_tokens", []):
                key = t["role"].replace("-", "_")
                color_entries += f"      '{key}': '{t['hex']}',\n"
            font_entries = ""
            for f_k, f_v in fonts.items():
                if not str(f_k).startswith("_"):
                    val = f_v if isinstance(f_v, str) else f_v.get("family", str(f_v)) if isinstance(f_v, dict) else str(f_v)
                    font_entries += f"      '{f_k}': ['{val}', 'sans-serif'],\n"
            radius_entries = ""
            for r_k, r_v in list(radius.items())[:6]:
                radius_entries += f"      '{r_k}': '{r_v}',\n"
            spacing_entries = ""
            for s_k, s_v in sp_items[:12]:
                spacing_entries += f"      '{s_k}': '{s_v}',\n"
            tailwind_output = f"""// tailwind.config.js — {domain}
// Auto-generated by ExtractDesign Studio from extracted design tokens

/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: [
    './app/**/*.{{js,ts,jsx,tsx,mdx}}',
    './components/**/*.{{js,ts,jsx,tsx,mdx}}',
    './pages/**/*.{{js,ts,jsx,tsx,mdx}}',
  ],
  theme: {{
    extend: {{
      colors: {{
{color_entries}    }},
      fontFamily: {{
{font_entries}    }},
      borderRadius: {{
{radius_entries}    }},
      spacing: {{
{spacing_entries}    }},
    }},
  }},
  plugins: [],
}};
"""

        # ── 4. TYPESCRIPT THEME (if React/Next.js detected) ───────────────────
        typescript_theme = ""
        if uses_react:
            color_ts = ""
            for t in semantic.get("named_tokens", []):
                key = t["role"].replace("-", "_").replace(".", "_")
                color_ts += f"  {key}: '{t['hex']}',\n"
            font_ts = ""
            for f_k, f_v in fonts.items():
                if not str(f_k).startswith("_"):
                    val = f_v if isinstance(f_v, str) else f_v.get("family", str(f_v)) if isinstance(f_v, dict) else str(f_v)
                    font_ts += f"  {f_k}: '{val}',\n"
            typescript_theme = f"""// theme.ts — {domain}
// Auto-generated by ExtractDesign Studio
// Import and use in _app.tsx, layout.tsx, or ThemeProvider

export const theme = {{
  colors: {{
{color_ts}  }},
  fonts: {{
{font_ts}  }},
  borderRadius: {{
    sm: '{list(radius.values())[0] if radius else "4px"}',
    md: '{list(radius.values())[1] if len(radius) > 1 else "8px"}',
    lg: '{list(radius.values())[2] if len(radius) > 2 else "16px"}',
    full: '9999px',
  }},
}} as const;

export type ThemeColors = keyof typeof theme.colors;
export type ThemeFonts = keyof typeof theme.fonts;
"""

        # ── 5. VUE COMPOSABLE (if Vue/Nuxt detected) ──────────────────────────
        vue_composable = ""
        if uses_vue:
            color_obj = ", ".join(f"{t['role'].replace('-', '_')}: '{t['hex']}'" for t in semantic.get("named_tokens", [])[:10])
            vue_composable = f"""// composables/useTokens.ts — {domain}
// Auto-generated by ExtractDesign Studio

export function useTokens() {{
  const colors = reactive({{
    {color_obj}
  }});

  return {{ colors }};
}}
"""

        # ── 6. FIGMA TOKENS (Tokens Studio standard format) ──────────────────
        figma_dict: dict = {
            "global": {
                "color": {},
                "fontFamilies": {},
                "borderRadius": {},
                "spacing": {},
            }
        }
        for t in semantic.get("named_tokens", []):
            role_key = t["role"].replace("-", "_")
            figma_dict["global"]["color"][role_key] = {"value": t["hex"], "type": "color"}
        for f_k, f_v in fonts.items():
            if not str(f_k).startswith("_"):
                val = f_v if isinstance(f_v, str) else f_v.get("family", str(f_v)) if isinstance(f_v, dict) else str(f_v)
                figma_dict["global"]["fontFamilies"][str(f_k)] = {"value": val, "type": "fontFamilies"}
        for r_k, r_v in list(radius.items())[:6]:
            figma_dict["global"]["borderRadius"][str(r_k)] = {"value": str(r_v), "type": "borderRadius"}
        for s_k, s_v in sp_items[:12]:
            figma_dict["global"]["spacing"][str(s_k)] = {"value": str(s_v), "type": "spacing"}
        figma_tokens_output = _json.dumps(figma_dict, indent=2, ensure_ascii=False)

        # ── 7. DESIGN.md DOCUMENTATION ────────────────────────────────────────
        design_md_lines = [
            f"# {domain.split('.')[0].capitalize()} — Design System Reference",
            f"> Reverse-engineered by ExtractDesign Studio",
            "",
            "## Color Palette",
        ]
        for t in semantic.get("named_tokens", []):
            design_md_lines.append(f"- `{t['css_variable']}` → `{t['hex']}` ({t['role']})")
        design_md_lines += ["", "## Typography"]
        for f_k, f_v in fonts.items():
            if not str(f_k).startswith("_"):
                val = f_v if isinstance(f_v, str) else f_v.get("family", str(f_v)) if isinstance(f_v, dict) else str(f_v)
                design_md_lines.append(f"- `{f_k}`: {val}")
        design_md_lines += ["", "## Border Radius"]
        for r_k, r_v in list(radius.items())[:6]:
            design_md_lines.append(f"- `--radius-{r_k}`: {r_v}")
        design_md_lines += ["", "## Spacing Scale"]
        for s_k, s_v in sp_items[:12]:
            design_md_lines.append(f"- `--space-{s_k}`: {s_v}")
        design_md_lines += ["", "---", "> All design assets remain property of their respective owners."]
        design_md_output = "\n".join(design_md_lines)

        # ── DETERMINE ACTIVE FORMAT ────────────────────────────────────────────
        primary_format = (
            "tailwind" if uses_tailwind
            else "typescript" if uses_react
            else "vue" if uses_vue
            else "css"
        )
        framework_label = (
            "Tailwind CSS" if uses_tailwind
            else "Next.js / React (TypeScript)" if uses_nextjs
            else "React (TypeScript)" if uses_react
            else "Vue / Nuxt" if uses_vue
            else "Vanilla CSS"
        )

        return {
            "primary_format": primary_format,
            "framework_detected": framework_label,
            "css_variables": css_vars_output,
            "json_tokens_w3c": json_tokens_output,
            "figma_tokens": figma_tokens_output,
            "tailwind_config": tailwind_output,
            "typescript_theme": typescript_theme,
            "vue_composable": vue_composable,
            "design_md": design_md_output,
            # Legacy field kept for backward compatibility
            "react_components": self._generate_react_components(primary_color),
        }

    def _generate_react_components(self, primary_color: str) -> str:
        """Generates Next.js App Router component templates (legacy export, kept for compatibility)."""
        return f"""// Next.js App Router Components for {self.domain}
// Optimized for Core Web Vitals (LCP < 2.5s, CLS < 0.1, INP < 200ms)
// Generated by ExtractDesign Studio

import React from 'react';
import Image from 'next/image';

'use client';
export function Button({{ children, variant = 'primary', className = '', ...props }}) {{
  const styles = {{
    primary: {{ backgroundColor: 'var(--color-brand-primary, {primary_color})', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '8px', fontWeight: 600, cursor: 'pointer' }},
    secondary: {{ backgroundColor: 'transparent', border: '1px solid rgba(128,128,128,0.3)', padding: '10px 20px', borderRadius: '8px', fontWeight: 600, cursor: 'pointer' }},
  }};
  return <button style={{styles[variant]}} className={{className}} {{...props}}>{{children}}</button>;
}}

export function Hero({{ headline, description, ctaText = 'Get Started', imageSrc }}) {{
  return (
    <section style={{{{ padding: '64px 24px', textAlign: 'center', maxWidth: '960px', margin: '0 auto' }}}}>
      <h1 style={{{{ fontSize: '42px', fontWeight: 700, marginBottom: '16px' }}}}>{{headline}}</h1>
      <p style={{{{ fontSize: '18px', opacity: 0.8, marginBottom: '28px' }}}}>{{description}}</p>
      {{imageSrc && <Image src={{imageSrc}} alt={{headline}} width={{800}} height={{450}} priority />}}
      <Button>{{ctaText}}</Button>
    </section>
  );
}}
"""

    # =========================================================================
    # 14. EXPORT GENERATOR (legacy - now calls generate_framework_exports)
    # =========================================================================
    def generate_exports(self):
        return self.generate_framework_exports(None)
