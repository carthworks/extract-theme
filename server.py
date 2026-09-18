#!/usr/bin/env python3
"""
server.py — Flask API backend for ExtractDesign Studio.
Reverse-engineers design systems, UI components & website intelligence from live URLs.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import mimetypes
import os
import re
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

from flask import (
    Flask,
    Response,
    g,
    jsonify,
    request,
    send_file,
    send_from_directory,
    stream_with_context,
)
from flask_cors import CORS

import auth
import db
from storage import get_mime_type, storage

BASE_DIR = Path(__file__).parent.resolve()
PUBLIC_DIR = BASE_DIR / "public"
DOWNLOADED_THEMES_DIR = BASE_DIR / "downloaded-themes"

# Initialize Database & Run Auto-Migration
db.init_db()

# Initialize Flask application
app = Flask(
    __name__,
    static_folder=str(PUBLIC_DIR),
    static_url_path="",
)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


# =============================================================================
# Security & Cache Control Headers
# =============================================================================
@app.after_request
def add_security_headers(response: Response) -> Response:
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self' 'unsafe-inline' 'unsafe-eval' https: data: blob:; "
        "img-src 'self' https: data: blob:; font-src 'self' https: data:; "
        "style-src 'self' 'unsafe-inline' https:; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; "
        "frame-ancestors 'self';"
    )
    return response


# =============================================================================
# Frontend Pages & Static File Serving
# =============================================================================
@app.route("/")
@app.route("/landing")
@app.route("/landing.html")
def serve_landing():
    landing_file = PUBLIC_DIR / "landing.html"
    if landing_file.is_file():
        return send_from_directory(PUBLIC_DIR, "landing.html")
    return jsonify({"error": "landing.html not found"}), 404


@app.route("/studio")
@app.route("/app")
@app.route("/workbench")
@app.route("/settings")
def serve_studio():
    index_file = PUBLIC_DIR / "index.html"
    if index_file.is_file():
        return send_from_directory(PUBLIC_DIR, "index.html")
    return jsonify({"error": "index.html not found"}), 404


@app.route("/vibe-coders")
@app.route("/how-to-vibe-coders")
@app.route("/vibe-coding")
@app.route("/vibe-coders.html")
def serve_vibe_coders():
    vibe_file = PUBLIC_DIR / "vibe-coders.html"
    if vibe_file.is_file():
        return send_from_directory(PUBLIC_DIR, "vibe-coders.html")
    return jsonify({"error": "vibe-coders.html not found"}), 404




# =============================================================================
# API: Health Check
# =============================================================================
@app.route("/api/health")
@app.route("/healthz")
@app.route("/health")
@app.route("/api")
def api_health():
    return jsonify({
        "status": "ok",
        "storage_configured": storage.is_configured(),
        "service": "extract-theme",
        "framework": "Flask",
        "version": "2.2.0",
    })


# =============================================================================
# API: Magic Link Authentication (Passwordless & JWT)
# =============================================================================
@app.route("/api/auth/magic-link", methods=["POST"])
@app.route("/api/magic-link", methods=["POST"])
def api_magic_link():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    if not email or "@" not in email or "." not in email:
        return jsonify({"error": "A valid email address is required"}), 400

    user_id = f"usr_{email.replace('@', '_at_').replace('.', '_')}"
    with db.db_cursor() as cur:
        cur.execute("INSERT OR IGNORE INTO users (id, email, full_name) VALUES (?, ?, ?);",
                    (user_id, email, email.split("@")[0].capitalize()))
        # Assign to default workspace if not already assigned
        cur.execute("INSERT OR IGNORE INTO tenant_members (tenant_id, user_id, role) VALUES ('ten_default', ?, 'member');",
                    (user_id,))

    # Find first accessible tenant
    tenants = db.get_user_tenants(user_id)
    active_tenant_id = tenants[0]["id"] if tenants else "ten_default"

    token = auth.generate_token(user_id, email, active_tenant_id)
    response = jsonify({
        "status": "ok",
        "message": "Magic access link generated successfully.",
        "email": email,
        "token": token,
        "active_tenant_id": active_tenant_id,
        "access_url": f"/studio?auth={token}&user={email}",
    })
    response.set_cookie("extract_session", token, max_age=3600 * 24 * 7, httponly=True, samesite="Lax")
    return response


# =============================================================================
# API: Multi-Tenant & User Management
# =============================================================================
@app.route("/api/user/me", methods=["GET"])
@auth.require_auth
def api_user_me():
    user = g.current_user
    tenant = g.current_tenant
    role = g.tenant_role
    tenants = db.get_user_tenants(user["id"])
    if not tenants:
        tenants = [{"id": tenant["id"], "name": tenant["name"], "role": role, "plan_id": tenant.get("plan_id", "pro")}]

    plan_and_quota = db.get_tenant_plan_and_quota(tenant["id"])

    return jsonify({
        "status": "ok",
        "user": user,
        "current_tenant": tenant,
        "role": role,
        "tenants": tenants,
        "plan_and_quota": plan_and_quota,
    })


@app.route("/api/user/switch-tenant", methods=["POST"])
@auth.require_auth
def api_switch_tenant():
    data = request.get_json(silent=True) or {}
    target_tenant_id = data.get("tenant_id", "").strip()
    if not target_tenant_id:
        return jsonify({"error": "Missing tenant_id parameter"}), 400

    user_id = g.current_user["id"]
    email = g.current_user["email"]

    # Verify membership
    with db.db_cursor() as cur:
        cur.execute("SELECT role FROM tenant_members WHERE tenant_id = ? AND user_id = ?;", (target_tenant_id, user_id))
        row = cur.fetchone()
        if not row and user_id != "usr_admin":
            return jsonify({"error": "You are not a member of this workspace"}), 403

    new_token = auth.generate_token(user_id, email, target_tenant_id)
    target_tenant = db.get_tenant_by_id(target_tenant_id) or {"id": target_tenant_id, "name": "Workspace"}

    response = jsonify({
        "status": "ok",
        "token": new_token,
        "active_tenant": target_tenant,
        "message": f"Switched to workspace '{target_tenant.get('name')}'",
    })
    response.set_cookie("extract_session", new_token, max_age=3600 * 24 * 7, httponly=True, samesite="Lax")
    return response


@app.route("/api/tenants", methods=["POST"])
@auth.require_auth
def api_create_tenant():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify({"error": "Workspace name is required"}), 400

    new_t = db.create_new_tenant(name=name, owner_user_id=g.current_user["id"], plan_id="free")
    new_token = auth.generate_token(g.current_user["id"], g.current_user["email"], new_t["id"])

    response = jsonify({
        "status": "ok",
        "tenant": new_t,
        "token": new_token,
        "message": f"Workspace '{name}' created successfully.",
    })
    response.set_cookie("extract_session", new_token, max_age=3600 * 24 * 7, httponly=True, samesite="Lax")
    return response


@app.route("/api/tenants/<tenant_id>/members", methods=["GET"])
@auth.require_auth
def api_tenant_members(tenant_id: str):
    members = db.get_tenant_members(tenant_id)
    return jsonify({
        "status": "ok",
        "members": members,
    })


@app.route("/api/tenants/<tenant_id>/invites", methods=["POST"])
@auth.require_role("admin")
def api_tenant_invite(tenant_id: str):
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    role = str(data.get("role", "member")).lower()
    if not email or "@" not in email:
        return jsonify({"error": "A valid email address is required"}), 400
    if role not in ("admin", "member", "viewer"):
        role = "member"

    res = db.add_or_invite_member(tenant_id, email, role=role)
    return jsonify({
        "status": "ok",
        "message": f"Invited {email} as {role}.",
        "member": res,
    })


@app.route("/api/tenants/<tenant_id>/members/<user_id>", methods=["DELETE"])
@auth.require_role("admin")
def api_remove_member(tenant_id: str, user_id: str):
    ok = db.remove_tenant_member(tenant_id, user_id)
    if not ok:
        return jsonify({"error": "Cannot remove member or member is workspace owner"}), 400
    return jsonify({"status": "ok", "message": "Member removed."})


# =============================================================================
# API: Workspace & Platform Settings
# =============================================================================
SETTINGS_FILE = BASE_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "brand": {
        "name": "ExtractDesign Studio",
        "tagline": "Reverse-engineer design systems & website intelligence",
        "accent_color": "#6366f1",
        "logo_url": "",
        "custom_domain": "design-intel.local",
    },
    "whitelabel": {
        "agency_name": "Apex Digital Studio",
        "agency_url": "https://apexdigital.design",
        "footer_signature": "Design Intelligence Audit prepared by Apex Digital Studio",
        "hide_powered_by": False,
        "default_print_auto": False,
    },
    "plan": {
        "id": "pro",
        "name": "Pro Agency Plan",
        "price_label": "₹999/mo (~$12/mo)",
        "status": "Active",
        "billing_cycle": "Monthly",
        "expiry_date": "2026-10-18T00:00:00Z",
        "days_remaining": 30,
        "scans_used": 14,
        "scans_limit": "Unlimited",
        "crawls_used": 4,
        "crawls_limit": 20,
        "storage_used_mb": 182,
        "storage_limit_mb": 10240,
    },
    "engine": {
        "default_crawl_depth": 5,
        "request_timeout_seconds": 30,
        "download_fonts": True,
        "user_agent_preset": "desktop_chrome",
        "skip_tls_verify": False,
        "preferred_export_format": "tailwind",
    },
    "api": {
        "api_key": "sk_live_extract_99f82d114ba742e88a09b",
        "webhook_url": "",
    },
}


def load_settings() -> dict:
    if SETTINGS_FILE.is_file():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                user_settings = json.load(f)
                merged = json.loads(json.dumps(DEFAULT_SETTINGS))
                for section, vals in user_settings.items():
                    if isinstance(vals, dict) and section in merged and isinstance(merged[section], dict):
                        merged[section].update(vals)
                    else:
                        merged[section] = vals
                return merged
        except Exception as e:
            print(f"[Settings] Error loading settings: {e}")
    return json.loads(json.dumps(DEFAULT_SETTINGS))


def save_settings(new_settings: dict) -> dict:
    try:
        current = load_settings()
        for section, vals in new_settings.items():
            if isinstance(vals, dict) and section in current and isinstance(current[section], dict):
                current[section].update(vals)
            else:
                current[section] = vals
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2)
        return current
    except Exception as e:
        print(f"[Settings] Error saving settings: {e}")
        return current


@app.route("/api/settings", methods=["GET"])
def api_get_settings():
    return jsonify({
        "status": "ok",
        "settings": load_settings(),
    })


@app.route("/api/settings", methods=["POST", "PUT"])
def api_update_settings():
    data = request.get_json(silent=True) or {}
    updated = save_settings(data)
    return jsonify({
        "status": "ok",
        "message": "Settings saved successfully",
        "settings": updated,
    })


@app.route("/api/settings/reset", methods=["POST"])
def api_reset_settings():
    if SETTINGS_FILE.is_file():
        try:
            SETTINGS_FILE.unlink()
        except Exception:
            pass
    return jsonify({
        "status": "ok",
        "message": "Settings reset to defaults",
        "settings": DEFAULT_SETTINGS,
    })


# =============================================================================
# API: Projects Listing (Multi-Tenant Scoped)
# =============================================================================
@app.route("/api/projects", methods=["GET"])
@auth.require_auth
def api_projects():
    tenant_id = g.current_tenant.get("id", "ten_default")
    projects_by_domain: dict[str, dict] = {}

    def _scan_dir(dir_path: Path):
        if not dir_path.exists() or not dir_path.is_dir():
            return
        for item in dir_path.iterdir():
            try:
                if not item.is_dir() or item.name in {
                    ".git", "public", "__pycache__", ".agents", "api", "node_modules", "downloaded-themes", "tenants"
                }:
                    continue

                guide_file = item / "style-guide.html"
                tokens_file = item / "design-tokens.json"
                intel_file = item / "site-intelligence.json"

                if guide_file.exists() or tokens_file.exists() or intel_file.exists():
                    meta: dict = {}
                    tokens: dict = {}
                    if tokens_file.exists():
                        try:
                            tokens = json.loads(tokens_file.read_text(encoding="utf-8"))
                            meta = tokens.get("_meta", {}) if isinstance(tokens.get("_meta"), dict) else {}
                        except Exception:
                            pass

                    # Determine accurate timestamp & modification date
                    mtime = 0.0
                    for f_stat in (tokens_file, guide_file, intel_file, item):
                        if f_stat.exists():
                            try:
                                mtime = max(mtime, f_stat.stat().st_mtime)
                            except Exception:
                                pass

                    gen_time = tokens.get("generated") or meta.get("generated")
                    if not gen_time and mtime > 0:
                        import datetime
                        gen_time = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%dT%H:%M:%S")

                    meta["generated"] = gen_time
                    meta["timestamp"] = mtime

                    # Extract richer metadata from tokens if available
                    if tokens:
                        meta["colors_count"] = len(tokens.get("colors", {}))
                        meta["fonts_count"] = len([k for k in tokens.get("fonts", {}) if not k.startswith("_")])
                        meta["font_files_count"] = len(tokens.get("font_files", []))
                        meta["gradients_count"] = len(tokens.get("gradients", []))
                        meta["copyright"] = tokens.get("copyright")
                        fw_raw = tokens.get("frameworks", [])
                        if isinstance(fw_raw, dict):
                            meta["frameworks"] = list(fw_raw.keys())
                        elif isinstance(fw_raw, list):
                            meta["frameworks"] = fw_raw
                        elif isinstance(fw_raw, str):
                            meta["frameworks"] = [fw_raw] if fw_raw else []
                        else:
                            meta["frameworks"] = []

                        # Extract authentic colors, brand palette & roles
                        colors_dict = tokens.get("colors", {})
                        raw_colors = []
                        if isinstance(colors_dict, dict):
                            raw_colors = [str(c) for c in colors_dict.values() if isinstance(c, str) and c.startswith("#")]
                        elif isinstance(colors_dict, list):
                            raw_colors = [str(c) for c in colors_dict if isinstance(c, str) and c.startswith("#")]

                        unique_colors = list(dict.fromkeys(raw_colors))

                        # Detect vibrant/chromatic colors
                        def _is_vibrant(hex_str: str) -> bool:
                            h = hex_str.lstrip("#")
                            if len(h) == 6:
                                try:
                                    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
                                    diff = max(abs(r - g), abs(r - b), abs(g - b))
                                    lum = 0.299 * r + 0.587 * g + 0.114 * b
                                    return diff > 25 and 30 < lum < 225
                                except Exception:
                                    return False
                            return False

                        brand_candidates = [c for c in unique_colors if _is_vibrant(c)]
                        if not brand_candidates:
                            brand_candidates = unique_colors[:5]

                        meta["brand_colors"] = brand_candidates[:4]
                        meta["top_colors"] = unique_colors[:8]

                        # Semantic roles mapping
                        meta["roles"] = {
                            "primary": brand_candidates[0] if brand_candidates else "#6366f1",
                            "secondary": brand_candidates[1] if len(brand_candidates) > 1 else (brand_candidates[0] if brand_candidates else "#06b6d4"),
                            "surface": next((c for c in unique_colors if c.lower() in ("#ffffff", "#000000", "#0f172a", "#18181b", "#111827", "#f8fafc", "#f9fafb")), "#0f172a"),
                        }

                    # Attach site intelligence details
                    if intel_file.exists():
                        try:
                            intel_data = json.loads(intel_file.read_text(encoding="utf-8"))
                            meta["intelligence"] = intel_data
                            metadata = intel_data.get("metadata", {})
                            if "style_archetype" in metadata:
                                meta["style_archetype"] = metadata["style_archetype"]
                            if "brand_name" in metadata and not meta.get("brand_name"):
                                meta["brand_name"] = metadata["brand_name"]
                            if "logo_type" in metadata:
                                meta["logo_type"] = metadata["logo_type"]
                            if "typography" in metadata:
                                meta["typography_primary"] = metadata["typography"].get("primary_font")
                            if "intelligence_scores" in metadata:
                                meta["intelligence_scores"] = metadata["intelligence_scores"]
                            if "components_count" in metadata:
                                meta["components_count"] = metadata["components_count"]
                        except Exception:
                            pass

                    if "intelligence_summary" in tokens:
                        meta["intelligence_scores"] = {
                            "accessibility": tokens["intelligence_summary"].get("accessibility_score", 0),
                            "seo": tokens["intelligence_summary"].get("seo_score", 0),
                            "security_grade": tokens["intelligence_summary"].get("security_grade", "B"),
                        }
                        meta["components_count"] = tokens["intelligence_summary"].get("components_detected", 0)

                    meta.setdefault("colors_count", 0)
                    meta.setdefault("fonts_count", 0)
                    meta.setdefault("font_files_count", 0)
                    meta.setdefault("gradients_count", 0)
                    meta.setdefault("frameworks", [])

                    if not meta.get("brand_colors"):
                        import colorsys
                        dom_seed = item.name
                        d_hash = int(hashlib.md5(dom_seed.encode()).hexdigest(), 16)
                        def _hsl_hex(h, s=0.74, l=0.52):
                            r, g, b = colorsys.hls_to_rgb((h % 360) / 360.0, l, s)
                            return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
                        h0 = d_hash % 360
                        h1 = (h0 + 45) % 360
                        h2 = (h0 + 175) % 360
                        h3 = (h0 + 220) % 360
                        gen_palette = [_hsl_hex(h0), _hsl_hex(h1), _hsl_hex(h2), _hsl_hex(h3)]
                        meta["brand_colors"] = gen_palette
                        meta["top_colors"] = gen_palette

                    if intel_file.exists() and not meta["frameworks"]:
                        try:
                            intel_data = json.loads(intel_file.read_text(encoding="utf-8"))
                            tech = intel_data.get("technology", {})
                            by_cat = tech.get("by_category", {})
                            fw_from_intel = by_cat.get("Frameworks", [])
                            if fw_from_intel:
                                meta["frameworks"] = fw_from_intel
                        except Exception:
                            pass

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
                    }
            except Exception as exc:
                print(f"Error reading local project folder {item.name}: {exc}")

    # 1. Scan local directories (Tenant-partitioned + root fallback)
    try:
        tenant_dir = DOWNLOADED_THEMES_DIR / "tenants" / tenant_id
        if tenant_dir.is_dir():
            _scan_dir(tenant_dir)

        # In primary workspace or if tenant folder is empty, scan main downloaded-themes
        if tenant_id == "ten_default" or not projects_by_domain:
            _scan_dir(DOWNLOADED_THEMES_DIR)
            _scan_dir(BASE_DIR)
            temp_output = Path(tempfile.gettempdir()) / "extract_theme_output" / "downloaded-themes"
            if temp_output.is_dir():
                _scan_dir(temp_output)
    except Exception as exc:
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
        except Exception as exc:
            print(f"Error listing projects from S3/R2 storage: {exc}")

    projects = list(projects_by_domain.values())
    def _project_sort_key(p):
        meta = p.get("meta", {})
        ts = meta.get("timestamp") or 0.0
        if not ts and meta.get("generated"):
            try:
                import datetime
                ts = datetime.datetime.fromisoformat(str(meta.get("generated")).replace("Z", "+00:00")).timestamp()
            except Exception:
                ts = 0.0
        return (ts, str(meta.get("generated") or ""))

    projects.sort(key=_project_sort_key, reverse=True)
    plan_info = db.get_tenant_plan_and_quota(tenant_id)
    return jsonify({
        "status": "ok",
        "tenant": plan_info,
        "role": g.tenant_role,
        "projects": projects,
        "storage_configured": storage.is_configured(),
    })


# =============================================================================
# API: Intelligence Report
# =============================================================================
@app.route("/api/intelligence", methods=["GET"])
def api_intelligence():
    domain = request.args.get("domain", "").strip()
    if not domain:
        return jsonify({"error": "domain parameter required"}), 400

    domain = re.sub(r"[^\w.-]", "_", domain)
    clean_host = domain.replace("_", ".")
    candidates = [
        DOWNLOADED_THEMES_DIR / domain / "site-intelligence.json",
        BASE_DIR / domain / "site-intelligence.json",
        Path(tempfile.gettempdir()) / "extract_theme_output" / "downloaded-themes" / domain / "site-intelligence.json",
        Path(tempfile.gettempdir()) / "extract_theme_output" / domain / "site-intelligence.json",
    ]

    refresh = request.args.get("refresh", "").lower() in ("true", "1")
    for target in candidates:
        if not refresh and target.exists() and target.is_file():
            try:
                data = json.loads(target.read_text(encoding="utf-8"))
                return jsonify(data)
            except Exception as exc:
                return jsonify({"error": f"Failed to read intelligence: {exc}"}), 500

    # Check S3 / R2 storage for site-intelligence.json
    if storage.is_configured():
        remote_key = f"downloaded-themes/{domain}/site-intelligence.json"
        res = storage.get_file(remote_key) or storage.get_file(f"{domain}/site-intelligence.json")
        if res:
            try:
                data = json.loads(res[0].decode("utf-8"))
                return jsonify(data)
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
            return jsonify(report)
        except Exception as exc:
            print(f"Notice: On-the-fly intelligence generation error: {exc}")

    # Fallback: Live baseline intelligence scan
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
        return jsonify(report)
    except Exception as dyn_err:
        print(f"Notice: Dynamic intelligence fallback failed: {dyn_err}")
        return jsonify({"error": f"Intelligence report could not be generated for {domain}"}), 404


# =============================================================================
# API: Serve Output Files
# =============================================================================
@app.route("/output/<path:filepath>", methods=["GET"])
def api_output(filepath: str):
    candidates = [
        (DOWNLOADED_THEMES_DIR / filepath).resolve(),
        (BASE_DIR / filepath).resolve(),
        (Path(tempfile.gettempdir()) / "extract_theme_output" / "downloaded-themes" / filepath).resolve(),
        (Path(tempfile.gettempdir()) / "extract_theme_output" / filepath).resolve(),
    ]

    for target in candidates:
        if target.is_file():
            content_type = get_mime_type(target.name)
            return send_file(target, mimetype=content_type)

    if storage.is_configured():
        remote_file = storage.get_file(f"downloaded-themes/{filepath}") or storage.get_file(filepath)
        if remote_file:
            content, content_type = remote_file
            return Response(content, mimetype=content_type)

    return jsonify({"error": "File not found"}), 404


# =============================================================================
# API: Download ZIP Archive
# =============================================================================
@app.route("/api/download", methods=["GET"])
def api_download():
    domain = request.args.get("domain", "").strip()
    if not domain:
        return jsonify({"error": "Missing domain parameter"}), 400

    clean_domain = re.sub(r"[^\w.-]", "_", domain)
    zip_buffer = io.BytesIO()

    candidates = [
        (DOWNLOADED_THEMES_DIR / clean_domain).resolve(),
        (BASE_DIR / clean_domain).resolve(),
        (Path(tempfile.gettempdir()) / "extract_theme_output" / "downloaded-themes" / clean_domain).resolve(),
        (Path(tempfile.gettempdir()) / "extract_theme_output" / clean_domain).resolve(),
    ]

    source_dir = None
    for cand in candidates:
        if cand.is_dir():
            source_dir = cand
            break

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
                "DESIGN.md", "site-intelligence.json", "react-components.jsx",
                "theme.ts", "tokens.w3c.json", "useTokens.ts"
            ]
            for fname in common_files:
                res = storage.get_file(f"downloaded-themes/{clean_domain}/{fname}") or storage.get_file(f"{clean_domain}/{fname}")
                if res:
                    zf.writestr(f"{root_zip_prefix}/{fname}", res[0])
                    file_count += 1

    if file_count == 0:
        return jsonify({"error": f"No assets found to download for {clean_domain}"}), 404

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"downloaded-themes-{clean_domain}.zip",
    )


# =============================================================================
# API: Extraction Pipeline (Streaming Execution)
# =============================================================================
@app.route("/api/extract", methods=["GET", "POST"])
@auth.require_auth
def api_extract():
    if request.method == "GET":
        url_param = request.args.get("url", "").strip()
        if not url_param:
            return jsonify({
                "status": "ready",
                "endpoint": "/api/extract",
                "method": "POST",
                "description": "Extract design tokens, styles, components, and website intelligence from any website URL.",
                "usage": {
                    "method": "POST",
                    "headers": {"Content-Type": "application/json"},
                    "body": {
                        "url": "https://example.com",
                        "crawl": 0,
                        "max_colors": 48,
                    },
                },
            })
        payload = {
            "url": url_param,
            "crawl": int(request.args.get("crawl", 0)),
            "max_colors": int(request.args.get("max_colors", 48)),
            "min_count": int(request.args.get("min_count", 1)),
            "color_tolerance": float(request.args.get("color_tolerance", 0.02)),
            "root_font_size": float(request.args.get("root_font_size", 16.0)),
            "output_dir": request.args.get("output_dir", ""),
            "no_verify": request.args.get("no_verify", "") in ("true", "1"),
        }
    else:
        payload = request.get_json(silent=True) or {}

    url = payload.get("url", "").strip()
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    # Quota and feature gate check
    crawl_val = int(payload.get("crawl") or 0)
    gate_err = auth.check_quota_and_gates("scan", crawl_depth=crawl_val)
    if gate_err:
        return jsonify(gate_err), 403

    if not (url.startswith("http://") or url.startswith("https://") or url.endswith(".html")):
        url = "https://" + url

    extract_script = (BASE_DIR / "extract_theme.py").resolve()
    cmd = [sys.executable, "-u", str(extract_script), url]

    if payload.get("crawl"):
        cmd.extend(["--crawl", str(payload["crawl"])])
    if payload.get("max_colors"):
        cmd.extend(["--max-colors", str(payload["max_colors"])])
    if payload.get("min_count"):
        cmd.extend(["--min-count", str(payload["min_count"])])
    if payload.get("color_tolerance"):
        cmd.extend(["--color-tolerance", str(payload["color_tolerance"])])
    if payload.get("root_font_size"):
        cmd.extend(["--root-font-size", str(payload["root_font_size"])])

    raw_output_dir = payload.get("output_dir", "").strip()
    if raw_output_dir:
        sanitized_dir = re.sub(r"[^\w.-]", "_", raw_output_dir).strip("._")
        output_dir = sanitized_dir if sanitized_dir else ""
    else:
        output_dir = ""

    from urllib.parse import urlparse
    domain = output_dir or urlparse(url).netloc or "extracted-theme"
    domain = re.sub(r"^www\.", "", domain, flags=re.I)
    domain = re.sub(r"[^\w.-]", "_", domain)

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

    def generate():
        yield f"🚀 Initializing extraction pipeline for: {url}\n"
        yield f"▸ Command: {' '.join(cmd)}\n\n"

        proc_returncode = 1
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
                    yield line

            proc.wait()
            proc_returncode = proc.returncode

        except (OSError, PermissionError) as os_err:
            yield f"\n⚠️ Subprocess unavailable ({os_err}). Executing in-process...\n"
            try:
                import extract_theme

                class StreamCapture:
                    def __init__(self):
                        self._buffer = []
                    def write(self, s):
                        if s:
                            self._buffer.append(s)
                    def flush(self):
                        pass

                stream_cap = StreamCapture()
                old_stdout, old_stderr = sys.stdout, sys.stderr
                sys.stdout = stream_cap
                sys.stderr = stream_cap
                try:
                    run_argv = cmd[3:]
                    proc_returncode = extract_theme.main(run_argv)
                finally:
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr
                    for b in stream_cap._buffer:
                        yield b
            except Exception as inproc_exc:
                yield f"\n❌ In-process execution error: {inproc_exc}\n"
                proc_returncode = 1
        except Exception as exc:
            yield f"\n❌ EXCEPTION: {exc}\n"
            proc_returncode = 1

        host_header = request.headers.get("Host") or "localhost:8000"
        proto = "https" if request.headers.get("X-Forwarded-Proto") == "https" or "onrender.com" in host_header or "vercel.app" in host_header else "http"
        base_url = f"{proto}://{host_header}"

        if proc_returncode == 0:
            try:
                tenant_id = auth.get_current_tenant_id()
                crawl_cnt = int(payload.get("crawl") or 0)
                db.increment_tenant_scan(tenant_id, is_crawl=(crawl_cnt > 1), depth=crawl_cnt)
                db.register_tenant_project(
                    tenant_id=tenant_id,
                    domain=domain,
                    storage_path=f"downloaded-themes/{domain}",
                    user_id=g.current_user.get("id") if hasattr(g, "current_user") else "usr_admin",
                    crawl_depth=crawl_cnt,
                )
            except Exception as reg_exc:
                print(f"[DB] Warning: Failed to record tenant scan in db: {reg_exc}")

            if storage.is_configured():
                yield f"\n☁️ Syncing extracted theme to persistent S3/R2 storage ({storage.bucket})...\n"
                count = storage.upload_theme_directory(domain, target_dir)
                yield f"☁️ Uploaded {count} files to cloud storage.\n"
            else:
                yield f"\n💡 Note: Object storage not configured. Saved locally to {target_dir.name}\n"

            yield f"\n✨ SUCCESS! Extracted design system saved for: {domain}\n"
            yield f"🔗 Style Guide: {base_url}/output/{domain}/style-guide.html\n"
            yield f"🔗 DESIGN.md:   {base_url}/output/{domain}/DESIGN.md\n"
            yield f"🔗 Tokens JSON: {base_url}/output/{domain}/design-tokens.json\n"
        else:
            yield f"\n❌ ERROR: Extraction pipeline terminated (code {proc_returncode}).\n"
            yield "💡 Diagnostic Tips:\n"
            yield "   1. Verify the target website is publicly reachable in your browser.\n"
            yield "   2. If the site has strict anti-bot / Cloudflare mitigation, save the page as HTML and run extract on the local file.\n"
            yield "   3. If SSL/TLS certificate verification fails, toggle the 'Skip TLS Verify' option.\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/plain; charset=utf-8",
        headers={"X-Content-Type-Options": "nosniff"},
    )



@app.route("/<path:filename>")
def serve_static(filename: str):
    if filename.startswith("api/") or filename == "api":
        return jsonify({"error": f"API endpoint '/{filename}' not found"}), 404

    # 1. Exact file match
    target = (PUBLIC_DIR / filename).resolve()
    if target.is_file() and str(target).startswith(str(PUBLIC_DIR.resolve())):
        return send_from_directory(PUBLIC_DIR, filename)

    # 2. Clean URL fallback (e.g. /vibe-coders -> /vibe-coders.html)
    html_target = (PUBLIC_DIR / f"{filename}.html").resolve()
    if html_target.is_file() and str(html_target).startswith(str(PUBLIC_DIR.resolve())):
        return send_from_directory(PUBLIC_DIR, f"{filename}.html")

    return jsonify({"error": "File not found"}), 404



# =============================================================================
# CLI Entry Point
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="ExtractDesign Studio Flask Server")
    parser.add_argument("-p", "--port", type=int, default=int(os.environ.get("PORT", 8000)), help="Port to listen on (default: 8000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host interface (default: 0.0.0.0)")
    parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")
    args = parser.parse_args()

    port = args.port
    host = args.host

    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOADED_THEMES_DIR.mkdir(parents=True, exist_ok=True)

    display_host = "localhost" if host == "0.0.0.0" else host
    print("\n=======================================================")
    print(f"  ExtractDesign Studio running at http://{display_host}:{port}/")
    print(f"  Framework: Flask (RESTful & Streaming API)")
    print(f"  Reverse-engineer design systems & website intelligence")
    print(f"  Listening on {host}:{port}")
    print("=======================================================\n")

    app.run(host=host, port=port, debug=args.debug, threaded=True)


if __name__ == "__main__":
    main()
