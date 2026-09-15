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
import tempfile
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from storage import get_mime_type, storage

BASE_DIR = Path(__file__).parent.resolve()
PUBLIC_DIR = BASE_DIR / "public"



class ExtractThemeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path in ("/api/health", "/healthz", "/health"):
            return self._send_json({
                "status": "ok",
                "storage_configured": storage.is_configured(),
                "service": "extract-theme"
            })

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
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.end_headers()
        self.wfile.write(body)

    def _handle_get_projects(self):
        projects_by_domain: dict[str, dict] = {}

        # 1. Read local projects from BASE_DIR
        try:
            for item in BASE_DIR.iterdir():
                try:
                    if not item.is_dir() or item.name in {".git", "public", "__pycache__", ".agents", "api"}:
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
                                    "source": tokens.get("source") or "",
                                    "generated": tokens.get("generated") or "",
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

                        files = [f.name for f in item.iterdir() if f.is_file()] if item.exists() else []
                        if (item / "fonts").exists():
                            files.append("fonts/")

                        projects_by_domain[item.name] = {
                            "domain": item.name,
                            "path": str(item),
                            "files": files,
                            "has_style_guide": guide_file.exists(),
                            "has_tokens": tokens_file.exists(),
                            "meta": meta,
                            "source_type": "local",
                        }
                except Exception as exc:  # noqa: BLE001
                    print(f"Error reading local project item {item}: {exc}")
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
        target = (BASE_DIR / decoded_path).resolve()

        # 1. Check if local file exists in BASE_DIR
        if target.exists() and target.is_file():
            try:
                target.relative_to(BASE_DIR)
                content = target.read_bytes()
                content_type = get_mime_type(target.name)
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "public, max-age=3600")
                self.end_headers()
                self.wfile.write(content)
                return
            except ValueError:
                self.send_error(403, "Access denied")
                return

        # 2. Check if file exists in temp directory (serverless fallback)
        temp_target = (Path(tempfile.gettempdir()) / "extract_theme_output" / decoded_path).resolve()
        if temp_target.exists() and temp_target.is_file():
            content = temp_target.read_bytes()
            content_type = get_mime_type(temp_target.name)
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "public, max-age=3600")
            self.end_headers()
            self.wfile.write(content)
            return

        # 3. If not found locally, check S3 / Cloudflare R2 storage
        if storage.is_configured():
            remote_file = storage.get_file(decoded_path)
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

        raw_output_dir = payload.get("output_dir", "").strip()
        if raw_output_dir:
            # Strictly sanitize output_dir to prevent path traversal
            sanitized_dir = re.sub(r"[^\w.-]", "_", raw_output_dir).strip("._")
            output_dir = sanitized_dir if sanitized_dir else ""
        else:
            output_dir = ""

        domain = output_dir or urlparse(url).netloc or "extracted-theme"
        domain = re.sub(r"^www\.", "", domain, flags=re.I)
        domain = re.sub(r"[^\w.-]", "_", domain)

        # Check if BASE_DIR is writable or read-only (serverless)
        target_dir = BASE_DIR / domain
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            test_file = target_dir / ".write_test"
            test_file.touch()
            test_file.unlink()
        except (OSError, PermissionError):
            target_dir = Path(tempfile.gettempdir()) / "extract_theme_output" / domain
            target_dir.mkdir(parents=True, exist_ok=True)

        cmd.extend(["-o", str(target_dir)])

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

            host_header = self.headers.get("Host") or "localhost:8000"
            proto = "https" if self.headers.get("X-Forwarded-Proto") == "https" or "onrender.com" in host_header or "vercel.app" in host_header else "http"
            base_url = f"{proto}://{host_header}"

            if proc.returncode == 0:
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
    server_address = ("0.0.0.0", port)

    # Create public directory if not exists
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    httpd = HTTPServer(server_address, ExtractThemeHandler)
    print(f"\n=======================================================")
    print(f"  ExtractTheme Studio running on port {port} (0.0.0.0)")
    print(f"=======================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()


if __name__ == "__main__":
    main()
