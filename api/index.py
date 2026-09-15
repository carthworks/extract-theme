"""
api/index.py — Vercel Serverless Function entrypoint for ExtractTheme Studio.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).parent.parent.resolve()
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from server import ExtractThemeHandler


class handler(ExtractThemeHandler):
    """
    Vercel serverless function entrypoint.
    Inherits all route handlers from ExtractThemeHandler (S3/R2 storage, projects list, file serving, extraction).
    """
    pass
