"""
db.py — Multi-Tenant Database Layer for ExtractDesign Studio.
Uses SQLite with WAL mode by default for zero-dependency execution.
Provides thread-safe connections, schema initialization, seed data, and migration helpers.
"""

from __future__ import annotations

import json
import os
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = Path(__file__).parent.parent.resolve()
DB_FILE = BASE_DIR / "studio.db"
DOWNLOADED_THEMES_DIR = BASE_DIR / "downloaded-themes"

# Thread-local storage for SQLite connections
_local = threading.local()


def get_db_connection() -> sqlite3.Connection:
    """Returns a thread-local SQLite connection configured for concurrent WAL access."""
    if not hasattr(_local, "conn") or _local.conn is None:
        conn = sqlite3.connect(
            str(DB_FILE),
            timeout=30.0,
            check_same_thread=False,
            isolation_level=None,  # Autocommit mode; transactions managed explicitly
        )
        conn.row_factory = sqlite3.Row
        # Enable WAL mode and foreign keys for high concurrency & integrity
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        _local.conn = conn
    return _local.conn


@contextmanager
def db_cursor():
    """Context manager for executing database operations with automatic rollback on error."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        yield cursor
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()


def init_db() -> None:
    """Creates tables, seeds standard plans, and initializes default workspace."""
    with db_cursor() as cur:
        # 1. Tenants (Organizations / Workspaces)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tenants (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                plan_id TEXT NOT NULL DEFAULT 'free',
                plan_status TEXT NOT NULL DEFAULT 'active',
                billing_cycle TEXT DEFAULT 'monthly',
                current_period_end TEXT,
                stripe_customer_id TEXT,
                stripe_subscription_id TEXT,
                custom_domain TEXT,
                brand_settings TEXT,        -- JSON string
                whitelabel_settings TEXT,   -- JSON string
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 2. Users
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT,
                avatar_url TEXT,
                is_platform_admin INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_login_at TEXT
            );
        """)

        # 3. Tenant Memberships (RBAC)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tenant_members (
                tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
                user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                role TEXT NOT NULL DEFAULT 'member', -- owner, admin, member, viewer
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (tenant_id, user_id)
            );
        """)

        # 4. Plans & Limits Reference
        cur.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price_inr INTEGER NOT NULL,
                price_usd INTEGER NOT NULL,
                monthly_scans_limit INTEGER, -- NULL means unlimited
                max_crawl_depth INTEGER NOT NULL,
                figma_export_allowed INTEGER DEFAULT 0,
                whitelabel_allowed INTEGER DEFAULT 0,
                executive_scorecard_allowed INTEGER DEFAULT 0,
                api_access_allowed INTEGER DEFAULT 0,
                webhooks_allowed INTEGER DEFAULT 0,
                max_team_seats INTEGER DEFAULT 1,
                storage_limit_mb INTEGER DEFAULT 500
            );
        """)

        # 5. Tenant Usage Quotas & Metering
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tenant_quotas (
                tenant_id TEXT PRIMARY KEY REFERENCES tenants(id) ON DELETE CASCADE,
                billing_period_start TEXT NOT NULL,
                billing_period_end TEXT NOT NULL,
                scans_count INTEGER DEFAULT 0,
                crawls_count INTEGER DEFAULT 0,
                storage_bytes_used INTEGER DEFAULT 0,
                pay_per_scan_credits INTEGER DEFAULT 0
            );
        """)

        # 6. Tenant Scanned Projects
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tenant_projects (
                id TEXT PRIMARY KEY,
                tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
                domain TEXT NOT NULL,
                storage_path TEXT NOT NULL,
                created_by_user_id TEXT REFERENCES users(id),
                crawl_depth INTEGER DEFAULT 1,
                scores TEXT, -- JSON string
                meta TEXT,   -- JSON string
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(tenant_id, domain)
            );
        """)

        # 7. API Keys
        cur.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id TEXT PRIMARY KEY,
                tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
                user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                key_hash TEXT UNIQUE NOT NULL,
                key_prefix TEXT NOT NULL,
                name TEXT NOT NULL,
                last_used_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Seed Standard Plans
        plans_data = [
            ("free", "Community Free", 0, 0, 3, 1, 0, 0, 0, 0, 0, 1, 100),
            ("pay_per_scan", "Pay-Per-Scan", 149, 9, None, 5, 1, 0, 1, 0, 0, 1, 1000),
            ("pro", "Pro Agency Plan", 999, 29, None, 10, 1, 1, 1, 0, 0, 3, 10240),
            ("agency", "Workspace Enterprise", 3999, 99, None, 20, 1, 1, 1, 1, 1, 10, 102400),
        ]
        cur.executemany("""
            INSERT OR REPLACE INTO plans (
                id, name, price_inr, price_usd, monthly_scans_limit, max_crawl_depth,
                figma_export_allowed, whitelabel_allowed, executive_scorecard_allowed,
                api_access_allowed, webhooks_allowed, max_team_seats, storage_limit_mb
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, plans_data)

        # Seed Default Tenant & User if not existing
        cur.execute("SELECT id FROM tenants WHERE id = 'ten_default';")
        if not cur.fetchone():
            now = datetime.now(timezone.utc)
            period_end = (now + timedelta(days=30)).isoformat()
            default_brand = json.dumps({
                "name": "ExtractDesign Studio",
                "tagline": "Reverse-engineer design systems & website intelligence",
                "accent_color": "#6366f1",
                "logo_url": "",
                "custom_domain": "design-intel.local",
            })
            default_whitelabel = json.dumps({
                "agency_name": "Apex Digital Studio",
                "agency_url": "https://apexdigital.design",
                "footer_signature": "Design Intelligence Audit prepared by Apex Digital Studio",
                "hide_powered_by": False,
                "default_print_auto": False,
            })

            cur.execute("""
                INSERT INTO tenants (
                    id, name, slug, plan_id, plan_status, billing_cycle,
                    current_period_end, brand_settings, whitelabel_settings
                ) VALUES ('ten_default', 'Primary Workspace', 'primary-workspace', 'pro', 'active', 'monthly', ?, ?, ?);
            """, (period_end, default_brand, default_whitelabel))

            cur.execute("""
                INSERT OR IGNORE INTO users (id, email, full_name, is_platform_admin)
                VALUES ('usr_admin', 'admin@extractdesign.local', 'Primary Admin', 1);
            """)

            cur.execute("""
                INSERT OR IGNORE INTO tenant_members (tenant_id, user_id, role)
                VALUES ('ten_default', 'usr_admin', 'owner');
            """)

            cur.execute("""
                INSERT OR IGNORE INTO tenant_quotas (
                    tenant_id, billing_period_start, billing_period_end, scans_count, crawls_count, storage_bytes_used
                ) VALUES ('ten_default', ?, ?, 14, 4, 190840832);
            """, (now.isoformat(), period_end))

    # Run auto-migration for legacy folders
    migrate_existing_projects_to_default_tenant()


def migrate_existing_projects_to_default_tenant() -> int:
    """Scans downloaded-themes/ and registers any untracked projects into ten_default."""
    if not DOWNLOADED_THEMES_DIR.is_dir():
        return 0

    migrated_count = 0
    with db_cursor() as cur:
        for item in DOWNLOADED_THEMES_DIR.iterdir():
            if not item.is_dir() or item.name in {"tenants", ".git", "__pycache__"}:
                continue

            domain = item.name
            guide_file = item / "style-guide.html"
            tokens_file = item / "design-tokens.json"
            intel_file = item / "site-intelligence.json"

            if guide_file.is_file() or tokens_file.is_file() or intel_file.is_file():
                # Check if already registered
                cur.execute("SELECT id FROM tenant_projects WHERE tenant_id = 'ten_default' AND domain = ?;", (domain,))
                if not cur.fetchone():
                    proj_id = f"prj_{domain.replace('.', '_')}"
                    meta_dict: Dict[str, Any] = {}
                    if intel_file.is_file():
                        try:
                            with open(intel_file, "r", encoding="utf-8") as f:
                                meta_dict = json.load(f).get("metadata", {})
                        except Exception:
                            pass

                    scores_dict = meta_dict.get("intelligence_scores", {})
                    storage_path = f"downloaded-themes/{domain}"

                    cur.execute("""
                        INSERT INTO tenant_projects (
                            id, tenant_id, domain, storage_path, created_by_user_id, scores, meta
                        ) VALUES (?, 'ten_default', ?, ?, 'usr_admin', ?, ?);
                    """, (
                        proj_id,
                        domain,
                        storage_path,
                        json.dumps(scores_dict),
                        json.dumps(meta_dict),
                    ))
                    migrated_count += 1

    return migrated_count


# =============================================================================
# Tenant & User Query Helpers
# =============================================================================

def get_tenant_by_id(tenant_id: str) -> Optional[Dict[str, Any]]:
    with db_cursor() as cur:
        cur.execute("SELECT * FROM tenants WHERE id = ?;", (tenant_id,))
        row = cur.fetchone()
        if not row:
            return None
        d = dict(row)
        d["brand_settings"] = json.loads(d["brand_settings"]) if d.get("brand_settings") else {}
        d["whitelabel_settings"] = json.loads(d["whitelabel_settings"]) if d.get("whitelabel_settings") else {}
        return d


def get_user_tenants(user_id: str) -> List[Dict[str, Any]]:
    """Returns all tenants a user is a member of, along with their role and plan."""
    with db_cursor() as cur:
        cur.execute("""
            SELECT t.id, t.name, t.slug, t.plan_id, t.plan_status, tm.role, p.name as plan_name
            FROM tenant_members tm
            JOIN tenants t ON tm.tenant_id = t.id
            JOIN plans p ON t.plan_id = p.id
            WHERE tm.user_id = ?
            ORDER BY tm.created_at ASC;
        """, (user_id,))
        return [dict(r) for r in cur.fetchall()]


def get_tenant_plan_and_quota(tenant_id: str) -> Dict[str, Any]:
    """Returns combined plan limits and current quota consumption for a tenant."""
    with db_cursor() as cur:
        cur.execute("""
            SELECT 
                t.id as tenant_id, t.name as tenant_name, t.plan_id, t.plan_status, t.current_period_end,
                p.name as plan_name, p.price_inr, p.price_usd, p.monthly_scans_limit, p.max_crawl_depth,
                p.figma_export_allowed, p.whitelabel_allowed, p.executive_scorecard_allowed,
                p.api_access_allowed, p.webhooks_allowed, p.max_team_seats, p.storage_limit_mb,
                q.scans_count, q.crawls_count, q.storage_bytes_used, q.pay_per_scan_credits
            FROM tenants t
            JOIN plans p ON t.plan_id = p.id
            LEFT JOIN tenant_quotas q ON t.id = q.tenant_id
            WHERE t.id = ?;
        """, (tenant_id,))
        row = cur.fetchone()
        if not row:
            return {}
        return dict(row)


def increment_tenant_scan(tenant_id: str, is_crawl: bool = False, depth: int = 1) -> None:
    """Increments the tenant's usage counter."""
    with db_cursor() as cur:
        if is_crawl and depth > 1:
            cur.execute("""
                UPDATE tenant_quotas
                SET scans_count = scans_count + 1, crawls_count = crawls_count + 1
                WHERE tenant_id = ?;
            """, (tenant_id,))
        else:
            cur.execute("""
                UPDATE tenant_quotas
                SET scans_count = scans_count + 1
                WHERE tenant_id = ?;
            """, (tenant_id,))


def get_tenant_projects(tenant_id: str) -> List[Dict[str, Any]]:
    """Lists all scanned projects belonging to a tenant."""
    with db_cursor() as cur:
        cur.execute("""
            SELECT id, domain, storage_path, crawl_depth, scores, meta, created_at, updated_at
            FROM tenant_projects
            WHERE tenant_id = ?
            ORDER BY updated_at DESC;
        """, (tenant_id,))
        results = []
        for r in cur.fetchall():
            item = dict(r)
            item["scores"] = json.loads(item["scores"]) if item.get("scores") else {}
            item["meta"] = json.loads(item["meta"]) if item.get("meta") else {}
            results.append(item)
        return results


def register_tenant_project(
    tenant_id: str,
    domain: str,
    storage_path: str,
    user_id: Optional[str] = None,
    crawl_depth: int = 1,
    scores: Optional[Dict] = None,
    meta: Optional[Dict] = None,
) -> str:
    """Registers or updates a scanned project for a specific tenant."""
    proj_id = f"prj_{domain.replace('.', '_')}"
    with db_cursor() as cur:
        cur.execute("""
            INSERT INTO tenant_projects (
                id, tenant_id, domain, storage_path, created_by_user_id, crawl_depth, scores, meta, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(tenant_id, domain) DO UPDATE SET
                storage_path = excluded.storage_path,
                crawl_depth = excluded.crawl_depth,
                scores = excluded.scores,
                meta = excluded.meta,
                updated_at = CURRENT_TIMESTAMP;
        """, (
            proj_id,
            tenant_id,
            domain,
            storage_path,
            user_id,
            crawl_depth,
            json.dumps(scores or {}),
            json.dumps(meta or {}),
        ))
    return proj_id


def get_tenant_members(tenant_id: str) -> List[Dict[str, Any]]:
    """Returns all users in a tenant with their email and role."""
    with db_cursor() as cur:
        cur.execute("""
            SELECT u.id, u.email, u.full_name, tm.role, tm.created_at as joined_at
            FROM tenant_members tm
            JOIN users u ON tm.user_id = u.id
            WHERE tm.tenant_id = ?
            ORDER BY tm.created_at ASC;
        """, (tenant_id,))
        return [dict(r) for r in cur.fetchall()]


def add_or_invite_member(tenant_id: str, email: str, role: str = "member", full_name: Optional[str] = None) -> Dict[str, Any]:
    """Adds a user to a tenant by email, creating the user record if new."""
    email = email.strip().lower()
    user_id = f"usr_{email.replace('@', '_at_').replace('.', '_')}"
    with db_cursor() as cur:
        cur.execute("""
            INSERT OR IGNORE INTO users (id, email, full_name)
            VALUES (?, ?, ?);
        """, (user_id, email, full_name or email.split("@")[0].capitalize()))

        cur.execute("""
            INSERT OR REPLACE INTO tenant_members (tenant_id, user_id, role)
            VALUES (?, ?, ?);
        """, (tenant_id, user_id, role))

    return {"user_id": user_id, "email": email, "role": role}


def remove_tenant_member(tenant_id: str, user_id: str) -> bool:
    """Removes a member from a tenant. Cannot remove the owner."""
    with db_cursor() as cur:
        cur.execute("SELECT role FROM tenant_members WHERE tenant_id = ? AND user_id = ?;", (tenant_id, user_id))
        row = cur.fetchone()
        if not row or row["role"] == "owner":
            return False
        cur.execute("DELETE FROM tenant_members WHERE tenant_id = ? AND user_id = ?;", (tenant_id, user_id))
        return True


def create_new_tenant(name: str, owner_user_id: str, plan_id: str = "free") -> Dict[str, Any]:
    """Creates a new workspace/tenant and assigns the owner."""
    import re
    slug = re.sub(r"[^a-z0-9-]", "-", name.lower()).strip("-") or "workspace"
    tenant_id = f"ten_{slug[:16]}_{os.urandom(3).hex()}"
    now = datetime.now(timezone.utc)
    period_end = (now + timedelta(days=30)).isoformat()

    default_brand = json.dumps({
        "name": name,
        "tagline": "Reverse-engineer design systems & website intelligence",
        "accent_color": "#6366f1",
        "logo_url": "",
        "custom_domain": "",
    })
    default_whitelabel = json.dumps({
        "agency_name": name,
        "agency_url": "",
        "footer_signature": f"Design Intelligence Audit prepared by {name}",
        "hide_powered_by": False,
        "default_print_auto": False,
    })

    with db_cursor() as cur:
        cur.execute("""
            INSERT INTO tenants (
                id, name, slug, plan_id, plan_status, billing_cycle,
                current_period_end, brand_settings, whitelabel_settings
            ) VALUES (?, ?, ?, ?, 'active', 'monthly', ?, ?, ?);
        """, (tenant_id, name, slug, plan_id, period_end, default_brand, default_whitelabel))

        cur.execute("""
            INSERT INTO tenant_members (tenant_id, user_id, role)
            VALUES (?, ?, 'owner');
        """, (tenant_id, owner_user_id))

        cur.execute("""
            INSERT INTO tenant_quotas (
                tenant_id, billing_period_start, billing_period_end, scans_count, crawls_count, storage_bytes_used
            ) VALUES (?, ?, ?, 0, 0, 0);
        """, (tenant_id, now.isoformat(), period_end))

    return {
        "id": tenant_id,
        "name": name,
        "slug": slug,
        "plan_id": plan_id,
        "role": "owner",
    }
