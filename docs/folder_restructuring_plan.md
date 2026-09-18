# Implementation Plan: Clean, Maintainable & Modular Folder Restructuring

Reorganize **ExtractDesign Studio** into a clean, professional, modular architecture that separates core extraction/analysis engines, database/auth layers, frontend presentation, documentation, and demo fixtures, while preserving 100% plug-and-play backward compatibility for CLI commands, local scripts, and the `app-run.bat` launcher.

---

## User Review Required

> [!IMPORTANT]
> **Zero-Breakage Backward Compatibility Strategy**:
> Rather than breaking existing scripts or commands that call `python extract_theme.py <url>` or `python server.py`, we will place the implementations in dedicated modules (`core/` and `db/`) and retain thin, zero-overhead re-export shims at the project root. This ensures that CLI workflows, automated tests, `app-run.bat`, and `Dockerfile` continue running out-of-the-box without any manual path adjustments.

> [!NOTE]
> **Documentation Consolidation**:
> Multiple strategy, audience, and architecture documents currently scattered across the root directory and `downloaded-themes/example.com/` (e.g., `Who Will Benefit & How.md`, `implementation_plan_multi_tenent.md`, `landing-page-content.md`) will be consolidated into a structured `docs/` directory, adhering to the project's behavioral guidelines.

---

## Proposed Target Structure

```
carthworks/extract-theme/
├── core/                                # Core Engine & Extraction Modules
│   ├── __init__.py
│   ├── extractor.py                     # Web crawling, Playwright driver, DOM & CSS token parser
│   ├── analyzer.py                      # 6-pillar site intelligence & scoring engine
│   └── storage.py                       # Local disk & Cloudflare R2/S3 hybrid storage driver
│
├── db/                                  # Multi-Tenancy & Data Access Layer
│   ├── __init__.py
│   ├── database.py                      # SQLite WAL engine, connection pool, migrations
│   └── auth.py                          # JWT session tokens, RBAC permissions & quota gates
│
├── public/                              # Frontend Presentation Layer (Studio SPA & Landing)
│   ├── index.html                       # ExtractDesign Studio main dashboard
│   ├── app.css, app.js                  # Studio styles & interactive logic
│   ├── landing.html                     # Marketing & conversion showcase page
│   ├── landing.css, landing.js          # Landing page styles & interactions
│   ├── robots.txt, sitemap.xml          # SEO metadata
│   └── assets/                          # Static branding & preview assets
│
├── docs/                                # Modular Project Knowledge & Architecture Specs
│   ├── README.md                        # Documentation hub index
│   ├── architecture.md                  # Multi-tenant architecture & request lifecycle
│   ├── multi_tenant_plan.md             # Multi-user/tenant specification & roadmap
│   ├── market_analysis.md               # Audience breakdown, monetization & ROI analysis
│   ├── landing_copy.md                  # Landing page content source
│   └── assets/                          # System diagrams & UI screenshots (homepage.png, etc.)
│
├── examples/                            # Sample Outputs & Demonstration Demos
│   ├── README.md
│   ├── example-style-guide.html
│   └── example-style-guide_update.html
│
├── api/                                 # Cloud & Serverless Deployment Entrypoints
│   ├── index.py                         # Vercel / serverless WSGI adapter (updated for Flask)
│   └── requirements.txt
│
├── downloaded-themes/                   # Partitioned Output Directory (Scanned Themes)
│   ├── tenants/                         # Multi-tenant isolated scan outputs
│   └── [legacy domain directories]/
│
├── root shims (100% plug & play):
│   ├── server.py                        # Primary Flask server entrypoint (imports from core & db)
│   ├── extract_theme.py                 # CLI backward compatibility shim -> core/extractor.py
│   ├── analyzer.py                      # Compatibility shim -> core/analyzer.py
│   ├── storage.py                       # Compatibility shim -> core/storage.py
│   ├── db.py                            # Compatibility shim -> db/database.py
│   └── auth.py                          # Compatibility shim -> db/auth.py
│
├── app-run.bat                          # 1-Click Windows launcher
├── Dockerfile                           # Container image definition
├── docker-compose.yml                   # Container orchestration
├── requirements.txt                     # Core dependencies
├── settings.json                        # Studio branding & whitelabel defaults
└── .env.example                         # Environment configuration template
```

---

## Detailed Proposed Changes

### 1. Cleanup of Clutter & Misplaced Files

| File | Current Location | Proposed Action | Rationale |
| :--- | :--- | :--- | :--- |
| `extract_theme (1).py` | Project root | **DELETE** | Leftover duplicate download file (90 KB). |
| `homepage.png` | Project root | **MOVE** to `docs/assets/homepage.png` | Cleans up root; preserves README visual asset. |
| `Screenshot 2026-09-15 180753.png` | Project root | **MOVE** to `docs/assets/screenshot.png` | Cleans up root. |
| `landing-page-content.md` | Project root | **MOVE** to `docs/landing_copy.md` | Proper modular documentation structure. |
| `example-style-guide.html` | Project root | **MOVE** to `examples/example-style-guide.html` | Sample HTML should live in `examples/`. |
| `example-style-guide_update.html` | Project root | **MOVE** to `examples/example-style-guide_update.html` | Sample HTML should live in `examples/`. |
| `Who Will Benefit & How.md` | `downloaded-themes/example.com/` | **MOVE** to `docs/market_analysis.md` | Documentation misplaced inside a scanned theme folder. |
| `implementation_plan_multi_tenent.md` | `downloaded-themes/example.com/` | **MOVE** to `docs/multi_tenant_plan.md` | Architecture plan misplaced inside a theme folder. |

---

### 2. Core Package (`core/`)

#### [NEW] [`core/__init__.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/core/__init__.py)
- Defines package exports for `extractor`, `analyzer`, and `storage`.

#### [NEW] [`core/extractor.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/core/extractor.py)
- Migrates full implementation of `extract_theme.py`.
- Encapsulates Playwright/requests web scraping, CSS AST parsing (`tinycss2`), font retrieval, token generation, and HTML style guide builder.

#### [NEW] [`core/analyzer.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/core/analyzer.py)
- Migrates full implementation of `analyzer.py`.
- 6-pillar scoring engine (Visual Hierarchy, Color Cohesion, Typography, Layout, Motion, Code Quality).

#### [NEW] [`core/storage.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/core/storage.py)
- Migrates full implementation of `storage.py`.
- Local disk & Cloudflare R2 / AWS S3 hybrid storage provider.

---

### 3. Database & Auth Package (`db/`)

#### [NEW] [`db/__init__.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/db/__init__.py)
- Package exports for database operations and auth utilities.

#### [NEW] [`db/database.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/db/database.py)
- Migrates the SQLite WAL database engine, schema definition (7 tables), seed data, connection pooling, and project migrations.

#### [NEW] [`db/auth.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/db/auth.py)
- Migrates JWT session generation, verification, RBAC role enforcement (`@require_auth`, `@require_role`), and tenant context resolution.

---

### 4. Root Compatibility Shims (Plug & Play)

#### [MODIFY] [`server.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/server.py)
- Update imports to use `core` and `db` packages (`from core.storage import ...`, `from db import database as db`, `from db import auth`).
- Clean up server initialization and route registration.

#### [MODIFY] [`extract_theme.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/extract_theme.py)
- Becomes a clean CLI shim delegating to `core.extractor`:
  ```python
  from core.extractor import *
  if __name__ == "__main__":
      from core.extractor import main
      main()
  ```

#### [MODIFY] [`db.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/db.py)
- Backward compatibility shim: `from db.database import *`.

#### [MODIFY] [`auth.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/auth.py)
- Backward compatibility shim: `from db.auth import *`.

#### [MODIFY] [`storage.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/storage.py)
- Backward compatibility shim: `from core.storage import *`.

#### [MODIFY] [`analyzer.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/analyzer.py)
- Backward compatibility shim: `from core.analyzer import *`.

---

### 5. Serverless & Deployment Updates

#### [MODIFY] [`api/index.py`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/api/index.py)
- Fix legacy import from `ExtractThemeHandler` to export Flask's WSGI application `app` directly for Vercel/serverless environments.

#### [MODIFY] [`.gitignore`](file:///c:/Users/tkart/Dev/products/CSS_xtraction_style%20guide_generator/.gitignore)
- Add entries for SQLite runtime files (`*.db-shm`, `*.db-wal`, `studio.db`) so local database states are not accidentally committed.

---

## Verification Plan

### Automated Verification
1. **Module Import Test**:
   ```powershell
   python -c "import core; import db; from core.extractor import WebExtractor; from db.database import get_db_connection; print('All core modules imported successfully')"
   ```
2. **Backward Compatibility Shim Test**:
   ```powershell
   python -c "import extract_theme; import storage; import analyzer; import db; import auth; print('All backward compatibility shims functional')"
   ```
3. **Server Startup & Health Check**:
   ```powershell
   python -c "import server; with server.app.test_client() as client: res = client.get('/api/health'); assert res.status_code == 200, res.data; print('Server healthcheck: OK')"
   ```
4. **User & Tenant API Test**:
   ```powershell
   python -c "import server; with server.app.test_client() as client: res = client.get('/api/user/me'); assert res.status_code == 200, res.data; print('Multi-tenant API: OK')"
   ```

### Manual Verification
- Verify that `.\app-run.bat` starts smoothly and serves the Studio dashboard on `http://localhost:8000/`.
- Verify the root directory is pristine and clutter-free.
