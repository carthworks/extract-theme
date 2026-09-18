# ExtractDesign Studio — Documentation Hub

Welcome to the modular documentation hub for **ExtractDesign Studio**.

## Navigation & Architecture

- **[Multi-Tenant & Multi-User Architecture](multi_tenant_plan.md)**: Specifications for tenancy models, RBAC member roles (Owner, Admin, Member, Viewer), quota enforcement, and tier feature gates.
- **[Market Analysis & Value Proposition](market_analysis.md)**: Target audiences (agencies, SaaS developers, design system leads), monetization potential, pricing strategies, and ROI breakdown.
- **[Landing Page Content](landing_copy.md)**: Marketing copy and value-props used across the public showcase.
- **[Visual Assets](assets/)**: System architecture diagrams, screenshots, and visual assets.

## Codebase Organization

```
├── core/       # Core extraction engine, CSS AST parser, intelligence analyzer, storage driver
├── db/         # Multi-tenant SQLite WAL engine, connection pooling, migrations, auth/RBAC
├── public/     # Studio SPA and landing page frontend assets
├── docs/       # Modular technical documentation & specs
├── examples/   # Interactive sample outputs and demonstration files
├── api/        # Serverless deployment entrypoints (Vercel)
└── server.py   # Flask API backend entrypoint
```
