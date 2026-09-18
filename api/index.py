"""
api/index.py — Vercel Serverless Function entrypoint for ExtractDesign Studio.
Exposes the Flask WSGI application for cloud deployments.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure project root is in sys.path and PYTHONPATH for serverless executions
BASE_DIR = Path(__file__).parent.parent.resolve()
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ["PYTHONPATH"] = f"{BASE_DIR}{os.pathsep}{os.environ.get('PYTHONPATH', '')}"

from server import app

# Vercel WSGI callable
handler = app
