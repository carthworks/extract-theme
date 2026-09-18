#!/usr/bin/env python3
"""
extract_theme.py — Backward compatibility shim for core.extractor.
Enables plug-and-play CLI execution (python extract_theme.py <url>) and direct imports.
"""
from __future__ import annotations

import sys
from core.extractor import *
from core.extractor import main

if __name__ == "__main__":
    sys.exit(main())
