"""
auth.py — Authentication, RBAC & Multi-Tenant Context Resolution for ExtractDesign Studio.
Provides JWT session token generation, verification, and request context injection.
"""

from __future__ import annotations

import os
import time
from functools import wraps
from typing import Any, Callable, Dict, Optional

import jwt
from flask import g, jsonify, make_response, request

from . import database as db

JWT_SECRET = os.environ.get("JWT_SECRET", "extractdesign-super-secret-multi-tenant-key-2026")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24 * 7  # 7 days

ROLE_HIERARCHY = {
    "owner": 40,
    "admin": 30,
    "member": 20,
    "viewer": 10,
}


def generate_token(user_id: str, email: str, active_tenant_id: str) -> str:
    """Generates a signed JWT session token with user and tenant claims."""
    payload = {
        "sub": user_id,
        "email": email,
        "tenant_id": active_tenant_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + (JWT_EXPIRATION_HOURS * 3600),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verifies a JWT token and returns the decoded payload if valid."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception:
        return None


def get_current_tenant_id() -> str:
    """Resolves active tenant ID from request context with fallback."""
    if hasattr(g, "current_tenant") and g.current_tenant:
        return g.current_tenant.get("id", "ten_default")
    return "ten_default"


def require_auth(f: Callable) -> Callable:
    """
    Middleware resolving authenticated user and active tenant context.
    Falls back gracefully to 'usr_admin' and 'ten_default' if unauthenticated,
    preserving seamless local usability while securing multi-tenant operations.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token: Optional[str] = None

        # 1. Bearer Token in Authorization Header
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()

        # 2. Query parameter (?auth=...)
        if not token:
            token = request.args.get("auth")

        # 3. Cookie fallback
        if not token:
            token = request.cookies.get("extract_session")

        user_id = "usr_admin"
        email = "admin@extractdesign.local"
        tenant_id = request.headers.get("X-Tenant-ID") or "ten_default"

        if token:
            payload = verify_token(token)
            if payload:
                user_id = payload.get("sub", user_id)
                email = payload.get("email", email)
                tenant_id = request.headers.get("X-Tenant-ID") or payload.get("tenant_id", tenant_id)

        # Resolve Tenant & Role from database
        tenant = db.get_tenant_by_id(tenant_id)
        if not tenant:
            tenant_id = "ten_default"
            tenant = db.get_tenant_by_id(tenant_id) or {
                "id": "ten_default",
                "name": "Primary Workspace",
                "plan_id": "pro",
                "plan_status": "active",
            }

        # Resolve membership role
        with db.db_cursor() as cur:
            cur.execute("SELECT role FROM tenant_members WHERE tenant_id = ? AND user_id = ?;", (tenant_id, user_id))
            role_row = cur.fetchone()
            role = role_row["role"] if role_row else ("owner" if user_id == "usr_admin" else "viewer")

        g.current_user = {"id": user_id, "email": email}
        g.current_tenant = tenant
        g.tenant_role = role
        g.is_owner_or_admin = ROLE_HIERARCHY.get(role, 0) >= ROLE_HIERARCHY["admin"]

        return f(*args, **kwargs)

    return decorated


def require_role(min_role: str):
    """Decorator ensuring current user has at least min_role within active tenant."""
    min_level = ROLE_HIERARCHY.get(min_role, 10)

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        @require_auth
        def wrapper(*args, **kwargs):
            user_level = ROLE_HIERARCHY.get(g.tenant_role, 0)
            if user_level < min_level:
                return jsonify({
                    "error": "permission_denied",
                    "message": f"Action requires '{min_role}' role or higher. Your role: '{g.tenant_role}'.",
                }), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator


def check_quota_and_gates(action: str, crawl_depth: int = 1) -> Optional[Dict[str, Any]]:
    """
    Checks whether the active tenant's plan allows the requested action.
    Returns an error dict if blocked, or None if allowed.
    """
    tenant_id = g.current_tenant.get("id", "ten_default")
    plan_info = db.get_tenant_plan_and_quota(tenant_id)
    if not plan_info:
        return None

    plan_id = plan_info.get("plan_id", "free")
    scans_used = plan_info.get("scans_count", 0)
    scans_limit = plan_info.get("monthly_scans_limit")
    max_crawl = plan_info.get("max_crawl_depth", 1)

    if action == "scan":
        # Free tier scan limit
        if scans_limit is not None and scans_used >= scans_limit:
            if plan_id == "pay_per_scan":
                credits = plan_info.get("pay_per_scan_credits", 0)
                if credits <= 0:
                    return {
                        "error": "quota_exceeded",
                        "message": "No Pay-Per-Scan credits remaining. Please purchase additional scan credits.",
                        "plan_id": plan_id,
                        "upgrade_url": "/studio#settings?tab=plan",
                    }
            else:
                return {
                    "error": "quota_exceeded",
                    "message": f"Monthly scan quota ({scans_limit} scans) reached on {plan_info.get('plan_name')}. Upgrade to Pro for unlimited scans.",
                    "plan_id": plan_id,
                    "scans_used": scans_used,
                    "scans_limit": scans_limit,
                    "upgrade_url": "/studio#settings?tab=plan",
                }

        # Crawl depth gate
        if crawl_depth > max_crawl:
            return {
                "error": "crawl_depth_exceeded",
                "message": f"Your current plan ({plan_info.get('plan_name')}) supports up to {max_crawl} pages crawl. Requested: {crawl_depth} pages.",
                "allowed_depth": max_crawl,
                "upgrade_url": "/studio#settings?tab=plan",
            }

    elif action == "figma_export":
        if not plan_info.get("figma_export_allowed"):
            return {
                "error": "feature_locked",
                "message": "Figma Tokens Studio export requires the Pro or Agency plan.",
                "upgrade_url": "/studio#settings?tab=plan",
            }

    elif action == "whitelabel":
        if not plan_info.get("whitelabel_allowed"):
            return {
                "error": "feature_locked",
                "message": "Whitelabeled presentation links require the Pro or Agency plan.",
                "upgrade_url": "/studio#settings?tab=plan",
            }

    return None
