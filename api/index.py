"""
api/index.py — Vercel Serverless Function entrypoint for ExtractTheme Studio.
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

from server import ExtractThemeHandler


class handler(ExtractThemeHandler):
    """
    Vercel serverless function entrypoint.
    Inherits all route handlers from ExtractThemeHandler (S3/R2 storage, projects list, file serving, extraction).
    """
    pass
