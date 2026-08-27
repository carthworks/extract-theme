#!/usr/bin/env python3
"""
extract-theme web server — hostable web UI backend for design system extraction.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

BASE_DIR = Path(__file__).parent.resolve()
PUBLIC_DIR = BASE_DIR / "public"


class ExtractThemeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/projects":
            return self._handle_get_projects()

        if parsed.path.startswith("/output/"):
            return self._handle_serve_output(parsed.path[8:])

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/extract":
            return self._handle_post_extract()

        self.send_error(404, "Endpoint not found")

    def _send_json(self, data: dict | list, status: int = 200):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_get_projects(self):
        projects = []
        for item in BASE_DIR.iterdir():
            if not item.is_dir() or item.name in {".git", "public", "__pycache__", ".agents"}:
                continue
            tokens_file = item / "design-tokens.json"
            guide_file = item / "style-guide.html"

            if tokens_file.exists() or guide_file.exists():
                meta = {}
                if tokens_file.exists():
                    try:
                        tokens = json.loads(tokens_file.read_text(encoding="utf-8"))
                        colors_dict = tokens.get("colors", {}) if isinstance(tokens.get("colors"), dict) else {}
                        top_colors = list(colors_dict.values())[:10]
                        fonts_val = tokens.get("fonts", {})
                        fonts_count = len([k for k in fonts_val if isinstance(k, str) and not k.startswith("_")]) if isinstance(fonts_val, (dict, list)) else 0
                        fw = tokens.get("frameworks", {})
                        fw_list = list(fw.keys()) if isinstance(fw, dict) else (fw if isinstance(fw, list) else [])
                        meta = {
                            "source": tokens.get("source"),
                            "generated": tokens.get("generated"),
                            "colors_count": len(colors_dict),
                            "top_colors": top_colors,
                            "roles": tokens.get("roles", {}) if isinstance(tokens.get("roles"), dict) else {},
                            "fonts_count": fonts_count,
                            "font_files_count": len(tokens.get("font_files", [])) if isinstance(tokens.get("font_files"), list) else 0,
                            "gradients_count": len(tokens.get("gradients", [])) if isinstance(tokens.get("gradients"), list) else 0,
                            "frameworks": fw_list,
                            "logo": tokens.get("logo"),
                        }
                    except Exception as exc:  # noqa: BLE001
                        print(f"Error parsing tokens for {item.name}: {exc}")

                files = [f.name for f in item.iterdir() if f.is_file()]
                if (item / "fonts").exists():
                    files.append("fonts/")

                projects.append({
                    "domain": item.name,
                    "path": str(item),
                    "files": files,
                    "has_style_guide": guide_file.exists(),
                    "has_tokens": tokens_file.exists(),
                    "meta": meta,
                })

        projects.sort(key=lambda p: p.get("meta", {}).get("generated", ""), reverse=True)
        self._send_json({"projects": projects})

    def _handle_serve_output(self, rel_path: str):
        target = (BASE_DIR / unquote(rel_path)).resolve()
        # Security check: must be inside BASE_DIR
        try:
            target.relative_to(BASE_DIR)
        except ValueError:
            self.send_error(403, "Access denied")
            return

        if not target.exists() or not target.is_file():
            self.send_error(404, "File not found")
            return

        ext = target.suffix.lower()
        mime_types = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".woff2": "font/woff2",
            ".woff": "font/woff",
            ".ttf": "font/ttf",
        }
        content_type = mime_types.get(ext, "application/octet-stream")

        content = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

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

        cmd = [sys.executable, "-u", "extract_theme.py", url]

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

        output_dir = payload.get("output_dir", "").strip()
        if output_dir:
            cmd.extend(["-o", output_dir])

        if payload.get("no_verify"):
            cmd.append("--no-verify")

        # Send HTTP 200 with Transfer-Encoding: chunked
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Transfer-Encoding", "chunked")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        self._send_chunk(f"🚀 Initializing extraction pipeline for: {url}\n")
        self._send_chunk(f"▸ Command: {' '.join(cmd)}\n\n")

        try:
            proc = subprocess.Popen(
                cmd,
                cwd=str(BASE_DIR),
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

            domain = output_dir or urlparse(url).netloc or "extracted-theme"
            domain = re.sub(r"^www\.", "", domain, flags=re.I)
            domain = re.sub(r"[^\w.-]", "_", domain)

            if proc.returncode == 0:
                self._send_chunk(f"\n✨ SUCCESS! Extracted design system saved to: {domain}\n")
            else:
                self._send_chunk(f"\n❌ ERROR: Process exited with code {proc.returncode}\n")

        except Exception as exc:
            self._send_chunk(f"\n❌ EXCEPTION: {exc}\n")
        finally:
            self.wfile.write(b"0\r\n\r\n")
            try:
                self.wfile.flush()
            except Exception:
                pass


def main():
    port = int(os.environ.get("PORT", 8000))
    server_address = ("", port)

    # Create public directory if not exists
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    httpd = HTTPServer(server_address, ExtractThemeHandler)
    print(f"\n=======================================================")
    print(f"  Theme Extractor Web UI running on http://localhost:{port}")
    print(f"=======================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()


if __name__ == "__main__":
    main()
