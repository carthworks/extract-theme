#!/usr/bin/env python3
"""
extract-theme — pull a real design system out of any website's CSS.

Fetches a page (or several), collects every stylesheet it references, parses
the CSS properly with tinycss2, resolves custom properties, normalises every
colour and length it finds, and emits a usable design system:

    out/
    ├── style-guide.html      interactive, self-contained
    ├── design-tokens.json    machine-readable
    ├── theme.css             :root custom properties + dark scope
    ├── components.css        buttons / cards / inputs built on the tokens
    ├── tailwind.theme.css    Tailwind v4  @theme block
    ├── tailwind.config.js    Tailwind v3  config
    └── raw/
        ├── combined.css      every rule, url() rewritten to absolute
        └── sheet-001.css     each stylesheet as fetched

Usage
    python extract_theme.py https://example.com
    python extract_theme.py https://example.com --crawl 8 -o ./theme
    python extract_theme.py ./local/page.html
    python extract_theme.py https://a.com https://b.com --max-colors 24

Install
    pip install requests beautifulsoup4 tinycss2
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import hashlib
import json
import math
import re
import sys
import textwrap
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence
from urllib.parse import urljoin, urlparse, urldefrag

try:
    import requests
except ImportError:  # pragma: no cover
    sys.exit("Missing dependency: pip install requests")

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    sys.exit("Missing dependency: pip install beautifulsoup4")

try:
    import tinycss2
except ImportError:  # pragma: no cover
    sys.exit("Missing dependency: pip install tinycss2")


__version__ = "2.0.0"

DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

# ---------------------------------------------------------------------------
# logging
# ---------------------------------------------------------------------------

_VERBOSITY = 1


def log(msg: str, level: int = 1) -> None:
    if _VERBOSITY >= level:
        print(msg, file=sys.stderr)


def warn(msg: str) -> None:
    log(f"  ! {msg}", 1)


# ===========================================================================
# 1.  COLOUR
# ===========================================================================

_NAMED_RAW = """
aliceblue:f0f8ff antiquewhite:faebd7 aqua:00ffff aquamarine:7fffd4 azure:f0ffff beige:f5f5dc
bisque:ffe4c4 black:000000 blanchedalmond:ffebcd blue:0000ff blueviolet:8a2be2 brown:a52a2a
burlywood:deb887 cadetblue:5f9ea0 chartreuse:7fff00 chocolate:d2691e coral:ff7f50
cornflowerblue:6495ed cornsilk:fff8dc crimson:dc143c cyan:00ffff darkblue:00008b
darkcyan:008b8b darkgoldenrod:b8860b darkgray:a9a9a9 darkgreen:006400 darkgrey:a9a9a9
darkkhaki:bdb76b darkmagenta:8b008b darkolivegreen:556b2f darkorange:ff8c00
darkorchid:9932cc darkred:8b0000 darksalmon:e9967a darkseagreen:8fbc8f darkslateblue:483d8b
darkslategray:2f4f4f darkslategrey:2f4f4f darkturquoise:00ced1 darkviolet:9400d3
deeppink:ff1493 deepskyblue:00bfff dimgray:696969 dimgrey:696969 dodgerblue:1e90ff
firebrick:b22222 floralwhite:fffaf0 forestgreen:228b22 fuchsia:ff00ff gainsboro:dcdcdc
ghostwhite:f8f8ff gold:ffd700 goldenrod:daa520 gray:808080 green:008000 greenyellow:adff2f
grey:808080 honeydew:f0fff0 hotpink:ff69b4 indianred:cd5c5c indigo:4b0082 ivory:fffff0
khaki:f0e68c lavender:e6e6fa lavenderblush:fff0f5 lawngreen:7cfc00 lemonchiffon:fffacd
lightblue:add8e6 lightcoral:f08080 lightcyan:e0ffff lightgoldenrodyellow:fafad2
lightgray:d3d3d3 lightgreen:90ee90 lightgrey:d3d3d3 lightpink:ffb6c1 lightsalmon:ffa07a
lightseagreen:20b2aa lightskyblue:87cefa lightslategray:778899 lightslategrey:778899
lightsteelblue:b0c4de lightyellow:ffffe0 lime:00ff00 limegreen:32cd32 linen:faf0e6
magenta:ff00ff maroon:800000 mediumaquamarine:66cdaa mediumblue:0000cd mediumorchid:ba55d3
mediumpurple:9370db mediumseagreen:3cb371 mediumslateblue:7b68ee mediumspringgreen:00fa9a
mediumturquoise:48d1cc mediumvioletred:c71585 midnightblue:191970 mintcream:f5fffa
mistyrose:ffe4e1 moccasin:ffe4b5 navajowhite:ffdead navy:000080 oldlace:fdf5e6 olive:808000
olivedrab:6b8e23 orange:ffa500 orangered:ff4500 orchid:da70d6 palegoldenrod:eee8aa
palegreen:98fb98 paleturquoise:afeeee palevioletred:db7093 papayawhip:ffefd5
peachpuff:ffdab9 peru:cd853f pink:ffc0cb plum:dda0dd powderblue:b0e0e6 purple:800080
rebeccapurple:663399 red:ff0000 rosybrown:bc8f8f royalblue:4169e1 saddlebrown:8b4513
salmon:fa8072 sandybrown:f4a460 seagreen:2e8b57 seashell:fff5ee sienna:a0522d silver:c0c0c0
skyblue:87ceeb slateblue:6a5acd slategray:708090 slategrey:708090 snow:fffafa
springgreen:00ff7f steelblue:4682b4 tan:d2b48c teal:008080 thistle:d8bfd8 tomato:ff6347
turquoise:40e0d0 violet:ee82ee wheat:f5deb3 white:ffffff whitesmoke:f5f5f5 yellow:ffff00
yellowgreen:9acd32
"""
NAMED_COLORS: dict[str, str] = dict(
    part.split(":") for part in _NAMED_RAW.split()
)

# Words that look like colours to a naive regex but carry no palette meaning.
COLOR_NOISE = {
    "transparent", "inherit", "initial", "unset", "revert",
    "currentcolor", "none", "auto",
}


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


@dataclass(frozen=True)
class Color:
    """A colour normalised to 8-bit sRGB + alpha."""

    r: int
    g: int
    b: int
    a: float = 1.0

    # -- representations ---------------------------------------------------

    @property
    def hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    @property
    def css(self) -> str:
        if self.a >= 0.999:
            return self.hex
        return f"rgb({self.r} {self.g} {self.b} / {round(self.a, 3)})"

    @property
    def rgb_channels(self) -> str:
        """`R G B` — usable as `rgb(var(--x) / .5)` in a theme file."""
        return f"{self.r} {self.g} {self.b}"

    # -- perceptual --------------------------------------------------------

    @property
    def oklab(self) -> tuple[float, float, float]:
        r = _srgb_to_linear(self.r / 255)
        g = _srgb_to_linear(self.g / 255)
        b = _srgb_to_linear(self.b / 255)
        l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
        m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
        s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
        l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
        return (
            0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
        )

    @property
    def oklch(self) -> tuple[float, float, float]:
        L, a, b = self.oklab
        return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360

    @property
    def luminance(self) -> float:
        """WCAG relative luminance."""
        r, g, b = (_srgb_to_linear(v / 255) for v in (self.r, self.g, self.b))
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def distance(self, other: "Color") -> float:
        """
        Perceptual distance in OKLab (<0.02 is imperceptible), with alpha
        folded in. Without the alpha term a fully transparent white sits at
        distance 0 from opaque white, and role inference happily assigns
        `--foreground: rgb(255 255 255 / 0)`.
        """
        return math.dist(self.oklab, other.oklab) + abs(self.a - other.a) * 0.6

    @property
    def is_overlay(self) -> bool:
        return self.a < 0.98

    def contrast(self, other: "Color") -> float:
        l1, l2 = sorted((self.luminance, other.luminance), reverse=True)
        return (l1 + 0.05) / (l2 + 0.05)

    def on_white(self) -> "Color":
        """Flatten alpha against white — needed to judge translucent colours."""
        if self.a >= 0.999:
            return self
        f = lambda c: round(c * self.a + 255 * (1 - self.a))
        return Color(f(self.r), f(self.g), f(self.b), 1.0)


# -- parsing ---------------------------------------------------------------

_HEX_RE = re.compile(r"#([0-9a-fA-F]{3,8})\b")
_FUNC_RE = re.compile(
    r"\b(rgba?|hsla?|hwb|oklch|oklab|lab|lch|color-mix)\(", re.I
)
_NAME_RE = re.compile(
    r"(?<![\w-])(" + "|".join(sorted(NAMED_COLORS, key=len, reverse=True)) + r")(?![\w-])",
    re.I,
)
_NUM = r"[-+]?(?:\d*\.\d+|\d+)"


def _pct_or_num(tok: str, scale: float = 255.0) -> float:
    tok = tok.strip()
    if tok.endswith("%"):
        return float(tok[:-1]) / 100 * scale
    return float(tok)


def _alpha(tok: str | None) -> float:
    if tok is None:
        return 1.0
    tok = tok.strip()
    if not tok or tok in {"none"}:
        return 1.0
    try:
        return max(0.0, min(1.0, _pct_or_num(tok, 1.0)))
    except ValueError:
        return 1.0


def _hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
    h = h % 360
    s = max(0.0, min(1.0, s))
    l = max(0.0, min(1.0, l))
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    rgb = [
        (c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)
    ][int(h // 60) % 6]
    return tuple(round((v + m) * 255) for v in rgb)  # type: ignore[return-value]


def _oklch_to_rgb(L: float, C: float, h: float) -> tuple[int, int, int]:
    hr = math.radians(h)
    a, b = C * math.cos(hr), C * math.sin(hr)
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    lr = +4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
    lg = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
    lb = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_

    def enc(c: float) -> int:
        c = max(0.0, min(1.0, c))
        c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
        return round(max(0.0, min(1.0, c)) * 255)

    return enc(lr), enc(lg), enc(lb)


def _split_args(inner: str) -> list[str]:
    """Split `1, 2, 3 / .5` or `1 2 3 / .5` into flat argument tokens."""
    inner = inner.replace("/", " / ")
    parts = [p for p in re.split(r"[,\s]+", inner.strip()) if p]
    return parts


def parse_color(text: str) -> Color | None:
    """Parse a single CSS colour literal. Returns None if it isn't one."""
    text = text.strip().rstrip(";").strip()
    if not text or text.lower() in COLOR_NOISE:
        return None

    low = text.lower()
    if low in NAMED_COLORS:
        h = NAMED_COLORS[low]
        return Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    m = _HEX_RE.fullmatch(text)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) not in (6, 8):
            return None
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return Color(r, g, b, round(a, 4))

    fm = re.fullmatch(r"([a-z-]+)\((.*)\)", text, re.I | re.S)
    if not fm:
        return None
    fn, inner = fm.group(1).lower(), fm.group(2)
    if "var(" in inner or "calc(" in inner:
        return None
    args = _split_args(inner)
    try:
        if fn in ("rgb", "rgba"):
            if len(args) < 3:
                return None
            r, g, b = (_pct_or_num(a) for a in args[:3])
            rest = [a for a in args[3:] if a != "/"]
            return Color(
                _clamp8(r), _clamp8(g), _clamp8(b),
                _alpha(rest[0] if rest else None),
            )

        if fn in ("hsl", "hsla"):
            if len(args) < 3:
                return None
            h = float(re.sub(r"(deg|grad|rad|turn)$", "", args[0]))
            s = _pct_or_num(args[1], 1.0)
            l = _pct_or_num(args[2], 1.0)
            rest = [a for a in args[3:] if a != "/"]
            return Color(*_hsl_to_rgb(h, s, l), _alpha(rest[0] if rest else None))

        if fn in ("oklch", "lch"):
            if len(args) < 3:
                return None
            L = _pct_or_num(args[0], 1.0)
            C = float(args[1].rstrip("%")) * (0.4 if args[1].endswith("%") else 1.0)
            h = float(re.sub(r"(deg)$", "", args[2])) if args[2] != "none" else 0.0
            if fn == "lch":  # rough: treat as oklch after scaling
                L, C = L / 100 if L > 1 else L, C / 150 * 0.4
            rest = [a for a in args[3:] if a != "/"]
            return Color(*_oklch_to_rgb(L, C, h), _alpha(rest[0] if rest else None))
    except (ValueError, IndexError):
        return None
    return None


def _clamp8(v: float) -> int:
    return max(0, min(255, int(round(v))))


def find_colors(value: str) -> list[Color]:
    """Every colour literal inside an arbitrary declaration value."""
    out: list[Color] = []
    # quoted strings hold font names and content, never colours
    value = re.sub(r"""(['"]).*?\1""", " ", value)
    for m in _FUNC_RE.finditer(value):
        depth, i = 0, m.end() - 1
        for j in range(m.end() - 1, len(value)):
            if value[j] == "(":
                depth += 1
            elif value[j] == ")":
                depth -= 1
                if depth == 0:
                    i = j
                    break
        c = parse_color(value[m.start():i + 1])
        if c:
            out.append(c)
    for m in _HEX_RE.finditer(value):
        c = parse_color(m.group(0))
        if c:
            out.append(c)
    for m in _NAME_RE.finditer(value):
        # ignore names that are part of a font stack or an identifier
        c = parse_color(m.group(0))
        if c:
            out.append(c)
    return out


# -- naming ----------------------------------------------------------------

HUE_ANCHORS = [
    ("red", 29), ("orange", 52), ("amber", 71), ("yellow", 92),
    ("lime", 128), ("green", 150), ("emerald", 163), ("teal", 185),
    ("cyan", 205), ("sky", 232), ("blue", 259), ("indigo", 274),
    ("violet", 293), ("purple", 309), ("fuchsia", 323), ("pink", 354),
    ("rose", 16),
]
STEP_LIGHTNESS = [
    (50, 0.971), (100, 0.936), (200, 0.885), (300, 0.808), (400, 0.704),
    (500, 0.637), (600, 0.577), (700, 0.505), (800, 0.444), (900, 0.396),
    (950, 0.258),
]


def color_name(c: Color) -> str:
    """
    Tailwind-shaped name: `blue-600`, `slate-100`, `white`.

    Naming reads the colour's OWN channels. Flattening against white first
    (the obvious shortcut) makes every low-alpha colour look white, so
    `rgb(12 12 12 / 0)` gets named "white" — it is black.
    """
    L, C, H = c.oklch
    if c.r == c.g == c.b:
        if c.r >= 250:
            return "white"
        if c.r <= 8:
            return "black"
    if C < 0.055:
        # Low-chroma colours are greys with a tint. Naming them "blue-600"
        # is technically true and practically useless.
        family = (
            "neutral" if C < 0.015
            else "slate" if 190 <= H < 310
            else "stone" if H < 110 or H >= 330
            else "zinc"
        )
    else:
        family = min(
            HUE_ANCHORS,
            key=lambda kv: min(abs(H - kv[1]), 360 - abs(H - kv[1])),
        )[0]
    step = min(STEP_LIGHTNESS, key=lambda kv: abs(L - kv[1]))[0]
    return f"{family}-{step}"


# ===========================================================================
# 2.  LENGTHS
# ===========================================================================

LEN_RE = re.compile(rf"(?<![\w.]){_NUM}(px|rem|em|%|vh|vw|vmin|vmax|pt|ch|ex)\b")
BARE_ZERO_RE = re.compile(r"(?<![\w.#-])0(?![\w.%])")


def to_px(value: str, root_px: float = 16.0) -> float | None:
    """Best-effort conversion of a single length token to px. None if relative."""
    m = re.fullmatch(rf"({_NUM})(px|rem|em|pt)?", value.strip())
    if not m:
        return None
    n = float(m.group(1))
    unit = m.group(2) or ("px" if n == 0 else None)
    if unit == "px":
        return n
    if unit in ("rem", "em"):
        return n * root_px
    if unit == "pt":
        return n * 4 / 3
    return None


def length_tokens(value: str) -> list[str]:
    """Split `0 1px 3px 0 rgba(...)` into `['0','1px','3px','0']`."""
    value = re.sub(r"\w+\([^)]*\)", " ", value)  # drop functions
    out = []
    for tok in value.split():
        tok = tok.strip(",")
        if LEN_RE.fullmatch(tok) or re.fullmatch(r"0", tok):
            out.append(tok)
    return out


# ===========================================================================
# 3.  FETCHING
# ===========================================================================


@dataclass
class Asset:
    url: str
    text: str
    kind: str = "external"        # external | inline | attribute
    file: str | None = None


class Fetcher:
    def __init__(self, timeout: int, workers: int, ua: str, verify: bool):
        self.timeout = timeout
        self.workers = workers
        self.verify = verify
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": ua,
                "Accept": "text/html,text/css,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )
        self._cache: dict[str, tuple[str, str]] = {}

    def get(self, url: str) -> tuple[str, str]:
        """Returns (final_url, text). Supports local paths."""
        if url in self._cache:
            return self._cache[url]

        if not re.match(r"^https?://", url):
            local = url[7:] if url.startswith("file://") else url
            p = Path(local).expanduser().resolve()
            if not p.exists():
                raise FileNotFoundError(url)
            result = (p.as_uri(), p.read_text(encoding="utf-8", errors="replace"))
        else:
            for attempt in range(3):
                try:
                    r = self.session.get(
                        url, timeout=self.timeout, verify=self.verify,
                        allow_redirects=True,
                    )
                    r.raise_for_status()
                    if not r.encoding or r.encoding.lower() == "iso-8859-1":
                        r.encoding = r.apparent_encoding or "utf-8"
                    result = (r.url, r.text)
                    break
                except requests.RequestException:
                    if attempt == 2:
                        raise
                    time.sleep(0.6 * (attempt + 1))
        self._cache[url] = result
        return result

    def get_many(self, urls: Sequence[str]) -> list[tuple[str, str, str]]:
        """Parallel fetch. Yields (requested_url, final_url, text) for successes."""
        out: list[tuple[str, str, str]] = []
        if not urls:
            return out
        with futures.ThreadPoolExecutor(max_workers=self.workers) as pool:
            jobs = {pool.submit(self.get, u): u for u in urls}
            for job in futures.as_completed(jobs):
                u = jobs[job]
                try:
                    final, text = job.result()
                    out.append((u, final, text))
                except Exception as exc:  # noqa: BLE001
                    warn(f"{u} — {type(exc).__name__}")
        return out


def clean_url(url: str) -> str:
    return urldefrag(url)[0]


def same_site(a: str, b: str) -> bool:
    na, nb = urlparse(a).netloc, urlparse(b).netloc
    return na.removeprefix("www.") == nb.removeprefix("www.")


# ===========================================================================
# 4.  DISCOVERY
# ===========================================================================

STYLESHEET_RELS = {"stylesheet", "preload"}


def discover(page_url: str, html: str) -> tuple[list[str], list[Asset], list[str], list[str]]:
    """
    Returns (external_css_urls, inline_assets, font_links, page_links).
    """
    soup = BeautifulSoup(html, "html.parser")
    external: list[str] = []
    inline: list[Asset] = []
    fonts: list[str] = []

    for link in soup.find_all("link", href=True):
        rels = {r.lower() for r in (link.get("rel") or [])}
        as_attr = (link.get("as") or "").lower()
        href = clean_url(urljoin(page_url, link["href"]))
        if "stylesheet" in rels or (rels & {"preload"} and as_attr == "style"):
            external.append(href)
            if "fonts.googleapis" in href or "font" in href:
                fonts.append(href)

    for i, style in enumerate(soup.find_all("style"), 1):
        css = style.get_text() or ""
        if css.strip():
            inline.append(
                Asset(url=f"{page_url}#style-{i}", text=css, kind="inline")
            )

    attrs = [t["style"] for t in soup.find_all(style=True) if t.get("style")]
    if attrs:
        # wrap so the parser sees valid rules
        body = "\n".join(f"[data-inline-{i}]{{{s}}}" for i, s in enumerate(attrs))
        inline.append(Asset(url=f"{page_url}#style-attrs", text=body, kind="attribute"))

    links = []
    for a in soup.find_all("a", href=True):
        u = clean_url(urljoin(page_url, a["href"]))
        if u.startswith("file://") or (u.startswith("http") and same_site(page_url, u)):
            links.append(u)

    return external, inline, fonts, links


IMPORT_RE = re.compile(
    r"""@import\s+(?:url\(\s*)?["']?([^"')\s;]+)["']?\s*\)?[^;]*;""", re.I
)
URL_RE = re.compile(r"""url\(\s*(['"]?)([^'")]+)\1\s*\)""")


def absolutise_urls(css: str, base: str) -> str:
    def sub(m: re.Match[str]) -> str:
        q, u = m.group(1), m.group(2).strip()
        if u.startswith(("data:", "http://", "https://", "#")):
            return m.group(0)
        return f'url({q}{urljoin(base, u)}{q})'

    return URL_RE.sub(sub, css)


def resolve_imports(
    fetcher: Fetcher, base: str, css: str, seen: set[str], depth: int = 0
) -> str:
    if depth > 5:
        return css
    chunks: list[str] = []
    for raw in IMPORT_RE.findall(css):
        url = clean_url(urljoin(base, raw))
        if url in seen:
            continue
        seen.add(url)
        try:
            final, imported = fetcher.get(url)
        except Exception as exc:  # noqa: BLE001
            warn(f"@import {url} — {type(exc).__name__}")
            continue
        log(f"    @import {url}", 2)
        imported = absolutise_urls(imported, final)
        chunks.append(resolve_imports(fetcher, final, imported, seen, depth + 1))
    return css + ("\n\n" + "\n\n".join(chunks) if chunks else "")


# ===========================================================================
# 5.  CSS PARSING
# ===========================================================================


@dataclass
class Decl:
    prop: str
    value: str
    selector: str
    at: str = ""            # serialized enclosing at-rule prelude
    dark: bool = False
    source: str = ""


# Sites name their dark scope in a dozen ways: data-bs-theme, data-color-mode,
# data-color-scheme, .dark, .theme-dark. Miss it and the dark palette silently
# overwrites the light one in the cascade, inverting every inferred role.
DARK_SELECTOR_RE = re.compile(
    r"""(?:\.(?:dark|theme-dark|dark-mode|dark-theme)\b"""
    r"""|\[data-[\w-]*(?:theme|mode|scheme)[~^|*$]?=["']?dark)""",
    re.I,
)


def _parse_declarations(content):
    """tinycss2 renamed this API; support both."""
    fn = getattr(tinycss2, "parse_blocks_contents", None) or tinycss2.parse_declaration_list
    return fn(content)


def parse_css(css: str, source: str) -> tuple[list[Decl], list[str], list[dict]]:
    """
    Returns (declarations, media_preludes, font_faces).
    Walks nested at-rules so rules inside @media/@supports/@layer are included.
    """
    decls: list[Decl] = []
    medias: list[str] = []
    faces: list[dict] = []

    def walk(rules, at: str, dark: bool) -> None:
        for rule in rules:
            if rule.type == "qualified-rule":
                sel = tinycss2.serialize(rule.prelude).strip()
                sel = re.sub(r"\s+", " ", sel)[:400]
                is_dark = dark or bool(DARK_SELECTOR_RE.search(sel))
                for d in _parse_declarations(rule.content):
                    if d.type != "declaration":
                        continue
                    val = tinycss2.serialize(d.value).strip()
                    if not val:
                        continue
                    name = d.name if d.name.startswith("--") else d.lower_name
                    decls.append(
                        Decl(name, val, sel, at, is_dark, source)
                    )
            elif rule.type == "at-rule":
                kw = (rule.lower_at_keyword or "").lower()
                prelude = tinycss2.serialize(rule.prelude).strip()
                prelude = re.sub(r"\s+", " ", prelude)
                if kw == "font-face" and rule.content:
                    face = {}
                    for d in _parse_declarations(rule.content):
                        if d.type == "declaration":
                            face[d.lower_name] = tinycss2.serialize(d.value).strip()
                    if face:
                        faces.append(face)
                elif kw in ("media", "supports", "layer", "container", "scope") and rule.content:
                    if kw == "media":
                        medias.append(prelude)
                    nested_dark = dark or (
                        kw == "media" and "prefers-color-scheme" in prelude
                        and "dark" in prelude
                    )
                    nested_at = f"@{kw} {prelude}".strip() if prelude else f"@{kw}"
                    try:
                        walk(
                            tinycss2.parse_rule_list(
                                rule.content, skip_comments=True, skip_whitespace=True
                            ),
                            nested_at,
                            nested_dark,
                        )
                    except Exception:  # noqa: BLE001
                        pass
                elif kw == "keyframes" and rule.content:
                    try:
                        walk(
                            tinycss2.parse_rule_list(
                                rule.content, skip_comments=True, skip_whitespace=True
                            ),
                            "@keyframes",
                            dark,
                        )
                    except Exception:  # noqa: BLE001
                        pass

    walk(
        tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True),
        "",
        False,
    )
    return decls, medias, faces


VAR_REF_RE = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,([^()]*(?:\([^()]*\)[^()]*)*))?\)")


def build_var_map(decls: Iterable[Decl]) -> tuple[dict[str, str], dict[str, str]]:
    """Custom-property definitions, split light/dark. Later wins."""
    light: dict[str, str] = {}
    dark: dict[str, str] = {}
    for d in decls:
        if not d.prop.startswith("--"):
            continue
        (dark if d.dark else light)[d.prop] = d.value
    return light, dark


def resolve_vars(value: str, table: dict[str, str], depth: int = 0) -> str:
    if depth > 8 or "var(" not in value:
        return value

    def sub(m: re.Match[str]) -> str:
        name, fallback = m.group(1), (m.group(2) or "").strip()
        target = table.get(name)
        if target is None:
            return fallback or m.group(0)
        return target

    new = VAR_REF_RE.sub(sub, value)
    return new if new == value else resolve_vars(new, table, depth + 1)


# ===========================================================================
# 6.  TOKEN EXTRACTION
# ===========================================================================

COLOR_PROPS = (
    "color", "background", "background-color", "background-image", "border",
    "border-color", "border-top-color", "border-right-color",
    "border-bottom-color", "border-left-color", "outline", "outline-color",
    "fill", "stroke", "box-shadow", "text-shadow", "caret-color",
    "text-decoration-color", "accent-color", "column-rule-color",
    "background-clip", "--",
)
SPACING_PROPS = (
    "margin", "padding", "gap", "row-gap", "column-gap", "inset",
    "top", "right", "bottom", "left", "translate",
)
TEXT_PROPS = ("font-size", "line-height", "letter-spacing", "font-weight")

# Properties whose values carry fg/bg semantics, used for role inference.
FG_PROPS = {"color", "fill"}
BG_PROPS = {"background", "background-color"}

# `body { color: … }` states the document's ink far more reliably than the
# hundred utility classes that happen to repeat a shade. Weight it accordingly.
ROOT_SEL_RE = re.compile(
    r"^(?:html|body|:root|:where\(html\)|\*)(?:[:.\[][^,]*)?$", re.I
)


def root_weight(selector: str) -> int:
    parts = [p.strip() for p in selector.split(",")]
    return 60 if any(ROOT_SEL_RE.match(p) for p in parts if p) else 1


def _cluster(counts: Counter[Color], tol: float) -> list[tuple[Color, int]]:
    """Merge perceptually identical colours, keeping the most-used representative."""
    ordered = counts.most_common()
    reps: list[list] = []
    for color, n in ordered:
        for rep in reps:
            if abs(rep[0].a - color.a) < 0.05 and rep[0].distance(color) < tol:
                rep[1] += n
                break
        else:
            reps.append([color, n])
    reps.sort(key=lambda r: -r[1])
    return [(r[0], r[1]) for r in reps]


def collect_colors(
    decls: Sequence[Decl], var_map: dict[str, str], tol: float
) -> tuple[list[tuple[Color, int]], Counter[Color], Counter[Color]]:
    counts: Counter[Color] = Counter()
    fg: Counter[Color] = Counter()
    bg: Counter[Color] = Counter()
    for d in decls:
        base = d.prop.split("-")[0]
        if "shadow" in d.prop:
            # shadow tints are captured verbatim in the shadow scale; letting them
            # into the palette fills it with near-transparent greys
            continue
        if not (
            d.prop.startswith("--")
            or d.prop in COLOR_PROPS
            or base in ("color", "background", "border", "outline", "fill", "stroke")
        ):
            continue
        if d.prop.startswith("--") and re.search(r"shadow|ring|glow", d.prop):
            continue
        if re.search(r"font|family|typeface", d.prop):
            continue
        value = resolve_vars(d.value, var_map) if "var(" in d.value else d.value
        found = find_colors(value)
        # weight: tokens declared on :root are design decisions, not usage
        weight = 3 if d.prop.startswith("--") and ":root" in d.selector else 1
        rw = root_weight(d.selector)
        for c in found:
            counts[c] += weight
            if d.prop in FG_PROPS:
                fg[c] += rw
            elif d.prop in BG_PROPS and len(found) == 1:
                bg[c] += rw
    return _cluster(counts, tol), fg, bg


STEPS = [s for s, _l in STEP_LIGHTNESS]


def continuous_step(L: float) -> float:
    """
    Map OKLab lightness onto the 50–950 step scale, interpolating between the
    anchors and extrapolating past 950 for the very dark end.
    """
    pts = STEP_LIGHTNESS
    if L >= pts[0][1]:
        return 25.0
    for (s1, l1), (s2, l2) in zip(pts, pts[1:]):
        if l2 <= L <= l1:
            t = (l1 - L) / (l1 - l2) if l1 != l2 else 0.0
            return s1 + t * (s2 - s1)
    tail = (pts[-2][1] - pts[-1][1]) or 0.1
    return min(1000.0, 950 + (pts[-1][1] - L) / tail * 50)


def name_palette(entries: Sequence[tuple[Color, int]]) -> dict[str, Color]:
    """
    Assign stable names, then resolve collisions by *subdividing the lightness
    ramp* rather than appending -2, -3, -4.

    A dark-first product legitimately ships six near-black surfaces. Calling
    them neutral-950 through neutral-950-5 destroys the only information a
    reader needs: which one is darker. They become 900 / 925 / 950 / 975.
    """
    groups: dict[tuple[str, str], list[Color]] = defaultdict(list)
    flat: list[Color] = []
    for color, _n in entries:
        name = color_name(color)
        if "-" in name and name.rsplit("-", 1)[1].isdigit():
            family, _step = name.rsplit("-", 1)
            alpha = f"a{round(color.a * 100)}" if color.is_overlay else ""
            groups[(family, alpha)].append(color)
        else:
            flat.append(color)

    used: dict[str, Color] = {}

    def claim(name: str, color: Color) -> None:
        final, i = name, 2
        while final in used:
            final, i = f"{name}-{i}", i + 1
        used[final] = color

    for color in flat:
        base = color_name(color)
        claim(f"{base}-a{round(color.a * 100)}" if color.is_overlay else base, color)

    for (family, alpha), colors in groups.items():
        # Assign from the dark end upward. Going the other way lets a crowded
        # dark cluster overflow past 950 into invented steps like neutral-1050.
        colors.sort(key=lambda c: c.oklch[0])            # darkest first
        suffix = f"-{alpha}" if alpha else ""
        last = STEPS[-1] + 25
        for color in colors:
            cont = continuous_step(color.oklch[0])
            snap = min(STEPS, key=lambda st: abs(st - cont))
            step = snap if snap < last else max(25, last - 25)
            last = step
            claim(f"{family}-{step}{suffix}", color)

    for name in [n for n in used if n.endswith("-2")]:
        base = name[:-2]
        if base not in used:
            used[base] = used.pop(name)

    return dict(sorted(used.items(), key=lambda kv: -entry_count(entries, kv[1])))


def entry_count(entries: Sequence[tuple[Color, int]], color: Color) -> int:
    return next((n for c, n in entries if c == color), 0)


def collect_property(
    decls: Sequence[Decl],
    props: Sequence[str],
    var_hint: str | None = None,
) -> Counter[str]:
    """
    Count declared values for a set of properties.

    `var_hint` is a regex matched against custom-property *names*: a site that
    declares `--radius: 8px` and only ever uses `border-radius: var(--radius)`
    would otherwise contribute nothing to the radius scale.
    """
    c: Counter[str] = Counter()
    wanted = set(props)
    hint = re.compile(var_hint, re.I) if var_hint else None
    for d in decls:
        val = re.sub(r"\s+", " ", d.value.strip())
        if not val or val.startswith("var("):
            continue
        if d.prop in wanted:
            c[val] += 1
        elif hint and d.prop.startswith("--") and hint.search(d.prop):
            c[val] += 2   # an explicitly declared token outranks incidental use
    return c


def detect_grid(counts: Counter[float]) -> float:
    """
    Infer the base unit by scoring candidate grids on how much of the
    (frequency-weighted) usage lands on them. Almost every system is 4 or 8.
    """
    best, best_score = 4.0, -1.0
    for unit in (2.0, 4.0, 5.0, 6.0, 8.0):
        hit = sum(n for px, n in counts.items() if px % unit == 0)
        total = sum(counts.values()) or 1
        score = (hit / total) * (1 + unit / 40)   # mild bias to a coarser grid
        if score > best_score:
            best, best_score = unit, score
    return best


SPACING_VAR_RE = re.compile(r"^--(space|spacing|gap|gutter|pad)", re.I)


def collect_spacing(decls: Sequence[Decl], root_px: float) -> Counter[float]:
    c: Counter[float] = Counter()
    for d in decls:
        is_var = SPACING_VAR_RE.match(d.prop)
        if not (
            is_var
            or d.prop in SPACING_PROPS
            or d.prop.split("-")[0] in ("margin", "padding")
        ):
            continue
        for tok in length_tokens(d.value):
            px = to_px(tok, root_px)
            if px is not None and 0 <= px <= 256:
                c[round(px, 2)] += 1
    return c


TEXT_SIZE_NAMES = [
    ("xs", 12), ("sm", 14), ("base", 16), ("lg", 18), ("xl", 20),
    ("2xl", 24), ("3xl", 30), ("4xl", 36), ("5xl", 48), ("6xl", 60),
    ("7xl", 72), ("8xl", 96), ("9xl", 128),
]
RADIUS_NAMES = [
    ("none", 0), ("sm", 2), ("DEFAULT", 4), ("md", 6), ("lg", 8),
    ("xl", 12), ("2xl", 16), ("3xl", 24),
]
BREAKPOINT_NAMES = [("sm", 640), ("md", 768), ("lg", 1024), ("xl", 1280), ("2xl", 1536)]


_PILL = 10 ** 6   # sentinel px value for "pill" / 9999px radii


def _nearest_name(px: float, table: Sequence[tuple[str, float]]) -> str:
    return min(table, key=lambda kv: abs(px - kv[1]))[0]


def _scale(
    counts: Counter[str], table: Sequence[tuple[str, float]], root_px: float,
    limit: int, full_key: str | None = None,
) -> dict[str, str]:
    """Turn raw values into a named scale, most-used wins on name collision."""
    sized: list[tuple[float, str, int]] = []
    for raw, n in counts.items():
        first = raw.split()[0] if raw.split() else raw
        if full_key and ("9999" in first or first.endswith("%")):
            sized.append((_PILL, raw, n))
            continue
        px = to_px(first, root_px)
        if px is None:
            continue
        sized.append((px, raw, n))
    sized.sort(key=lambda t: -t[2])
    out: dict[str, str] = {}
    for px, raw, _n in sized[: limit * 3]:
        name = full_key if px == _PILL else _nearest_name(px, table)
        if name in out:
            continue
        out[name] = raw
        if len(out) >= limit:
            break
    def sort_key(raw: str) -> float:
        px = to_px(raw.split()[0], root_px)
        return _PILL if px is None else px

    return dict(sorted(out.items(), key=lambda kv: sort_key(kv[1])))


LEADING_NAMES = [
    ("none", 1.0), ("tight", 1.25), ("snug", 1.375), ("normal", 1.5),
    ("relaxed", 1.625), ("loose", 2.0),
]
TRACKING_NAMES = [
    ("tighter", -0.05), ("tight", -0.025), ("normal", 0.0),
    ("wide", 0.025), ("wider", 0.05), ("widest", 0.1),
]


def collect_leading(counts: Counter[str], root_px: float) -> dict[str, str]:
    """line-height, normalised to a unitless ratio for naming."""
    out: dict[str, str] = {}
    for raw, _n in counts.most_common(24):
        raw = raw.strip()
        if raw in ("normal", "inherit"):
            ratio = 1.5
        elif re.fullmatch(rf"{_NUM}", raw):
            ratio = float(raw)
        elif raw.endswith("%"):
            ratio = float(raw[:-1]) / 100
        else:
            px = to_px(raw, root_px)
            ratio = px / root_px if px else None
        if ratio is None or not 0.7 <= ratio <= 3.0:
            continue
        name = min(LEADING_NAMES, key=lambda kv: abs(ratio - kv[1]))[0]
        out.setdefault(name, raw)
    return dict(sorted(out.items(), key=lambda kv: dict(LEADING_NAMES)[kv[0]]))


def collect_tracking(counts: Counter[str], root_px: float) -> dict[str, str]:
    """letter-spacing, normalised to em for naming."""
    out: dict[str, str] = {}
    for raw, _n in counts.most_common(24):
        raw = raw.strip()
        if raw == "normal":
            em = 0.0
        elif raw.endswith("em"):
            em = float(raw[:-2])
        else:
            px = to_px(raw, root_px)
            em = px / root_px if px is not None else None
        if em is None or abs(em) > 0.5:
            continue
        name = min(TRACKING_NAMES, key=lambda kv: abs(em - kv[1]))[0]
        out.setdefault(name, raw)
    return dict(sorted(out.items(), key=lambda kv: dict(TRACKING_NAMES)[kv[0]]))


def collect_breakpoints(medias: Sequence[str], limit: int = 6) -> dict[str, str]:
    """
    Real systems have four to six breakpoints. A raw dump gives you fifteen —
    1024 and 1025 and 1101 — because max-width rules sit one pixel below the
    min-width rule they pair with. Cluster, then keep the ones actually used.
    """
    widths: Counter[int] = Counter()
    for q in medias:
        for m in re.finditer(
            r"(min|max)-width\s*:\s*(\d+(?:\.\d+)?)(px|rem|em)", q, re.I
        ):
            n = float(m.group(2))
            px = n * 16 if m.group(3) in ("rem", "em") else n
            if m.group(1).lower() == "max":
                px += 1                     # max-width: 767px pairs with 768
            if 320 <= px <= 2560:
                widths[int(round(px))] += 1

    clusters: list[list[tuple[int, int]]] = []
    for px in sorted(widths):
        if clusters and px - clusters[-1][-1][0] <= 40:
            clusters[-1].append((px, widths[px]))
        else:
            clusters.append([(px, widths[px])])

    merged = [
        (max(c, key=lambda kv: kv[1])[0], sum(n for _p, n in c)) for c in clusters
    ]
    merged.sort(key=lambda kv: -kv[1])
    keep = sorted(px for px, _n in merged[:limit])

    out: dict[str, str] = {}
    for px in keep:
        name = _nearest_name(px, BREAKPOINT_NAMES)
        if name in out:
            name = f"{name}-{px}"
        out[name] = f"{px}px"
    return out


def classify_font(stack: str) -> str:
    s = stack.lower()
    if "mono" in s or "courier" in s or "consol" in s:
        return "mono"
    head = s.split(",")[0].strip().strip("\"'")
    body = s.replace("sans-serif", "")          # so "sans-serif" never reads as serif
    serif_hint = ("serif" in body) or any(
        w in head for w in ("georgia", "garamond", "playfair", "times", "merriweather",
                            "lora", "baskerville", "cambria", "didot")
    )
    if serif_hint and "sans" not in head:
        return "serif"
    return "sans"


def collect_fonts(counts: Counter[str], faces: Sequence[dict]) -> dict[str, str]:
    out: dict[str, str] = {}
    by_kind: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for stack, n in counts.most_common():
        stack = stack.strip()
        # `font-family: inherit` is the single most common font declaration on
        # the web and says nothing about the design.
        if (
            not stack
            or stack.startswith("var(")
            or stack.lower() in {
                "inherit", "initial", "unset", "revert", "revert-layer",
                "system-ui", "sans-serif", "serif", "monospace", "cursive",
            }
        ):
            continue
        by_kind[classify_font(stack)].append((stack, n))
    for kind in ("sans", "serif", "mono"):
        if by_kind.get(kind):
            out[kind] = by_kind[kind][0][0]
    for kind, items in by_kind.items():
        for i, (stack, _n) in enumerate(items[1:4], 2):
            out[f"{kind}-{i}"] = stack
    families = []
    for face in faces:
        fam = face.get("font-family", "").strip("\"' ")
        if fam and fam not in families:
            families.append(fam)
    if families:
        out["_webfonts"] = ", ".join(families[:12])
    return out


def collect_shadows(
    decls: Sequence[Decl], var_map: dict[str, str]
) -> tuple[dict[str, str], dict[str, str], list[str]]:
    """
    Returns (elevation, rings, suspects).

    Three things the naive version gets wrong:
      · `0 0 0 0 #fff` sorts smallest and wins the `xs` slot — it is a no-op.
      · `inset 0 0 0 1px <c>` is a border drawn as a shadow. It is a ring, not
        elevation, and mixing the two produces an unusable scale.
      · `rgba(255,0,0,.5)` is somebody's debug outline that shipped.
    """
    counts: Counter[str] = Counter()
    for d in decls:
        if d.prop != "box-shadow" and not re.match(
            r"^--(box-)?shadow|^--elevation|^--ring", d.prop
        ):
            continue
        v = re.sub(r"\s+", " ", resolve_vars(d.value, var_map).strip())
        if v.lower() in ("none", "inherit", "initial", "unset") or "var(" in v:
            continue
        counts[v] += 1

    def lengths(v: str) -> list[float]:
        return [to_px(t) or 0.0 for t in length_tokens(v)]

    def is_debug(v: str) -> bool:
        for c in find_colors(v):
            if c.a > 0.2 and c.oklch[1] > 0.22 and max(c.r, c.g, c.b) > 200:
                mx = max(c.r, c.g, c.b)
                if sorted((c.r, c.g, c.b))[1] < mx * 0.35:   # pure R/G/B
                    return True
        return False

    elevation: Counter[str] = Counter()
    rings: Counter[str] = Counter()
    suspects: list[str] = []
    for v, n in counts.items():
        px = lengths(v)
        if not px or all(abs(x) < 0.01 for x in px):
            continue                                    # no-op shadow
        if is_debug(v):
            suspects.append(v)
            continue
        ox, oy = (px + [0.0, 0.0])[:2]
        blur = px[2] if len(px) > 2 else 0.0
        spread = px[3] if len(px) > 3 else 0.0
        ring = (
            (abs(ox) < 0.5 and abs(oy) < 0.5 and abs(blur) < 1.5 and abs(spread) > 0.5)
            or (v.lower().startswith("inset") and abs(blur) < 1.5)
        )
        (rings if ring else elevation)[v] = n           # a border in disguise

    def scale(c: Counter[str], names: Sequence[str]) -> dict[str, str]:
        ranked = sorted(c.items(), key=lambda kv: (sum(abs(x) for x in lengths(kv[0])), -kv[1]))
        return {
            (names[i] if i < len(names) else f"s{i}"): v
            for i, (v, _n) in enumerate(ranked[: len(names)])
        }

    return (
        scale(elevation, ["xs", "sm", "DEFAULT", "md", "lg", "xl", "2xl"]),
        scale(rings, ["ring", "ring-2", "ring-inset", "ring-lg"]),
        suspects,
    )


# ===========================================================================
# 7.  SEMANTIC ROLES
# ===========================================================================


def guess_roles(
    palette: dict[str, Color],
    fg: Counter[Color],
    bg: Counter[Color],
    entries: Sequence[tuple[Color, int]],
) -> dict[str, str]:
    """
    Map extracted colours onto conventional UI roles.

    Background and foreground are chosen as a *pair*: the most-used surface
    colour, then the most-used text colour that actually reads against it.
    Picking them independently is how you end up with white-on-white.
    """
    rev = {c: n for n, c in palette.items()}
    opaque = [(c, n) for c, n in entries if c.a > 0.9]

    def token(c: Color | None) -> str | None:
        if c is None:
            return None
        if c in rev:
            return rev[c]
        if not palette:
            return None
        name, near = min(palette.items(), key=lambda kv: kv[1].distance(c))
        return name if near.distance(c) < 0.08 else None

    roles: dict[str, str] = {}
    if not opaque:
        return roles

    # --- surface -----------------------------------------------------------
    ranked_bg = [c for c, _ in bg.most_common() if c.a > 0.9]
    extremes = [
        c for c, _ in opaque if c.luminance > 0.80 or c.luminance < 0.12
    ]
    bg_pick = (ranked_bg or extremes or [opaque[0][0]])[0]

    # --- ink: most-used text colour that clears AA against the surface ------
    fg_pick = None
    for c, _n in fg.most_common():
        if c.a > 0.9 and c.contrast(bg_pick) >= 4.5:
            fg_pick = c
            break
    if fg_pick is None:
        candidates = [c for c, _ in opaque if c.contrast(bg_pick) >= 4.5]
        fg_pick = candidates[0] if candidates else max(
            (c for c, _ in opaque), key=lambda c: c.contrast(bg_pick)
        )

    roles["background"] = token(bg_pick) or bg_pick.css
    roles["foreground"] = token(fg_pick) or fg_pick.css

    # --- muted text: readable but softer than the ink -----------------------
    muted = [
        c for c, _ in opaque
        if 3.0 <= c.contrast(bg_pick) < fg_pick.contrast(bg_pick) - 1
        and c.on_white().oklch[1] < 0.06          # chromatic == brand, not body copy
    ]
    if muted:
        roles["muted-foreground"] = token(muted[0]) or muted[0].css

    # --- brand: most-used chromatic colour with enough presence -------------
    accents = [
        c for c, _n in opaque
        if c.on_white().oklch[1] > 0.06
        and c.contrast(bg_pick) >= 1.6
        and c not in (bg_pick, fg_pick)
    ]
    if accents:
        roles["primary"] = token(accents[0]) or accents[0].css
        for c in accents[1:]:
            if c.distance(accents[0]) > 0.15:
                roles["accent"] = token(c) or c.css
                break

    # --- hairlines: low contrast against the surface ------------------------
    borders = [
        c for c, _ in opaque
        if 1.05 < c.contrast(bg_pick) < 2.2 and c.on_white().oklch[1] < 0.09
    ]
    if borders:
        roles["border"] = token(borders[0]) or borders[0].css

    # --- status colours by hue ---------------------------------------------
    def by_hue(target: float, span: float = 26) -> str | None:
        for c, _n in opaque:
            L, C, H = c.on_white().oklch
            if C < 0.09 or not (0.25 < L < 0.85):
                continue
            if min(abs(H - target), 360 - abs(H - target)) < span:
                return token(c) or c.css
        return None

    for role, hue in (
        ("destructive", 29), ("warning", 71), ("success", 150), ("info", 232)
    ):
        t = by_hue(hue)
        if t:
            roles[role] = t
    return roles


def ambiguous_vars(decls: Iterable[Decl]) -> set[str]:
    """
    Custom properties redeclared with different values across components.
    `--bs-btn-hover-bg` has one value per button variant, so resolving it
    statically pairs one variant's text with another's surface and invents
    contrast failures that nobody can see.
    """
    values: dict[str, set[str]] = defaultdict(set)
    for d in decls:
        if d.prop.startswith("--") and not d.dark:
            values[d.prop].add(d.value.strip())
    return {k for k, v in values.items() if len(v) > 1}


def collect_pairs(
    decls: Sequence[Decl], var_map: dict[str, str], ambiguous: set[str] | None = None
) -> list[tuple[str, Color, Color]]:
    """
    Foreground/background colours declared on the same selector — the pairs a
    user actually sees. A cartesian product of every colour against every other
    produces forty rows of `black on white — 21:1 ✓` and hides the two pairs
    that fail.
    """
    fg_by_sel: dict[str, Color] = {}
    bg_by_sel: dict[str, Color] = {}
    ambiguous = ambiguous or set()
    for d in decls:
        if d.prop not in FG_PROPS | BG_PROPS:
            continue
        if any(v in ambiguous for v in VAR_REF_RE.findall(d.value)):
            continue
        found = find_colors(resolve_vars(d.value, var_map))
        if len(found) != 1 or found[0].a < 0.9:
            continue
        (fg_by_sel if d.prop in FG_PROPS else bg_by_sel)[d.selector] = found[0]

    pairs: list[tuple[str, Color, Color]] = []
    seen: set[tuple[Color, Color]] = set()
    for sel, fg in fg_by_sel.items():
        bg = bg_by_sel.get(sel)
        if bg is None or (fg, bg) in seen or fg == bg:
            continue
        seen.add((fg, bg))
        pairs.append((sel, fg, bg))
    return pairs


def contrast_report(palette: dict[str, Color], limit: int = 6) -> list[dict]:
    lights = sorted(
        ((n, c) for n, c in palette.items() if c.on_white().luminance > 0.5),
        key=lambda kv: -kv[1].luminance,
    )[:limit]
    darks = sorted(
        ((n, c) for n, c in palette.items() if c.on_white().luminance <= 0.5),
        key=lambda kv: kv[1].luminance,
    )[:limit]
    rows = []
    for bn, bc in lights:
        for fn, fc in darks:
            ratio = bc.on_white().contrast(fc.on_white())
            rows.append(
                {
                    "background": bn, "background_hex": bc.hex,
                    "foreground": fn, "foreground_hex": fc.hex,
                    "ratio": round(ratio, 2),
                    "aa_normal": ratio >= 4.5,
                    "aa_large": ratio >= 3.0,
                    "aaa_normal": ratio >= 7.0,
                }
            )
    rows.sort(key=lambda r: -r["ratio"])
    return rows[:40]


# ===========================================================================
# 8.  EMITTERS
# ===========================================================================


def build_audit(
    palette: dict[str, Color],
    overlays: dict[str, Color],
    off_grid: Sequence[tuple[float, int]],
    grid: float,
    contrast: Sequence[dict],
    shadow_suspects: Sequence[str],
    fonts: dict[str, str],
    breakpoint_count: int,
    raw_breakpoints: int,
) -> list[dict]:
    """
    Extraction is table stakes. The useful output is the diff between the
    system a team thinks they have and the CSS they actually shipped.
    """
    issues: list[dict] = []

    fails = [c for c in contrast if not c["aa_normal"]]
    if fails:
        issues.append({
            "severity": "high",
            "title": f"{len(fails)} colour pair(s) below WCAG AA",
            "detail": ", ".join(
                f"{c['foreground']} on {c['background']} ({c['ratio']}:1)"
                for c in fails[:6]
            ),
            "action": "Darken the foreground or lighten the surface to clear 4.5:1.",
        })

    near = []
    items = list(palette.items())
    for i, (n1, c1) in enumerate(items):
        for n2, c2 in items[i + 1:]:
            d = c1.distance(c2)
            if d < 0.045:
                near.append(f"{n1} {c1.hex} ≈ {n2} {c2.hex}")
    if near:
        issues.append({
            "severity": "medium",
            "title": f"{len(near)} near-duplicate colour pair(s)",
            "detail": "; ".join(near[:8]),
            "action": "Collapse to one token. Nobody can tell these apart on a screen.",
        })

    if off_grid:
        total_off = sum(n for _px, n in off_grid)
        issues.append({
            "severity": "medium",
            "title": f"{len(off_grid)} spacing values off the {grid:g}px grid "
                     f"({total_off} uses)",
            "detail": ", ".join(f"{px:g}px×{n}" for px, n in off_grid[:12]),
            "action": f"Snap to the nearest multiple of {grid:g}px, or promote the "
                      f"recurring ones into real tokens.",
        })

    if raw_breakpoints > breakpoint_count:
        issues.append({
            "severity": "medium",
            "title": f"{raw_breakpoints} distinct media-query widths, "
                     f"{breakpoint_count} kept",
            "detail": "Off-by-one widths usually mean min-width and max-width "
                      "rules were written against different values.",
            "action": "Standardise on min-width only and one shared width list.",
        })

    if shadow_suspects:
        issues.append({
            "severity": "high",
            "title": "Debug styling in production CSS",
            "detail": "; ".join(shadow_suspects[:4]),
            "action": "A saturated primary-channel shadow is almost always a "
                      "leftover outline. Remove it.",
        })

    stacks = [v for k, v in fonts.items() if not k.startswith("_")]
    norm = [re.sub(r"[\"'\s]", "", v).lower() for v in stacks]
    if len(norm) != len(set(norm)):
        issues.append({
            "severity": "low",
            "title": "Duplicate font stacks differing only in quoting",
            "detail": "; ".join(stacks[:4]),
            "action": "Normalise quoting and declare the stack once as a token.",
        })

    if len(overlays) > 8:
        issues.append({
            "severity": "low",
            "title": f"{len(overlays)} one-off overlay tints",
            "detail": ", ".join(list(overlays)[:10]),
            "action": "Reduce to a 3-4 step scrim scale "
                      "(--overlay-subtle / -medium / -strong).",
        })

    order = {"high": 0, "medium": 1, "low": 2}
    issues.sort(key=lambda i: order[i["severity"]])
    return issues


def emit_theme_css(tokens: dict, source: str) -> str:
    L: list[str] = [
        "/* ---------------------------------------------------------------",
        f"   Design tokens extracted from {source}",
        f"   extract-theme v{__version__}",
        "   --------------------------------------------------------------- */",
        "",
        ":root {",
        "  /* palette */",
    ]
    for name, hexv in tokens["colors"].items():
        L.append(f"  --color-{name}: {hexv};")

    if tokens["roles"]:
        L += ["", "  /* semantic roles */"]
        for role, ref in tokens["roles"].items():
            ref_css = f"var(--color-{ref})" if ref in tokens["colors"] else ref
            L.append(f"  --{role}: {ref_css};")

    if tokens["overlays"]:
        L += ["", "  /* overlays and scrims */"]
        for name, css in tokens["overlays"].items():
            L.append(f"  --overlay-{name}: {css};")

    if tokens["fonts"]:
        L += ["", "  /* typography */"]
        for k, v in tokens["fonts"].items():
            if k.startswith("_"):
                continue
            L.append(f"  --font-{k}: {v};")
    for k, v in tokens["font_sizes"].items():
        L.append(f"  --text-{k}: {v};")
    for k, v in tokens["font_weights"].items():
        L.append(f"  --weight-{k}: {v};")
    for k, v in tokens["line_heights"].items():
        L.append(f"  --leading-{k}: {v};")
    for k, v in tokens["letter_spacing"].items():
        L.append(f"  --tracking-{k}: {v};")

    if tokens["spacing"]:
        L += ["", "  /* spacing */"]
        for k, v in tokens["spacing"].items():
            L.append(f"  --space-{k}: {v};")

    if tokens["radius"]:
        L += ["", "  /* radius */"]
        for k, v in tokens["radius"].items():
            key = "radius" if k == "DEFAULT" else f"radius-{k}"
            L.append(f"  --{key}: {v};")

    if tokens["shadows"]:
        L += ["", "  /* elevation */"]
        for k, v in tokens["shadows"].items():
            key = "shadow" if k == "DEFAULT" else f"shadow-{k}"
            L.append(f"  --{key}: {v};")

    if tokens["rings"]:
        L += ["", "  /* rings — inset shadows used as borders */"]
        for k, v in tokens["rings"].items():
            L.append(f"  --{k}: {v};")

    L.append("}")

    if tokens["dark_vars"]:
        L += [
            "",
            "/* Dark scope, as declared by the source site */",
            "@media (prefers-color-scheme: dark) {",
            "  :root {",
        ]
        for k, v in tokens["dark_vars"].items():
            L.append(f"    {k}: {v};")
        L += ["  }", "}", "", '[data-theme="dark"], .dark {']
        for k, v in tokens["dark_vars"].items():
            L.append(f"  {k}: {v};")
        L.append("}")

    if tokens["breakpoints"]:
        L += ["", "/* Breakpoints (custom media — needs postcss-custom-media) */"]
        for k, v in tokens["breakpoints"].items():
            L.append(f"@custom-media --{k} (min-width: {v});")

    return "\n".join(L) + "\n"


COMPONENTS_TEMPLATE = """
/* ---------------------------------------------------------------
   Component primitives built on ./theme.css
   Every value here is a token reference — nothing is hard-coded.
   --------------------------------------------------------------- */

*, *::before, *::after { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--background);
  color: var(--foreground);
  font-family: var(--font-sans, system-ui, sans-serif);
  font-size: var(--text-base, 1rem);
  -webkit-font-smoothing: antialiased;
}

:focus-visible {
  outline: 2px solid var(--primary, currentColor);
  outline-offset: 2px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2, .5rem);
  padding: var(--space-3, .75rem) var(--space-4, 1rem);
  border: 1px solid transparent;
  border-radius: var(--radius, .5rem);
  font: inherit;
  font-weight: var(--weight-medium, 500);
  line-height: 1;
  cursor: pointer;
  transition: background-color .15s ease, border-color .15s ease;
}

.btn--primary {
  background: var(--primary);
  color: var(--background);
}
.btn--primary:hover { filter: brightness(1.08); }

.btn--ghost {
  background: transparent;
  border-color: var(--border, currentColor);
  color: var(--foreground);
}
.btn--ghost:hover { background: color-mix(in oklab, var(--foreground) 6%, transparent); }

.btn[disabled] { opacity: .5; cursor: not-allowed; }

.card {
  background: var(--background);
  border: 1px solid var(--border, currentColor);
  border-radius: var(--radius-lg, .75rem);
  box-shadow: var(--shadow-sm, none);
  padding: var(--space-6, 1.5rem);
}

.input {
  width: 100%;
  padding: var(--space-3, .75rem) var(--space-4, 1rem);
  background: var(--background);
  color: var(--foreground);
  border: 1px solid var(--border, currentColor);
  border-radius: var(--radius, .5rem);
  font: inherit;
}
.input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px color-mix(in oklab, var(--primary) 25%, transparent);
}
.input::placeholder { opacity: .55; }

.badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1, .25rem);
  padding: 0 var(--space-2, .5rem);
  border-radius: var(--radius-full, 9999px);
  font-size: var(--text-xs, .75rem);
  font-weight: var(--weight-medium, 500);
  line-height: 1.6;
}
.badge--success { background: color-mix(in oklab, var(--success, green) 15%, transparent); color: var(--success, green); }
.badge--warning { background: color-mix(in oklab, var(--warning, orange) 15%, transparent); color: var(--warning, orange); }
.badge--danger  { background: color-mix(in oklab, var(--destructive, red) 15%, transparent); color: var(--destructive, red); }
"""


def emit_tailwind_v4(tokens: dict, source: str) -> str:
    L = [
        f"/* Tailwind v4 theme extracted from {source} */",
        '@import "tailwindcss";',
        "",
        "@theme {",
    ]
    for name, hexv in tokens["colors"].items():
        L.append(f"  --color-{name}: {hexv};")
    L.append("")
    for role, ref in tokens["roles"].items():
        ref_css = f"var(--color-{ref})" if ref in tokens["colors"] else ref
        L.append(f"  --color-{role}: {ref_css};")
    L.append("")
    for k, v in tokens["fonts"].items():
        if not k.startswith("_"):
            L.append(f"  --font-{k}: {v};")
    L.append("")
    for k, v in tokens["font_sizes"].items():
        L.append(f"  --text-{k}: {v};")
    for k, v in tokens["line_heights"].items():
        L.append(f"  --leading-{k}: {v};")
    for k, v in tokens["letter_spacing"].items():
        L.append(f"  --tracking-{k}: {v};")
    L.append("")
    for k, v in tokens["spacing"].items():
        L.append(f"  --spacing-{k}: {v};")
    L.append("")
    for k, v in tokens["radius"].items():
        L.append(f"  --radius{'' if k == 'DEFAULT' else '-' + k}: {v};")
    L.append("")
    for k, v in tokens["shadows"].items():
        L.append(f"  --shadow{'' if k == 'DEFAULT' else '-' + k}: {v};")
    L.append("")
    for k, v in tokens["breakpoints"].items():
        L.append(f"  --breakpoint-{k}: {v};")
    L.append("}")
    return "\n".join(L) + "\n"


def emit_tailwind_v3(tokens: dict, source: str) -> str:
    colors: dict[str, object] = {}
    grouped: dict[str, dict[str, str]] = defaultdict(dict)
    for name, hexv in tokens["colors"].items():
        if "-" in name and name.rsplit("-", 1)[1].isdigit():
            fam, step = name.rsplit("-", 1)
            grouped[fam][step] = hexv
        else:
            colors[name] = hexv
    colors.update(grouped)
    for role, ref in tokens["roles"].items():
        colors[role] = tokens["colors"].get(ref, ref)

    def split_stack(stack: str) -> list[str]:
        return [p.strip().strip("\"'") for p in stack.split(",") if p.strip()]

    config = {
        "content": ["./src/**/*.{js,ts,jsx,tsx,html}"],
        "theme": {
            "extend": {
                "colors": colors,
                "fontFamily": {
                    k: split_stack(v)
                    for k, v in tokens["fonts"].items() if not k.startswith("_")
                },
                "fontSize": tokens["font_sizes"],
                "fontWeight": tokens["font_weights"],
                "lineHeight": tokens["line_heights"],
                "letterSpacing": tokens["letter_spacing"],
                "spacing": tokens["spacing"],
                "borderRadius": tokens["radius"],
                "boxShadow": tokens["shadows"],
                "screens": tokens["breakpoints"],
            }
        },
        "plugins": [],
    }
    return (
        f"/* Tailwind v3 config extracted from {source} */\n"
        "/** @type {import('tailwindcss').Config} */\n"
        "module.exports = " + json.dumps(config, indent=2) + ";\n"
    )


GUIDE_CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#f7f8fa;--panel:#fff;--line:#e5e7eb;--tx:#0f172a;--tx2:#64748b;--acc:#4f46e5;
}
html[data-t="dark"]{--bg:#0b0f17;--panel:#131a26;--line:#242e3f;--tx:#e8edf5;--tx2:#8b98ad;--acc:#8b7cf8}
body{margin:0;background:var(--bg);color:var(--tx);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1140px;margin:0 auto;padding:48px 24px 96px}
header{display:flex;align-items:flex-start;gap:24px;flex-wrap:wrap;margin-bottom:8px}
h1{font-size:34px;letter-spacing:-.025em;margin:0 0 4px}
h2{font-size:13px;text-transform:uppercase;letter-spacing:.1em;color:var(--tx2);margin:56px 0 14px;font-weight:600}
.sub{color:var(--tx2);font-size:14px;margin:0}
.sub a{color:var(--acc)}
.toggle{margin-left:auto;background:var(--panel);border:1px solid var(--line);color:var(--tx);
  border-radius:8px;padding:8px 14px;font:inherit;font-size:13px;cursor:pointer}
.stats{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;font-size:13px}
.stat b{display:block;font-size:20px;letter-spacing:-.02em}
.stat span{color:var(--tx2)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:12px}
.sw{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden;cursor:pointer;text-align:left;padding:0;font:inherit;color:inherit;width:100%}
.sw .chip{height:78px;background-image:linear-gradient(45deg,#0001 25%,transparent 25%,transparent 75%,#0001 75%),linear-gradient(45deg,#0001 25%,transparent 25%,transparent 75%,#0001 75%);background-size:14px 14px;background-position:0 0,7px 7px}
.sw .chip i{display:block;height:100%}
.sw .meta{padding:10px 12px;display:flex;flex-direction:column;gap:2px}
.sw code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px}
.sw .n{font-weight:600;font-size:13px}
.sw .u{color:var(--tx2);font-size:12px}
table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:13.5px}
th,td{padding:10px 14px;text-align:left;border-bottom:1px solid var(--line);vertical-align:middle}
tr:last-child td{border-bottom:0}
th{background:color-mix(in oklab,var(--tx) 4%,transparent);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--tx2)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
td code{font-size:12.5px}
.pill{display:inline-block;padding:1px 8px;border-radius:99px;font-size:11px;font-weight:600}
.ok{background:#16a34a22;color:#16a34a}.no{background:#dc262622;color:#ef4444}
.spec{display:flex;align-items:baseline;gap:16px;padding:10px 14px;border-bottom:1px solid var(--line)}
.spec:last-child{border-bottom:0}
.spec .k{width:110px;flex:none;color:var(--tx2);font-size:12px;font-family:ui-monospace,monospace}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}
.bar{background:var(--acc);height:14px;border-radius:3px}
.shadow-demo{height:64px;width:110px;border-radius:10px;background:var(--panel);border:1px solid var(--line)}
.rad-demo{height:56px;width:56px;background:var(--acc);opacity:.85}
.copy{position:fixed;left:50%;bottom:28px;transform:translate(-50%,80px);background:var(--tx);color:var(--bg);
  padding:9px 18px;border-radius:99px;font-size:13px;transition:transform .18s ease;pointer-events:none}
.copy.on{transform:translate(-50%,0)}
.note{color:var(--tx2);font-size:12.5px;margin:8px 0 0}
.iss{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--sev);
  border-radius:10px;padding:14px 16px;margin-bottom:10px}
.iss.high{--sev:#dc2626}.iss.medium{--sev:#d97706}.iss.low{--sev:#64748b}
.iss h3{margin:0 0 4px;font-size:14px;display:flex;align-items:center;gap:9px}
.iss .tag{font-size:10px;text-transform:uppercase;letter-spacing:.08em;font-weight:700;
  color:var(--sev);border:1px solid var(--sev);border-radius:99px;padding:0 7px}
.iss p{margin:2px 0 0;font-size:13px;color:var(--tx2)}
.iss .fix{color:var(--tx);margin-top:7px;font-size:13px}
.clean{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px;font-size:13.5px}
"""

GUIDE_JS = """
document.querySelectorAll('[data-copy]').forEach(function(el){
  el.addEventListener('click', function(){
    navigator.clipboard.writeText(el.dataset.copy);
    var t=document.getElementById('toast');
    t.textContent='Copied '+el.dataset.copy; t.classList.add('on');
    clearTimeout(window.__t); window.__t=setTimeout(function(){t.classList.remove('on')},1400);
  });
});
document.getElementById('theme').addEventListener('click', function(){
  var h=document.documentElement;
  h.dataset.t = h.dataset.t==='dark' ? 'light' : 'dark';
});
"""


def _esc(v) -> str:
    return (
        str(v).replace("&", "&amp;").replace("<", "&lt;")
        .replace(">", "&gt;").replace('"', "&quot;")
    )


def emit_style_guide(tokens: dict, source: str, stats: dict) -> str:
    def rows(d: dict, render=None) -> str:
        out = []
        for k, v in d.items():
            demo = render(k, v) if render else ""
            out.append(
                f"<tr><td><code>{_esc(k)}</code></td>"
                f"<td><code>{_esc(v)}</code></td>{demo}</tr>"
            )
        return "".join(out) or '<tr><td colspan="3" class="note">none found</td></tr>'

    swatches = []
    for name, hexv in tokens["colors"].items():
        uses = tokens["_color_uses"].get(name, 0)
        swatches.append(
            f'<button class="sw" data-copy="{_esc(hexv)}">'
            f'<div class="chip"><i style="background:{_esc(hexv)}"></i></div>'
            f'<div class="meta"><span class="n">{_esc(name)}</span>'
            f'<code>{_esc(hexv)}</code>'
            f'<span class="u">{uses} uses</span></div></button>'
        )

    role_rows = "".join(
        f"<tr><td><code>--{_esc(r)}</code></td><td><code>{_esc(v)}</code></td>"
        f'<td><span style="display:inline-block;width:34px;height:18px;border-radius:5px;'
        f'border:1px solid var(--line);background:{_esc(tokens["colors"].get(v, v))}"></span></td></tr>'
        for r, v in tokens["roles"].items()
    ) or '<tr><td colspan="3" class="note">no roles inferred</td></tr>'

    contrast_rows = "".join(
        f"<tr><td><code>{_esc(r['foreground'])}</code> on <code>{_esc(r['background'])}</code>"
        + (f"<br><span class='u' style='font-size:11px;color:var(--tx2)'>"
           f"{_esc(r['selector'])}</span>" if r.get("selector") else "")
        + "</td>"
        f"<td><b>{r['ratio']}</b>:1</td>"
        f"<td><span class='pill {'ok' if r['aa_normal'] else 'no'}'>"
        f"{'AA' if r['aa_normal'] else 'fail'}</span> "
        f"<span class='pill {'ok' if r['aaa_normal'] else 'no'}'>"
        f"{'AAA' if r['aaa_normal'] else '—'}</span></td>"
        f"<td style=\"background:{_esc(r['background_hex'])};color:{_esc(r['foreground_hex'])};"
        f"border-radius:6px\">The quick brown fox</td></tr>"
        for r in tokens["contrast"][:14]
    ) or '<tr><td colspan="4" class="note">not enough colours</td></tr>'

    type_rows = "".join(
        f'<tr><td><code>{_esc(k)}</code></td><td><code>{_esc(v)}</code></td>'
        f'<td style="font-size:{_esc(v)};line-height:1.2">Ag</td></tr>'
        for k, v in tokens["font_sizes"].items()
    ) or '<tr><td colspan="3" class="note">none found</td></tr>'

    font_rows = "".join(
        f'<div class="spec"><span class="k">{_esc(k)}</span>'
        f'<span style="font-family:{_esc(v)};font-size:19px">Design systems, extracted.</span></div>'
        f'<div class="spec"><span class="k"></span><code style="font-size:12px;color:var(--tx2)">{_esc(v)}</code></div>'
        for k, v in tokens["fonts"].items() if not k.startswith("_")
    ) or '<p class="note">none found</p>'

    space_rows = "".join(
        f'<tr><td><code>{_esc(k)}</code></td><td><code>{_esc(v)}</code></td>'
        f'<td><div class="bar" style="width:{_esc(v)}"></div></td></tr>'
        for k, v in tokens["spacing"].items()
    ) or '<tr><td colspan="3" class="note">none found</td></tr>'

    radius_rows = rows(
        tokens["radius"],
        lambda k, v: f'<td><div class="rad-demo" style="border-radius:{_esc(v)}"></div></td>',
    )
    shadow_rows = rows(
        tokens["shadows"],
        lambda k, v: f'<td><div class="shadow-demo" style="box-shadow:{_esc(v)}"></div></td>',
    )

    leading_rows = "".join(
        f'<tr><td><code>leading-{_esc(k)}</code></td><td><code>{_esc(v)}</code></td>'
        f'<td style="line-height:{_esc(v)};max-width:340px">Type set at this leading, '
        f'wrapped over two lines so the rhythm is visible.</td></tr>'
        for k, v in tokens["line_heights"].items()
    ) + "".join(
        f'<tr><td><code>tracking-{_esc(k)}</code></td><td><code>{_esc(v)}</code></td>'
        f'<td style="letter-spacing:{_esc(v)}">Letter spacing sample</td></tr>'
        for k, v in tokens["letter_spacing"].items()
    ) or '<tr><td colspan="3" class="note">none found</td></tr>'

    bp_rows = rows(tokens["breakpoints"])
    weight_rows = rows(
        tokens["font_weights"],
        lambda k, v: f'<td style="font-weight:{_esc(v)};font-size:16px">Weight</td>',
    )

    webfonts = tokens["fonts"].get("_webfonts")
    webfont_html = (
        f'<p class="note">@font-face families declared: <code>{_esc(webfonts)}</code></p>'
        if webfonts else ""
    )

    audit_html = "".join(
        f'<div class="iss {_esc(i["severity"])}">'
        f'<h3><span class="tag">{_esc(i["severity"])}</span>{_esc(i["title"])}</h3>'
        f'<p>{_esc(i["detail"])}</p>'
        f'<p class="fix">→ {_esc(i["action"])}</p></div>'
        for i in tokens["audit"]
    ) or '<div class="clean">No issues found. The palette is internally '\
         'consistent, spacing sits on the grid, and every declared colour '\
         'pair clears WCAG AA.</div>'

    overlay_html = "".join(
        f'<button class="sw" data-copy="{_esc(v)}">'
        f'<div class="chip"><i style="background:{_esc(v)}"></i></div>'
        f'<div class="meta"><span class="n">{_esc(k)}</span>'
        f'<code>{_esc(v)}</code></div></button>'
        for k, v in tokens["overlays"].items()
    ) or '<p class="note">none found</p>'

    ring_rows = rows(tokens["rings"])

    stat_html = "".join(
        f'<div class="stat"><b>{v}</b><span>{_esc(k)}</span></div>'
        for k, v in stats.items()
    )

    return f"""<!DOCTYPE html>
<html lang="en" data-t="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Design system — {_esc(urlparse(source).netloc or source)}</title>
<style>{GUIDE_CSS}</style>
</head>
<body>
<div class="wrap">

<header>
  <div>
    <h1>Design system</h1>
    <p class="sub">Extracted from <a href="{_esc(source)}">{_esc(source)}</a> ·
       {_esc(time.strftime('%d %b %Y'))} · extract-theme v{__version__}</p>
  </div>
  <button class="toggle" id="theme">Toggle theme</button>
</header>

<div class="stats">{stat_html}</div>

<h2>Audit</h2>
{audit_html}

<h2>Palette <span style="text-transform:none;letter-spacing:0;font-weight:400">— click to copy</span></h2>
<div class="grid">{"".join(swatches)}</div>

<h2>Semantic roles</h2>
<table><thead><tr><th>Role</th><th>Token</th><th></th></tr></thead>
<tbody>{role_rows}</tbody></table>
<p class="note">Inferred from usage frequency and hue. Verify before shipping.</p>

<h2>Contrast (WCAG 2.1)</h2>
<table><thead><tr><th>Pair</th><th>Ratio</th><th>Rating</th><th>Preview</th></tr></thead>
<tbody>{contrast_rows}</tbody></table>

<h2>Font families</h2>
<div class="panel">{font_rows}</div>
{webfont_html}

<h2>Type scale</h2>
<table><thead><tr><th>Token</th><th>Value</th><th>Sample</th></tr></thead>
<tbody>{type_rows}</tbody></table>

<h2>Font weights</h2>
<table><thead><tr><th>Token</th><th>Value</th><th>Sample</th></tr></thead>
<tbody>{weight_rows}</tbody></table>

<h2>Leading and tracking</h2>
<table><thead><tr><th>Token</th><th>Value</th><th>Sample</th></tr></thead>
<tbody>{leading_rows}</tbody></table>

<h2>Spacing scale</h2>
<table><thead><tr><th>Token</th><th>Value</th><th>Scale</th></tr></thead>
<tbody>{space_rows}</tbody></table>

<h2>Radius</h2>
<table><thead><tr><th>Token</th><th>Value</th><th>Preview</th></tr></thead>
<tbody>{radius_rows}</tbody></table>

<h2>Overlays and scrims</h2>
<div class="grid">{overlay_html}</div>

<h2>Elevation</h2>
<table><thead><tr><th>Token</th><th>Value</th><th>Preview</th></tr></thead>
<tbody>{shadow_rows}</tbody></table>

<h2>Rings <span style="text-transform:none;letter-spacing:0;font-weight:400">— inset shadows doing a border's job</span></h2>
<table><thead><tr><th>Token</th><th>Value</th></tr></thead>
<tbody>{ring_rows}</tbody></table>

<h2>Breakpoints</h2>
<table><thead><tr><th>Token</th><th>Min width</th></tr></thead>
<tbody>{bp_rows}</tbody></table>

</div>
<div class="copy" id="toast"></div>
<script>{GUIDE_JS}</script>
</body>
</html>
"""


# ===========================================================================
# 9.  PIPELINE
# ===========================================================================


def crawl(fetcher: Fetcher, seeds: Sequence[str], limit: int) -> list[tuple[str, str]]:
    """Fetch the seed pages, then up to `limit` extra same-site pages."""
    pages: list[tuple[str, str]] = []
    queue: list[str] = []
    seen: set[str] = set()

    for seed in seeds:
        try:
            final, html = fetcher.get(seed)
        except Exception as exc:  # noqa: BLE001
            warn(f"{seed} — {type(exc).__name__}: {exc}")
            continue
        seen.add(final)
        pages.append((final, html))
        log(f"  · {final}", 1)
        if limit:
            _, _, _, links = discover(final, html)
            queue.extend(links)

    extra = 0
    for url in queue:
        if extra >= limit:
            break
        if url in seen or url.rsplit(".", 1)[-1].lower() in {
            "pdf", "jpg", "png", "zip", "svg", "webp", "mp4", "gz"
        }:
            continue
        seen.add(url)
        try:
            final, html = fetcher.get(url)
        except Exception:  # noqa: BLE001
            continue
        pages.append((final, html))
        extra += 1
        log(f"  · {final}", 1)
    return pages


def run(args: argparse.Namespace) -> int:
    out = Path(args.out).expanduser()
    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    fetcher = Fetcher(args.timeout, args.workers, args.user_agent, not args.insecure)

    log("\n▸ Fetching pages")
    pages = crawl(fetcher, args.urls, args.crawl)
    if not pages:
        log("Nothing fetched. Check the URL.")
        return 1
    primary = pages[0][0]

    log("\n▸ Discovering stylesheets")
    css_urls: list[str] = []
    inline_assets: list[Asset] = []
    for page_url, html in pages:
        ext, inline, _fonts, _links = discover(page_url, html)
        css_urls.extend(ext)
        inline_assets.extend(inline)
    css_urls = list(dict.fromkeys(css_urls))
    log(f"  {len(css_urls)} external · {len(inline_assets)} inline")

    log("\n▸ Downloading")
    assets: list[Asset] = []
    hashes: set[str] = set()
    for _req, final, text in fetcher.get_many(css_urls):
        h = hashlib.sha1(text.encode("utf-8", "replace")).hexdigest()
        if h in hashes:
            continue
        hashes.add(h)
        assets.append(Asset(url=final, text=text))
    assets.extend(inline_assets)
    log(f"  {len(assets)} unique stylesheets")

    log("\n▸ Resolving @import and url()")
    # pre-seed with sheets we already have, so a stylesheet that is both
    # <link>ed and @imported is not counted twice
    seen_imports: set[str] = {a.url.split("#")[0] for a in assets}
    combined: list[str] = []
    n = 0
    for asset in assets:
        base = asset.url.split("#")[0]
        css = absolutise_urls(asset.text, base)
        css = resolve_imports(fetcher, base, css, seen_imports)
        asset.text = css
        if asset.kind == "external":
            n += 1
            path = raw_dir / f"sheet-{n:03d}.css"
            path.write_text(css, encoding="utf-8")
            asset.file = str(path)
        combined.append(
            f"/* ===== {asset.url} ===== */\n{css}"
        )
    combined_css = "\n\n".join(combined)
    (raw_dir / "combined.css").write_text(combined_css, encoding="utf-8")
    log(f"  {len(combined_css):,} bytes of CSS")

    log("\n▸ Parsing")
    all_decls: list[Decl] = []
    all_media: list[str] = []
    all_faces: list[dict] = []
    for asset in assets:
        try:
            d, m, f = parse_css(asset.text, asset.url)
        except Exception as exc:  # noqa: BLE001
            warn(f"parse failed for {asset.url}: {type(exc).__name__}")
            continue
        all_decls.extend(d)
        all_media.extend(m)
        all_faces.extend(f)
    log(f"  {len(all_decls):,} declarations · {len(all_media)} media queries")

    light_vars, dark_vars = build_var_map(all_decls)

    log("\n▸ Extracting tokens")
    entries, fg, bg = collect_colors(all_decls, light_vars, args.color_tolerance)
    # alpha-0 values are gradient/transition endpoints, never design tokens
    entries = [
        (c, n) for c, n in entries if n >= args.min_count and c.a >= 0.04
    ][: args.max_colors]
    palette = name_palette(entries)
    overlays = {n: c for n, c in palette.items() if c.is_overlay}
    palette = {n: c for n, c in palette.items() if not c.is_overlay}
    color_uses = {
        name: next((n for c, n in entries if c == color), 0)
        for name, color in palette.items()
    }

    font_counts = collect_property(
        all_decls, ["font-family"], r"font-family|font-sans|font-serif|font-mono|typeface"
    )
    fonts = collect_fonts(font_counts, all_faces)

    font_sizes = _scale(
        collect_property(all_decls, ["font-size"], r"font-size|text-|--fs-"),
        TEXT_SIZE_NAMES,
        args.root_font_size, 13,
    )
    radius = _scale(
        collect_property(all_decls, ["border-radius"], r"radius|rounded"),
        RADIUS_NAMES,
        args.root_font_size, 9, full_key="full",
    )

    weights_raw = collect_property(all_decls, ["font-weight"], r"weight")
    weight_names = {
        "100": "thin", "200": "extralight", "300": "light", "400": "normal",
        "500": "medium", "600": "semibold", "700": "bold", "800": "extrabold",
        "900": "black", "normal": "normal", "bold": "bold",
    }
    font_weights: dict[str, str] = {}
    for v, _n in weights_raw.most_common(9):
        key = weight_names.get(v.strip().lower())
        if key and key not in font_weights:
            font_weights[key] = v.strip()

    space_counts = collect_spacing(all_decls, args.root_font_size)
    grid = detect_grid(space_counts)
    on_grid = {px: n for px, n in space_counts.items() if px % grid == 0}
    off_grid = sorted(
        ((px, n) for px, n in space_counts.items() if px % grid != 0),
        key=lambda kv: -kv[1],
    )
    spacing: dict[str, str] = {}
    for px, _n in sorted(
        Counter(on_grid).most_common(args.max_spacing), key=lambda kv: kv[0]
    ):
        # Tailwind's scale is 1 unit = 4px; keeping that mapping means p-4 still
        # means 1rem after you drop the generated config in.
        key = f"{px / 4:g}" if px % 4 == 0 else f"{px:g}px".replace(".", "_")
        spacing[key] = f"{px:g}px"

    elevation, rings, shadow_suspects = collect_shadows(all_decls, light_vars)
    raw_widths = len({
        m.group(0) for q in all_media
        for m in re.finditer(r"\d+(?:\.\d+)?(?:px|rem|em)", q)
    })
    breakpoints = collect_breakpoints(all_media)

    tokens = {
        "source": primary,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "generator": f"extract-theme {__version__}",
        "colors": {name: c.css for name, c in palette.items()},
        "color_rgb_channels": {name: c.rgb_channels for name, c in palette.items()},
        "roles": guess_roles(palette, fg, bg, entries),
        "fonts": fonts,
        "font_sizes": font_sizes,
        "font_weights": font_weights,
        "line_heights": collect_leading(
            collect_property(all_decls, ["line-height"], r"leading|line-height"),
            args.root_font_size,
        ),
        "letter_spacing": collect_tracking(
            collect_property(all_decls, ["letter-spacing"], r"tracking|letter-spacing"),
            args.root_font_size,
        ),
        "spacing": spacing,
        "radius": radius,
        "shadows": elevation,
        "rings": rings,
        "overlays": {n: c.css for n, c in overlays.items()},
        "breakpoints": breakpoints,
        "spacing_grid": f"{grid:g}px",
        "off_grid_spacing": {f"{px:g}px": n for px, n in off_grid},
        "dark_vars": dark_vars,
        "source_variables": light_vars,
        "contrast": [],
        "_color_uses": color_uses,
        "_overlay_objs": overlays,
    }
    pairs = collect_pairs(all_decls, light_vars, ambiguous_vars(all_decls))
    rev = {c: n for n, c in palette.items()}

    def label(c: Color) -> str:
        if c in rev:
            return rev[c]
        near = min(palette.items(), key=lambda kv: kv[1].distance(c), default=None)
        return near[0] if near and near[1].distance(c) < 0.06 else c.hex

    if pairs:
        rows = []
        for sel, fg, bg in pairs:
            ratio = fg.contrast(bg)
            rows.append(
                {
                    "selector": sel[:64],
                    "foreground": label(fg), "foreground_hex": fg.hex,
                    "background": label(bg), "background_hex": bg.hex,
                    "ratio": round(ratio, 2),
                    "aa_normal": ratio >= 4.5,
                    "aa_large": ratio >= 3.0,
                    "aaa_normal": ratio >= 7.0,
                }
            )
        rows.sort(key=lambda r: r["ratio"])       # failures first
        tokens["contrast"] = rows[:24]
    else:
        tokens["contrast"] = contrast_report(palette)

    tokens["audit"] = build_audit(
        palette, overlays, off_grid, grid, tokens["contrast"], shadow_suspects,
        fonts, len(breakpoints), raw_widths,
    )

    log("\n▸ Writing")
    (out / "design-tokens.json").write_text(
        json.dumps(
            {k: v for k, v in tokens.items() if not k.startswith("_")},
            indent=2, ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (out / "theme.css").write_text(emit_theme_css(tokens, primary), encoding="utf-8")
    (out / "components.css").write_text(
        f"/* Generated from {primary} */\n" + COMPONENTS_TEMPLATE, encoding="utf-8"
    )
    (out / "tailwind.theme.css").write_text(
        emit_tailwind_v4(tokens, primary), encoding="utf-8"
    )
    (out / "tailwind.config.js").write_text(
        emit_tailwind_v3(tokens, primary), encoding="utf-8"
    )

    stats = {
        "issues": len(tokens["audit"]),
        "pages": len(pages),
        "stylesheets": len(assets),
        "declarations": len(all_decls),
        "colours": len(palette),
        "type sizes": len(font_sizes),
        "spacing steps": len(spacing),
        "breakpoints": len(tokens["breakpoints"]),
    }
    (out / "style-guide.html").write_text(
        emit_style_guide(tokens, primary, stats), encoding="utf-8"
    )

    print()
    print("  extract-theme — done")
    print("  " + "─" * 46)
    for k, v in stats.items():
        print(f"  {k:<16} {v}")
    print("  " + "─" * 46)
    for f in (
        "style-guide.html", "design-tokens.json", "theme.css",
        "components.css", "tailwind.theme.css", "tailwind.config.js",
        "raw/combined.css",
    ):
        print(f"  {out / f}")
    print()
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="extract-theme",
        description="Extract a usable design system from any website's CSS.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            examples:
              extract-theme https://stripe.com
              extract-theme https://linear.app --crawl 10 -o ./linear-theme
              extract-theme ./saved-page.html --max-colors 24 -q
            """
        ),
    )
    p.add_argument("urls", nargs="+", help="page URL(s) or local .html/.css path(s)")
    p.add_argument("-o", "--out", default="extracted-theme", help="output directory")
    p.add_argument("--crawl", type=int, default=0, metavar="N",
                   help="also scan up to N same-site pages (default 0)")
    p.add_argument("--max-colors", type=int, default=48)
    p.add_argument("--min-count", type=int, default=1,
                   help="drop colours used fewer than N times")
    p.add_argument("--color-tolerance", type=float, default=0.02,
                   help="OKLab distance below which two colours merge")
    p.add_argument("--max-spacing", type=int, default=24)
    p.add_argument("--root-font-size", type=float, default=16.0,
                   help="px value used to convert rem/em")
    p.add_argument("--timeout", type=int, default=25)
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--user-agent", default=DEFAULT_UA)
    p.add_argument("--insecure", action="store_true", help="skip TLS verification")
    p.add_argument("-q", "--quiet", action="store_true")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--version", action="version", version=f"extract-theme {__version__}")
    return p


def main(argv: Sequence[str] | None = None) -> int:
    global _VERBOSITY
    args = build_parser().parse_args(argv)
    _VERBOSITY = 0 if args.quiet else (2 if args.verbose else 1)
    try:
        return run(args)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
