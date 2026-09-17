#!/usr/bin/env python3
"""
extract-theme web server — hostable web UI backend for design system extraction.
"""

from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import zipfile
from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from storage import get_mime_type, storage

BASE_DIR = Path(__file__).parent.resolve()
PUBLIC_DIR = BASE_DIR / "public"
DOWNLOADED_THEMES_DIR = BASE_DIR / "downloaded-themes"



class ExtractThemeHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def __init__(self, *args, **kwargs):
        target_dir = str(PUBLIC_DIR) if PUBLIC_DIR.exists() else str(BASE_DIR)
        super().__init__(*args, directory=target_dir, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=()")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self' 'unsafe-inline' 'unsafe-eval' https: data: blob:; "
            "img-src 'self' https: data: blob:; font-src 'self' https: data:; "
            "style-src 'self' 'unsafe-inline' https:; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; "
            "frame-ancestors 'self';"
        )
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"

        if path in ("/api/health", "/healthz", "/health", "/api"):
            return self._send_json({
                "status": "ok",
                "storage_configured": storage.is_configured(),
                "service": "extract-theme"
            })

        if path == "/api/download":
            return self._handle_download_project(parsed)

        if path == "/api/intelligence":
            return self._handle_get_intelligence(parsed)

        if path == "/api/projects":
            return self._handle_get_projects()

        if path.startswith("/output/"):
            return self._handle_serve_output(path[8:])

        if path in ("/", "/landing", "/landing.html"):
            landing_file = PUBLIC_DIR / "landing.html"
            if landing_file.exists():
                content = landing_file.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        if path in ("/studio", "/app", "/workbench"):
            index_file = PUBLIC_DIR / "index.html"
            if index_file.exists():
                content = index_file.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        if PUBLIC_DIR.exists():
            return super().do_GET()

        self.send_error(404, "Not found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/api/extract":
            return self._handle_post_extract()

        if path in ("/api/auth/magic-link", "/api/magic-link"):
            return self._handle_magic_link()

        self.send_error(404, "Endpoint not found")

    def _handle_magic_link(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        try:
            payload = json.loads(post_data.decode("utf-8"))
        except Exception:
            return self._send_json({"error": "Invalid JSON body"}, status=400)

        email = payload.get("email", "").strip().lower()
        if not email or "@" not in email or "." not in email:
            return self._send_json({"error": "A valid email address is required"}, status=400)

        import hashlib
        import time
        token = hashlib.sha256(f"{email}:{time.time()}".encode()).hexdigest()[:32]
        return self._send_json({
            "status": "ok",
            "message": "Magic access link generated successfully.",
            "email": email,
            "token": token,
            "access_url": f"/studio?auth={token}&user={email}"
        })

    def _send_json(self, data: dict | list, status: int = 200):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.end_headers()
        self.wfile.write(body)

    def _handle_get_intelligence(self, parsed):
        qs = parse_qs(parsed.query)
        domain = qs.get("domain", [""])[0].strip()
        if not domain:
            return self._send_json({"error": "domain parameter required"}, status=400)

        domain = re.sub(r"[^\w.-]", "_", domain)
        clean_host = domain.replace("_", ".")
        candidates = [
            DOWNLOADED_THEMES_DIR / domain / "site-intelligence.json",
            BASE_DIR / domain / "site-intelligence.json",
            Path(tempfile.gettempdir()) / "extract_theme_output" / "downloaded-themes" / domain / "site-intelligence.json",
            Path(tempfile.gettempdir()) / "extract_theme_output" / domain / "site-intelligence.json",
        ]

        refresh = qs.get("refresh", [""])[0] in ("true", "1")
        for target in candidates:
            if not refresh and target.exists() and target.is_file():
                try:
                    data = json.loads(target.read_text(encoding="utf-8"))
                    if data.get("performance", {}).get("nextjs_performance"):
                        return self._send_json(data)
                except Exception as exc:
                    return self._send_json({"error": f"Failed to read intelligence: {exc}"}, status=500)

        # Check S3 / R2 storage for site-intelligence.json
        if storage.is_configured():
            remote_key = f"downloaded-themes/{domain}/site-intelligence.json"
            res = storage.get_file(remote_key) or storage.get_file(f"{domain}/site-intelligence.json")
            if res:
                try:
                    data = json.loads(res[0].decode("utf-8"))
                    return self._send_json(data)
                except Exception:
                    pass

        # If site-intelligence.json doesn't exist yet, check design-tokens.json
        token_candidates = [
            DOWNLOADED_THEMES_DIR / domain / "design-tokens.json",
            BASE_DIR / domain / "design-tokens.json",
            Path(tempfile.gettempdir()) / "extract_theme_output" / "downloaded-themes" / domain / "design-tokens.json",
            Path(tempfile.gettempdir()) / "extract_theme_output" / domain / "design-tokens.json",
        ]
        tokens_data = None
        target_token_path = None
        for t_target in token_candidates:
            if t_target.exists() and t_target.is_file():
                try:
                    tokens_data = json.loads(t_target.read_text(encoding="utf-8"))
                    target_token_path = t_target
                    break
                except Exception:
                    pass

        if not tokens_data and storage.is_configured():
            res = storage.get_file(f"downloaded-themes/{domain}/design-tokens.json") or storage.get_file(f"{domain}/design-tokens.json")
            if res:
                try:
                    tokens_data = json.loads(res[0].decode("utf-8"))
                except Exception:
                    pass

        html_content = ""
        css_content = ""
        if target_token_path:
            p_dir = target_token_path.parent
            guide_f = p_dir / "style-guide.html"
            if guide_f.exists():
                try:
                    html_content = guide_f.read_text(encoding="utf-8")
                except Exception:
                    pass
            comb_css = p_dir / "raw" / "combined.css"
            if comb_css.exists():
                try:
                    css_content = comb_css.read_text(encoding="utf-8", errors="replace")[:200000]
                except Exception:
                    pass

        if tokens_data:
            try:
                from analyzer import SiteAnalyzer
                primary_url = tokens_data.get("source") or f"https://{clean_host}"
                analyzer = SiteAnalyzer(
                    primary_url=primary_url,
                    pages=[(primary_url, html_content or f"<html><head><title>{clean_host}</title></head><body><h1>{clean_host}</h1></body></html>")],
                    css_text=css_content,
                    tokens=tokens_data,
                )
                report = analyzer.analyze_all()
                if target_token_path:
                    try:
                        target_token_path.parent.joinpath("site-intelligence.json").write_text(
                            json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
                        )
                    except Exception:
                        pass
                return self._send_json(report)
            except Exception as exc:
                print(f"Notice: On-the-fly intelligence generation error: {exc}")

        # Fallback: Live baseline intelligence scan so this never returns 404
        try:
            from analyzer import SiteAnalyzer
            primary_url = f"https://{clean_host}"
            try:
                import requests
                resp = requests.get(primary_url, timeout=4, headers={"User-Agent": "ExtractTheme/2.0"}, verify=False)
                if resp.status_code == 200:
                    html_content = resp.text
            except Exception:
                html_content = f"<html><head><title>{clean_host}</title></head><body><h1>{clean_host}</h1></body></html>"

            analyzer = SiteAnalyzer(
                primary_url=primary_url,
                pages=[(primary_url, html_content or "<html><body></body></html>")],
                css_text=css_content,
                tokens={"brand_name": clean_host.split(".")[0].capitalize(), "source": primary_url},
            )
            report = analyzer.analyze_all()
            return self._send_json(report)
        except Exception as dyn_err:
            print(f"Notice: Dynamic intelligence fallback failed: {dyn_err}")
            return self._send_json({"error": f"Intelligence report could not be generated for {domain}"}, status=404)

    def _handle_get_projects(self):
        projects_by_domain: dict[str, dict] = {}

        def _scan_dir(dir_path: Path):
            if not dir_path.exists() or not dir_path.is_dir():
                return
            for item in dir_path.iterdir():
                try:
                    if not item.is_dir() or item.name in {".git", "public", "__pycache__", ".agents", "api", "node_modules", "downloaded-themes"}:
                        continue
                    tokens_file = item / "design-tokens.json"
                    guide_file = item / "style-guide.html"
                    intel_file = item / "site-intelligence.json"

                    if tokens_file.exists() or guide_file.exists() or intel_file.exists():
                        meta = {}
                        if tokens_file.exists():
                            try:
                                tokens = json.loads(tokens_file.read_text(encoding="utf-8"))
                                colors_dict = tokens.get("colors", {}) if isinstance(tokens.get("colors"), dict) else {}
                                top_colors = list(colors_dict.values())[:12]

                                # Resolve semantic roles to concrete hex codes from colors_dict
                                raw_roles = tokens.get("roles", {}) if isinstance(tokens.get("roles"), dict) else {}
                                resolved_roles = {}
                                for r_name, r_ref in raw_roles.items():
                                    if isinstance(r_ref, str):
                                        resolved_roles[r_name] = colors_dict.get(r_ref, r_ref)

                                def is_chromatic(hex_or_rgb: str) -> bool:
                                    if not hex_or_rgb or not isinstance(hex_or_rgb, str):
                                        return False
                                    val = hex_or_rgb.strip().lower()
                                    if val in {"#ffffff", "#000000", "#fff", "#000"} or " 0)" in val or " 0.0)" in val:
                                        return False
                                    if val.startswith("#") and len(val) >= 7:
                                        try:
                                            r, g, b = int(val[1:3], 16), int(val[3:5], 16), int(val[5:7], 16)
                                            return (max(r, g, b) - min(r, g, b)) > 18
                                        except Exception:
                                            return True
                                    return True

                                brand_colors = []
                                for role_key in ("primary", "accent", "success", "info", "warning", "destructive"):
                                    c_val = resolved_roles.get(role_key)
                                    if c_val and is_chromatic(c_val) and c_val not in brand_colors:
                                        brand_colors.append(c_val)
                                for c_val in top_colors:
                                    if is_chromatic(c_val) and c_val not in brand_colors:
                                        brand_colors.append(c_val)
                                if not brand_colors:
                                    brand_colors = [c for c in top_colors if c and " 0)" not in c and " 0.0)" not in c]

                                fonts_val = tokens.get("fonts", {})
                                fonts_count = len([k for k in fonts_val if isinstance(k, str) and not k.startswith("_")]) if isinstance(fonts_val, (dict, list)) else 0
                                brand_name = tokens.get("brand_name") or (tokens.get("brand") or {}).get("brand_name")
                                if not brand_name:
                                    domain_parts = item.name.split(".")
                                    brand_name = domain_parts[-2].capitalize() if len(domain_parts) >= 2 and domain_parts[-2] not in {"co", "com", "org", "net", "io", "ai", "app"} else domain_parts[0].capitalize()

                                copyright_info = tokens.get("copyright") or (tokens.get("brand") or {}).get("copyright")
                                if not copyright_info:
                                    copyright_info = f"© 2026 {brand_name}. All rights reserved."

                                legal_notice = tokens.get("legal_notice") or (tokens.get("brand") or {}).get("legal_notice") or f"All trademarks, logos, and design tokens belong to {brand_name}."

                                fw_raw = tokens.get("frameworks", {})
                                if isinstance(fw_raw, dict):
                                    fw_list = list(fw_raw.keys())
                                elif isinstance(fw_raw, list):
                                    fw_list = fw_raw
                                else:
                                    fw_list = []

                                meta = {
                                    "source": tokens.get("source") or "",
                                    "generated": tokens.get("generated") or "",
                                    "brand_name": brand_name,
                                    "copyright": copyright_info,
                                    "legal_notice": legal_notice,
                                    "colors_count": len(colors_dict),
                                    "top_colors": top_colors,
                                    "brand_colors": brand_colors,
                                    "roles": resolved_roles,
                                    "fonts_count": fonts_count,
                                    "font_files_count": len(tokens.get("font_files", [])) if isinstance(tokens.get("font_files"), list) else 0,
                                    "gradients_count": len(tokens.get("gradients", [])) if isinstance(tokens.get("gradients"), list) else 0,
                                    "frameworks": fw_list,
                                    "logo": tokens.get("logo"),
                                }
                            except Exception as exc:  # noqa: BLE001
                                print(f"Error parsing tokens for {item.name}: {exc}")

                        intel_file = item / "site-intelligence.json"
                        if intel_file.exists():
                            try:
                                intel_data = json.loads(intel_file.read_text(encoding="utf-8"))
                                meta["intelligence_scores"] = intel_data.get("overview", {}).get("scores", {})
                                meta["components_count"] = len(intel_data.get("components", {}).get("detected", []))
                                meta["style_archetype"] = intel_data.get("ai_insights", {}).get("style_archetype", "Modern Web")
                            except Exception:
                                pass
                        elif "intelligence_summary" in tokens:
                            meta["intelligence_scores"] = {
                                "accessibility": tokens["intelligence_summary"].get("accessibility_score", 0),
                                "seo": tokens["intelligence_summary"].get("seo_score", 0),
                                "security_grade": tokens["intelligence_summary"].get("security_grade", "B"),
                            }
                            meta["components_count"] = tokens["intelligence_summary"].get("components_detected", 0)

                        files = [f.name for f in item.iterdir() if f.is_file()] if item.exists() else []
                        if (item / "fonts").exists():
                            files.append("fonts/")

                        projects_by_domain[item.name] = {
                            "domain": item.name,
                            "path": str(item),
                            "files": files,
                            "has_style_guide": guide_file.exists(),
                            "has_tokens": tokens_file.exists(),
                            "has_intelligence": intel_file.exists() or ("intelligence_summary" in tokens),
                            "meta": meta,
                            "source_type": "local",
                        }
                except Exception as exc:  # noqa: BLE001
                    print(f"Error reading project item {item}: {exc}")

        # 1. Scan downloaded-themes directory first, root BASE_DIR, and temporary output dirs
        try:
            _scan_dir(DOWNLOADED_THEMES_DIR)
            _scan_dir(BASE_DIR)
            tmp_output = Path(tempfile.gettempdir()) / "extract_theme_output"
            _scan_dir(tmp_output / "downloaded-themes")
            _scan_dir(tmp_output)
        except Exception as exc:  # noqa: BLE001
            print(f"Error scanning local projects: {exc}")

        # 2. Read remote projects from S3 / R2 storage if configured
        if storage.is_configured():
            try:
                remote_projects = storage.list_projects()
                for r_proj in remote_projects:
                    dom = r_proj["domain"]
                    if dom not in projects_by_domain:
                        r_proj["source_type"] = "s3"
                        projects_by_domain[dom] = r_proj
                    else:
                        # Merge files list and keep richer metadata
                        existing = projects_by_domain[dom]
                        for f in r_proj.get("files", []):
                            if f not in existing["files"]:
                                existing["files"].append(f)
                        if not existing.get("has_style_guide") and r_proj.get("has_style_guide"):
                            existing["has_style_guide"] = True
                        if not existing.get("has_tokens") and r_proj.get("has_tokens"):
                            existing["has_tokens"] = True
                        if not existing.get("meta") and r_proj.get("meta"):
                            existing["meta"] = r_proj["meta"]
            except Exception as exc:  # noqa: BLE001
                print(f"Error listing projects from S3/R2 storage: {exc}")

        projects = list(projects_by_domain.values())
        projects.sort(key=lambda p: str(p.get("meta", {}).get("generated") or ""), reverse=True)
        self._send_json({"projects": projects, "storage_configured": storage.is_configured()})

    def _handle_serve_output(self, rel_path: str):
        decoded_path = unquote(rel_path)

        candidates = [
            (DOWNLOADED_THEMES_DIR / decoded_path).resolve(),
            (BASE_DIR / decoded_path).resolve(),
            (Path(tempfile.gettempdir()) / "extract_theme_output" / "downloaded-themes" / decoded_path).resolve(),
            (Path(tempfile.gettempdir()) / "extract_theme_output" / decoded_path).resolve(),
        ]

        # Check candidate file paths
        for target in candidates:
            if target.exists() and target.is_file():
                try:
                    content = target.read_bytes()
                    content_type = get_mime_type(target.name)
                    self.send_response(200)
                    self.send_header("Content-Type", content_type)
                    self.send_header("Content-Length", str(len(content)))
                    self.send_header("Cache-Control", "public, max-age=3600")
                    self.end_headers()
                    self.wfile.write(content)
                    return
                except Exception:
                    pass

        # Check S3 / Cloudflare R2 storage
        if storage.is_configured():
            remote_file = storage.get_file(f"downloaded-themes/{decoded_path}") or storage.get_file(decoded_path)
            if remote_file:
                content, content_type = remote_file
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "public, max-age=86400")
                self.end_headers()
                self.wfile.write(content)
                return

        self.send_error(404, "File not found")

    def _handle_download_project(self, parsed):
        query_params = parse_qs(parsed.query)
        domain = query_params.get("domain", [""])[0].strip()
        if not domain:
            self.send_error(400, "Missing domain parameter")
            return

        clean_domain = re.sub(r"[^\w.-]", "_", domain)
        zip_buffer = io.BytesIO()

        # Check in downloaded-themes, root BASE_DIR, or temp dir
        candidates = [
            (DOWNLOADED_THEMES_DIR / clean_domain).resolve(),
            (BASE_DIR / clean_domain).resolve(),
            (Path(tempfile.gettempdir()) / "extract_theme_output" / "downloaded-themes" / clean_domain).resolve(),
            (Path(tempfile.gettempdir()) / "extract_theme_output" / clean_domain).resolve(),
        ]

        source_dir = None
        for cand in candidates:
            if cand.exists() and cand.is_dir():
                source_dir = cand
                break

        # If source found in root BASE_DIR, also ensure copy exists in downloaded-themes
        if source_dir and source_dir == (BASE_DIR / clean_domain).resolve():
            try:
                dt_target = DOWNLOADED_THEMES_DIR / clean_domain
                if not dt_target.exists():
                    dt_target.mkdir(parents=True, exist_ok=True)
                    for src_f in source_dir.rglob("*"):
                        if src_f.is_file():
                            rel_p = src_f.relative_to(source_dir)
                            dest_f = dt_target / rel_p
                            dest_f.parent.mkdir(parents=True, exist_ok=True)
                            dest_f.write_bytes(src_f.read_bytes())
            except Exception as copy_err:
                print(f"Notice: Could not copy theme to downloaded-themes directory: {copy_err}")

        file_count = 0
        root_zip_prefix = f"downloaded-themes/{clean_domain}"

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            if source_dir and source_dir.exists():
                for file_path in source_dir.rglob("*"):
                    if file_path.is_file():
                        rel_path = file_path.relative_to(source_dir).as_posix()
                        arcname = f"{root_zip_prefix}/{rel_path}"
                        zf.write(file_path, arcname=arcname)
                        file_count += 1
            elif storage.is_configured():
                common_files = [
                    "style-guide.html", "design-tokens.json", "theme.css",
                    "components.css", "tailwind.theme.css", "tailwind.config.js",
                    "DESIGN.md", "site-intelligence.json", "react-components.jsx"
                ]
                for fname in common_files:
                    res = storage.get_file(f"downloaded-themes/{clean_domain}/{fname}") or storage.get_file(f"{clean_domain}/{fname}")
                    if res:
                        zf.writestr(f"{root_zip_prefix}/{fname}", res[0])
                        file_count += 1

        if file_count == 0:
            self.send_error(404, f"No assets found to download for {clean_domain}")
            return

        zip_data = zip_buffer.getvalue()
        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition", f'attachment; filename="downloaded-themes-{clean_domain}.zip"')
        self.send_header("Content-Length", str(len(zip_data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(zip_data)

    def _send_chunk(self, text: str):
        chunk = text.encode("utf-8", errors="replace")
        if not chunk:
            return
        try:
            self.wfile.write(f"{len(chunk):x}\r\n".encode("ascii"))
            self.wfile.write(chunk)
            self.wfile.write(b"\r\n")
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _handle_post_extract(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            payload = json.loads(post_data.decode("utf-8"))
        except Exception:
            self._send_json({"error": "Invalid JSON body"}, status=400)
            return

        url = payload.get("url", "").strip()
        if not url:
            self._send_json({"error": "URL parameter is required"}, status=400)
            return

        if not (url.startswith("http://") or url.startswith("https://") or url.endswith(".html")):
            url = "https://" + url

        extract_script = (BASE_DIR / "extract_theme.py").resolve()
        cmd = [sys.executable, "-u", str(extract_script), url]

        # Flags mapping
        crawl = payload.get("crawl")
        if crawl:
            cmd.extend(["--crawl", str(crawl)])

        max_colors = payload.get("max_colors")
        if max_colors:
            cmd.extend(["--max-colors", str(max_colors)])

        min_count = payload.get("min_count")
        if min_count:
            cmd.extend(["--min-count", str(min_count)])

        color_tolerance = payload.get("color_tolerance")
        if color_tolerance:
            cmd.extend(["--color-tolerance", str(color_tolerance)])

        root_font_size = payload.get("root_font_size")
        if root_font_size:
            cmd.extend(["--root-font-size", str(root_font_size)])

        raw_output_dir = payload.get("output_dir", "").strip()
        if raw_output_dir:
            sanitized_dir = re.sub(r"[^\w.-]", "_", raw_output_dir).strip("._")
            output_dir = sanitized_dir if sanitized_dir else ""
        else:
            output_dir = ""

        domain = output_dir or urlparse(url).netloc or "extracted-theme"
        domain = re.sub(r"^www\.", "", domain, flags=re.I)
        domain = re.sub(r"[^\w.-]", "_", domain)

        # Output target in downloaded-themes directory
        target_dir = DOWNLOADED_THEMES_DIR / domain
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            test_file = target_dir / ".write_test"
            test_file.touch()
            test_file.unlink()
        except (OSError, PermissionError):
            target_dir = Path(tempfile.gettempdir()) / "extract_theme_output" / "downloaded-themes" / domain
            target_dir.mkdir(parents=True, exist_ok=True)

        cmd.extend(["-o", str(target_dir)])

        if payload.get("no_verify"):
            cmd.append("--insecure")

        # Send HTTP 200 with Transfer-Encoding: chunked
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Transfer-Encoding", "chunked")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        self._send_chunk(f"🚀 Initializing extraction pipeline for: {url}\n")
        self._send_chunk(f"▸ Command: {' '.join(cmd)}\n\n")

        proc_returncode = 1
        try:
            try:
                env = os.environ.copy()
                env["PYTHONIOENCODING"] = "utf-8"
                env["PYTHONUTF8"] = "1"
                env["PYTHONPATH"] = f"{BASE_DIR}{os.pathsep}{env.get('PYTHONPATH', '')}"
                proc = subprocess.Popen(
                    cmd,
                    cwd=str(BASE_DIR),
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                )

                if proc.stdout:
                    for line in iter(proc.stdout.readline, ""):
                        if not line:
                            break
                        self._send_chunk(line)

                proc.wait()
                proc_returncode = proc.returncode

            except (OSError, PermissionError) as os_err:
                # Fallback to in-process execution if subprocess execution is restricted on serverless
                self._send_chunk(f"\n⚠️ Subprocess unavailable ({os_err}). Executing in-process...\n")
                try:
                    import extract_theme

                    class StreamToChunk:
                        def __init__(self, sender):
                            self.sender = sender
                        def write(self, s):
                            if s:
                                self.sender(s)
                        def flush(self):
                            pass

                    old_stdout = sys.stdout
                    old_stderr = sys.stderr
                    sys.stdout = StreamToChunk(self._send_chunk)
                    sys.stderr = sys.stdout
                    try:
                        # Pass the arguments to extract_theme
                        run_argv = cmd[3:]
                        proc_returncode = extract_theme.main(run_argv)
                    finally:
                        sys.stdout = old_stdout
                        sys.stderr = old_stderr
                except Exception as inproc_exc:
                    self._send_chunk(f"\n❌ In-process execution error: {inproc_exc}\n")
                    proc_returncode = 1
            except Exception as exc:
                self._send_chunk(f"\n❌ EXCEPTION: {exc}\n")
                proc_returncode = 1

            host_header = self.headers.get("Host") or "localhost:8000"
            proto = "https" if self.headers.get("X-Forwarded-Proto") == "https" or "onrender.com" in host_header or "vercel.app" in host_header else "http"
            base_url = f"{proto}://{host_header}"

            if proc_returncode == 0:
                # Sync extracted theme directory to S3/R2 storage if enabled
                if storage.is_configured():
                    self._send_chunk(f"\n☁️ Syncing extracted theme to persistent S3/R2 storage ({storage.bucket})...\n")
                    count = storage.upload_theme_directory(domain, target_dir)
                    self._send_chunk(f"☁️ Uploaded {count} files to cloud storage.\n")
                else:
                    self._send_chunk(f"\n💡 Note: Object storage not configured. Saved locally to {target_dir.name}\n")

                self._send_chunk(f"\n✨ SUCCESS! Extracted design system saved for: {domain}\n")
                self._send_chunk(f"🔗 Style Guide: {base_url}/output/{domain}/style-guide.html\n")
                self._send_chunk(f"🔗 DESIGN.md:   {base_url}/output/{domain}/DESIGN.md\n")
                self._send_chunk(f"🔗 Tokens JSON: {base_url}/output/{domain}/design-tokens.json\n")
            else:
                self._send_chunk(f"\n❌ ERROR: Process exited with code {proc_returncode}\n")
        finally:
            self.wfile.write(b"0\r\n\r\n")
            try:
                self.wfile.flush()
            except Exception:
                pass


class ReusableHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="ExtractDesign Studio Server")
    parser.add_argument("-p", "--port", type=int, default=int(os.environ.get("PORT", 8000)), help="Port to listen on (default: 8000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host interface (default: 0.0.0.0)")
    args = parser.parse_args()

    port = args.port
    host = args.host
    server_address = (host, port)

    # Create directories if not exist
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOADED_THEMES_DIR.mkdir(parents=True, exist_ok=True)

    httpd = ReusableHTTPServer(server_address, ExtractThemeHandler)
    display_host = "localhost" if host == "0.0.0.0" else host
    print(f"\n=======================================================")
    print(f"  ExtractDesign Studio running at http://{display_host}:{port}/")
    print(f"  Reverse-engineer design systems & website intelligence")
    print(f"  Listening on {host}:{port}")
    print(f"=======================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
    except Exception as exc:
        print(f"\nServer error: {exc}")
    finally:
        try:
            httpd.server_close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
