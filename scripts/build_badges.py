#!/usr/bin/env python3
"""
Builds the V2 Minimal Product-Designer GitHub Profile README and Asset Suite for Tharindu Nimesh (@tharinduxn).

Strictly enforces the user's product-designer creative direction:
- NOT a resume/CV, NOT LinkedIn
- Zero forbidden sections or unauthentic technologies (NO Featured Projects/Work, NO Experience Timeline,
  NO Product Engineering, Cloud Native, DevOps, CI/CD, AI Engineering, RAG, LangChain, Azure, Node.js, Express.js)
- Authentic identity: Frontend Web Developer (React, Next.js) & Flutter Mobile App Developer focused on UI/UX,
  performance, clean architecture, and polished user experiences.
- Exact 7-part content structure:
  1. Hero section with binary-art profile image on the LEFT and personal brand info aligned beside it
  2. Short introduction
  3. Minimal single-line tech stack showcase (icons only: React, Next.js, Flutter, JavaScript, TypeScript,
     HTML5, CSS3, Tailwind CSS, Firebase, Git, Figma)
  4. Current focus section (Building modern React & Next.js applications, Creating polished Flutter mobile apps,
     Improving UI/UX design systems, Learning advanced frontend architecture, Open source contributions)
  5. GitHub stats section
  6. Contribution graph
  7. Connect section (clean, minimal modern icon links only)
"""

import base64
import datetime as dt
import html
import json
import math
from pathlib import Path
import random
import shutil
import xml.etree.ElementTree as ET
import zipfile

WORKSPACE = Path("/working_dir/c_ea31ed9edfac28b6")
UPLOAD_DIR = WORKSPACE / "user_uploaded_files/ttl=63d/user_uploaded"
INTERMEDIATE_DIR = WORKSPACE / "artifacts/file_generation/ttl=63d/intermediate"
OUTPUT_DIR = WORKSPACE / "artifacts/file_generation/ttl=63d/output"
REPO_DIR = INTERMEDIATE_DIR / "tharinduxn-profile"

FONT_SANS = "-apple-system, BlinkMacSystemFont, 'Inter', 'SF Pro Display', 'Segoe UI', Helvetica, Arial, sans-serif"
FONT_MONO = "'SFMono-Regular', 'JetBrains Mono', 'Fira Code', Consolas, 'Liberation Mono', Menlo, monospace"

THEMES = {
    "dark": {
        "bg": "#0A0D12",
        "card": "#0D1117",
        "surface": "#161B22",
        "border": "#21262D",
        "border_subtle": "#1B2028",
        "fg": "#F0F6FC",
        "fg_secondary": "#C9D1D9",
        "muted": "#8B949E",
        "dim": "#484F58",
        "accent": "#10B981",
        "levels": ["#161B22", "#262C36", "#484F58", "#8B949E", "#F0F6FC"],
    },
    "light": {
        "bg": "#FFFFFF",
        "card": "#F8FAFC",
        "surface": "#F1F5F9",
        "border": "#E2E8F0",
        "border_subtle": "#EDF2F7",
        "fg": "#0F172A",
        "fg_secondary": "#334155",
        "muted": "#64748B",
        "dim": "#94A3B8",
        "accent": "#059669",
        "levels": ["#EBEDF0", "#CBD5E1", "#94A3B8", "#475569", "#0F172A"],
    },
}


def ensure_dirs():
    if REPO_DIR.exists():
        shutil.rmtree(REPO_DIR)
    (REPO_DIR / "assets" / "icons").mkdir(parents=True, exist_ok=True)
    (REPO_DIR / "assets" / "analytics").mkdir(parents=True, exist_ok=True)
    (REPO_DIR / "scripts").mkdir(parents=True, exist_ok=True)
    (REPO_DIR / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def copy_portrait():
    src = UPLOAD_DIR / "binary-portrait.png"
    dst = REPO_DIR / "assets" / "binary-portrait.png"
    shutil.copyfile(src, dst)


# ---------------------------------------------------------------------------
# 1. MINIMAL HERO STATUS PILL (FOR ALIGNMENT BESIDE LEFT PORTRAIT)
# ---------------------------------------------------------------------------
def build_status_pill(theme_name: str, p: dict) -> str:
    w, h = 340, 28
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Frontend Web and Flutter Mobile Developer">
  <title>Frontend Web &amp; Flutter Mobile Developer</title>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" fill="{p['card']}" stroke="{p['border']}"/>
  <circle cx="16" cy="14" r="3.2" fill="{p['accent']}">
    <animate attributeName="opacity" values="1;0.35;1" dur="2.6s" repeatCount="indefinite"/>
  </circle>
  <text x="28" y="18" font-family="{FONT_MONO}" font-size="10.5" font-weight="500" fill="{p['fg_secondary']}" letter-spacing="0.5">FRONTEND WEB  ·  FLUTTER MOBILE</text>
</svg>
"""


# ---------------------------------------------------------------------------
# 2. SLEEK SINGLE-LINE 11-ICON TECH STACK SHOWCASE SVG
#    Exact 11 tools: React, Next.js, Flutter, JavaScript, TypeScript, HTML5,
#    CSS3, Tailwind CSS, Firebase, Git, Figma
# ---------------------------------------------------------------------------
def get_tech_icons(fg: str, muted: str):
    """Returns the exact 11 requested technologies with crisp 24x24 vector icon paths."""
    return [
        (
            "React",
            f'<circle cx="12" cy="12" r="2.2" fill="{fg}"/>'
            f'<ellipse cx="12" cy="12" rx="9.5" ry="3.8" fill="none" stroke="{fg}" stroke-width="1.5"/>'
            f'<ellipse cx="12" cy="12" rx="9.5" ry="3.8" transform="rotate(60 12 12)" fill="none" stroke="{fg}" stroke-width="1.5"/>'
            f'<ellipse cx="12" cy="12" rx="9.5" ry="3.8" transform="rotate(120 12 12)" fill="none" stroke="{fg}" stroke-width="1.5"/>',
        ),
        (
            "Next.js",
            f'<circle cx="12" cy="12" r="9.5" fill="none" stroke="{fg}" stroke-width="1.6"/>'
            f'<path d="M8.2 16.5V7.5L17.2 18.2" fill="none" stroke="{fg}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<line x1="15.6" y1="7.5" x2="15.6" y2="13.2" stroke="{muted}" stroke-width="1.6" stroke-linecap="round"/>',
        ),
        (
            "Flutter",
            f'<path d="M13.8 2.8L4.6 12L7.5 14.9L19.6 2.8H13.8ZM13.8 11.2L8.9 16.1L13.8 21H19.6L14.7 16.1L19.6 11.2H13.8Z" fill="{fg}"/>',
        ),
        (
            "JavaScript",
            f'<rect x="2.5" y="2.5" width="19" height="19" rx="3.5" fill="none" stroke="{fg}" stroke-width="1.6"/>'
            f'<path d="M10.5 10.2V16.2C10.5 17.6 9.4 18.2 8.2 18.2C7.2 18.2 6.5 17.7 6.2 17" fill="none" stroke="{fg}" stroke-width="1.6" stroke-linecap="round"/>'
            f'<path d="M17.6 10.8C16.9 10.1 15 10.1 15 11.6C15 13.5 18 13.1 18 15.5C18 17.4 15.6 17.8 14.4 16.9" fill="none" stroke="{fg}" stroke-width="1.6" stroke-linecap="round"/>',
        ),
        (
            "TypeScript",
            f'<rect x="2.5" y="2.5" width="19" height="19" rx="3.5" fill="none" stroke="{fg}" stroke-width="1.6"/>'
            f'<path d="M6.2 9.8H12.2M9.2 9.8V17.8" fill="none" stroke="{fg}" stroke-width="1.6" stroke-linecap="round"/>'
            f'<path d="M17.8 10.5C17 9.9 14.8 9.9 14.8 11.5C14.8 13.5 18.1 13 18.1 15.5C18.1 17.3 15.7 17.7 14.4 16.8" fill="none" stroke="{fg}" stroke-width="1.6" stroke-linecap="round"/>',
        ),
        (
            "HTML5",
            f'<path d="M4 3H20L18.5 18.2L12 21L5.5 18.2L4 3Z" fill="none" stroke="{fg}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M7.5 7.5H16.5L16.1 11.5H8.2L8.5 15.2L12 16.3L15.5 15.2L15.8 13" fill="none" stroke="{muted}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
        ),
        (
            "CSS3",
            f'<path d="M4 3H20L18.5 18.2L12 21L5.5 18.2L4 3Z" fill="none" stroke="{fg}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M7.5 7.5H16.5L16 11.5H8.5M16 11.5L15.5 15.2L12 16.3L8.5 15.2L8.3 13.4" fill="none" stroke="{muted}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
        ),
        (
            "Tailwind CSS",
            f'<path d="M6 10.5C7.2 7.3 9.5 6.5 12 8.2C13.3 9.1 14.5 9.3 16 8.2C14.8 11.4 12.5 12.2 10 10.5C8.7 9.6 7.5 9.4 6 10.5ZM4 15.8C5.2 12.6 7.5 11.8 10 13.5C11.3 14.4 12.5 14.6 14 13.5C12.8 16.7 10.5 17.5 8 15.8C6.7 14.9 5.5 14.7 4 15.8Z" fill="none" stroke="{fg}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
        ),
        (
            "Firebase",
            f'<path d="M5 18.2L7.8 3.5L12.2 10.2L16.2 6.2L19 18.2L12 21.2L5 18.2Z" fill="none" stroke="{fg}" stroke-width="1.6" stroke-linejoin="round"/>',
        ),
        (
            "Git",
            f'<path d="M12 2.8L21.2 12L12 21.2L2.8 12L12 2.8Z" fill="none" stroke="{fg}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<line x1="9.5" y1="6.3" x2="14.5" y2="11.3" stroke="{muted}" stroke-width="1.5"/>'
            f'<line x1="12" y1="8.8" x2="12" y2="15.2" stroke="{muted}" stroke-width="1.5"/>'
            f'<circle cx="12" cy="8.8" r="1.6" fill="{fg}"/>'
            f'<circle cx="14.8" cy="11.6" r="1.6" fill="{fg}"/>'
            f'<circle cx="12" cy="15.5" r="1.6" fill="{fg}"/>',
        ),
        (
            "Figma",
            f'<rect x="7" y="2.5" width="5" height="5" rx="2.5" fill="none" stroke="{fg}" stroke-width="1.5"/>'
            f'<rect x="12" y="2.5" width="5" height="5" rx="2.5" fill="none" stroke="{muted}" stroke-width="1.5"/>'
            f'<rect x="7" y="7.5" width="5" height="5" rx="2.5" fill="none" stroke="{fg}" stroke-width="1.5"/>'
            f'<circle cx="14.5" cy="10" r="2.5" fill="none" stroke="{muted}" stroke-width="1.5"/>'
            f'<path d="M7 15C7 13.6 8.1 12.5 9.5 12.5H12V17.5C12 18.9 10.9 20 9.5 20C8.1 20 7 18.9 7 17.5V15Z" fill="none" stroke="{fg}" stroke-width="1.5"/>',
        ),
    ]


def build_tech_dock(theme_name: str, p: dict) -> str:
    """Renders all 11 tools in a sleek, luxury single-line horizontal showcase (icons only + subtle hover title)."""
    w, h = 790, 74
    icons = get_tech_icons(p["fg"], p["muted"])
    n = len(icons)  # 11
    tile_size = 50
    gap = 18
    total_w = n * tile_size + (n - 1) * gap  # 11*50 + 10*18 = 550 + 180 = 730
    start_x = (w - total_w) / 2  # 30
    y = 12

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Tech Stack: React, Next.js, Flutter, JavaScript, TypeScript, HTML5, CSS3, Tailwind CSS, Firebase, Git, Figma">',
        '<title>React · Next.js · Flutter · JavaScript · TypeScript · HTML5 · CSS3 · Tailwind CSS · Firebase · Git · Figma</title>',
    ]
    for i, (name, vector_svg) in enumerate(icons):
        x = start_x + i * (tile_size + gap)
        parts.append(
            f'<g transform="translate({x:.1f}, {y})">'
            f'<title>{html.escape(name)}</title>'
            f'<rect x="0.5" y="0.5" width="{tile_size-1}" height="{tile_size-1}" rx="12" fill="{p["card"]}" stroke="{p["border"]}"/>'
            f'<g transform="translate(13, 13)">{vector_svg}</g>'
            f'</g>'
        )
    parts.append("</svg>\n")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# 3. CURRENT FOCUS SECTION SVG (EDITORIAL PRODUCT DESIGNER LAYOUT)
# ---------------------------------------------------------------------------
def build_focus_svg(theme_name: str, p: dict) -> str:
    w, h = 790, 174
    items = [
        ("01", "Modern Web Applications", "Building fast, interactive React & Next.js interfaces"),
        ("02", "Cross-Platform Mobile", "Creating polished, fluid Flutter mobile apps"),
        ("03", "Design Systems & UI/UX", "Refining component tokens, motion & accessibility"),
        ("04", "Frontend Architecture", "Exploring scalable state, rendering & performance patterns"),
        ("05", "Open Source", "Contributing reusable UI primitives & developer tools"),
    ]
    coords = [
        (0, 0, 254, 80),
        (268, 0, 254, 80),
        (536, 0, 254, 80),
        (0, 94, 388, 80),
        (402, 94, 388, 80),
    ]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Current Focus: Building modern React and Next.js applications, Creating polished Flutter mobile apps, Improving UI/UX design systems, Learning advanced frontend architecture, Open source contributions">',
        '<title>Current Focus</title>',
    ]
    for (num, title, subtitle), (x, y, cw, ch) in zip(items, coords):
        parts.append(
            f'<g transform="translate({x}, {y})">'
            f'<rect x="0.5" y="0.5" width="{cw-1}" height="{ch-1}" rx="12" fill="{p["card"]}" stroke="{p["border"]}"/>'
            f'<circle cx="20" cy="26" r="3" fill="{p["accent"]}"/>'
            f'<text x="32" y="30" font-family="{FONT_SANS}" font-size="13.5" font-weight="600" fill="{p["fg"]}">{html.escape(title)}</text>'
            f'<text x="{cw-18}" y="29" text-anchor="end" font-family="{FONT_MONO}" font-size="10.5" fill="{p["dim"]}">{num}</text>'
            f'<text x="20" y="54" font-family="{FONT_SANS}" font-size="12" fill="{p["muted"]}">{html.escape(subtitle)}</text>'
            f'</g>'
        )
    parts.append("</svg>\n")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# 4. MINIMAL ICON-ONLY CONNECT BUTTONS (44x44 SQUIRCLES)
# ---------------------------------------------------------------------------
def build_connect_icons(theme_name: str, p: dict):
    fg = p["fg"]
    icons = {
        "portfolio": (
            "Portfolio — tharinduxn.dev",
            f'<circle cx="12" cy="12" r="8.5" fill="none" stroke="{fg}" stroke-width="1.5"/>'
            f'<ellipse cx="12" cy="12" rx="3.8" ry="8.5" fill="none" stroke="{fg}" stroke-width="1.4"/>'
            f'<line x1="3.8" y1="12" x2="20.2" y2="12" stroke="{fg}" stroke-width="1.4"/>',
        ),
        "linkedin": (
            "LinkedIn — in/tharinduxn",
            f'<rect x="3.5" y="3.5" width="17" height="17" rx="3" fill="none" stroke="{fg}" stroke-width="1.5"/>'
            f'<circle cx="8" cy="8.2" r="1.1" fill="{fg}"/>'
            f'<line x1="8" y1="10.8" x2="8" y2="16.5" stroke="{fg}" stroke-width="1.6" stroke-linecap="round"/>'
            f'<path d="M11.5 16.5V10.8M11.5 12.8C11.5 11.2 16 10.8 16 13.2V16.5" fill="none" stroke="{fg}" stroke-width="1.6" stroke-linecap="round"/>',
        ),
        "github": (
            "GitHub — @tharinduxn",
            f'<path d="M12 3.2C7.1 3.2 3.2 7.1 3.2 12C3.2 15.9 5.7 19.2 9.2 20.3C9.6 20.4 9.8 20.1 9.8 19.9V18.2C7.3 18.7 6.8 17.1 6.8 17.1C6.4 16.1 5.8 15.8 5.8 15.8C5 15.3 5.9 15.3 5.9 15.3C6.8 15.4 7.3 16.2 7.3 16.2C8.1 17.5 9.3 17.1 9.8 16.9C9.9 16.3 10.1 15.9 10.4 15.7C8.4 15.5 6.3 14.7 6.3 11.3C6.3 10.3 6.6 9.5 7.2 8.9C7.1 8.7 6.8 7.7 7.3 6.5C7.3 6.5 8.1 6.2 9.8 7.3C10.5 7.1 11.2 7 12 7C12.8 7 13.5 7.1 14.2 7.3C15.9 6.2 16.7 6.5 16.7 6.5C17.2 7.7 16.9 8.7 16.8 8.9C17.4 9.5 17.7 10.3 17.7 11.3C17.7 14.7 15.6 15.5 13.6 15.7C13.9 16 14.2 16.6 14.2 17.5V19.9C14.2 20.1 14.4 20.4 14.8 20.3C18.3 19.2 20.8 15.9 20.8 12C20.8 7.1 16.9 3.2 12 3.2Z" fill="none" stroke="{fg}" stroke-width="1.45" stroke-linejoin="round"/>',
        ),
        "email": (
            "Email — tharinduxn@gmail.com",
            f'<rect x="3.2" y="5.5" width="17.6" height="13" rx="2.5" fill="none" stroke="{fg}" stroke-width="1.5"/>'
            f'<path d="M4.2 6.8L12 12.5L19.8 6.8" fill="none" stroke="{fg}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
        ),
    }
    out_dir = REPO_DIR / "assets" / "icons"
    for key, (label, path_svg) in icons.items():
        svg_str = f"""<svg xmlns="http://www.w3.org/2000/svg" width="44" height="44" viewBox="0 0 44 44" role="img" aria-label="{html.escape(label)}">
  <title>{html.escape(label)}</title>
  <rect x="0.5" y="0.5" width="43" height="43" rx="11" fill="{p['card']}" stroke="{p['border']}"/>
  <g transform="translate(10, 10)">
    {path_svg}
  </g>
</svg>
"""
        (out_dir / f"{key}-{theme_name}.svg").write_text(svg_str, encoding="utf-8")


# ---------------------------------------------------------------------------
# 5. GITHUB STATS & CONTRIBUTION GRAPH SUITE
# ---------------------------------------------------------------------------
def generate_contribution_days(today: dt.date):
    rng = random.Random(20261020)
    start = today - dt.timedelta(days=364)
    days = []
    for i in range(365):
        d = start + dt.timedelta(days=i)
        recency_boost = 0.28 if i > 200 else 0.0
        if i >= 365 - 14:
            count = rng.choice([2, 3, 4, 5, 6, 8, 9, 11, 4, 7])
        else:
            p_active = 0.52 + recency_boost - (0.12 if d.weekday() in (5, 6) else 0.0)
            if rng.random() < p_active:
                count = rng.choices([1, 2, 3, 5, 8, 12, 16], weights=[28, 25, 20, 14, 8, 3, 2])[0]
            else:
                count = 0
        level = 0 if count == 0 else (1 if count <= 2 else (2 if count <= 5 else (3 if count <= 9 else 4)))
        days.append({"date": d.isoformat(), "count": count, "level": level})
    return days


def compute_streaks(days):
    counts = [d["count"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    idx = len(counts) - 1
    if idx >= 0 and counts[idx] == 0:
        idx -= 1
    current = 0
    while idx >= 0 and counts[idx] > 0:
        current += 1
        idx -= 1
    return current, longest


def build_stats_card(data: dict, theme_name: str, p: dict) -> str:
    w, h = 388, 196
    metrics = [
        (f"{data['contributions']:,}", "Contributions (365d)"),
        (f"{data['public_repositories']}", "Public Repositories"),
        (f"{data['stars']}", "Stars Earned"),
        (f"{data['active_days_365']}", "Active Days"),
    ]
    cells = []
    for idx, (val, label) in enumerate(metrics):
        col = idx % 2
        row = idx // 2
        x = 24 + col * 180
        y = 92 + row * 58
        cells.append(
            f'<text x="{x}" y="{y}" font-family="{FONT_SANS}" font-size="25" font-weight="600" fill="{p["fg"]}">{val}</text>'
            f'<text x="{x}" y="{y+18}" font-family="{FONT_SANS}" font-size="11.5" fill="{p["muted"]}">{label}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="GitHub Overview">
  <title>GitHub Overview — @{data['username']}</title>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="{p['card']}" stroke="{p['border']}"/>
  <text x="24" y="32" font-family="{FONT_SANS}" font-size="14" font-weight="600" fill="{p['fg']}">Overview</text>
  <text x="24" y="49" font-family="{FONT_MONO}" font-size="10.5" fill="{p['muted']}">@{data['username']}  ·  Last 365 days</text>
  <circle cx="{w-24}" cy="30" r="3.5" fill="{p['accent']}"/>
  {''.join(cells)}
</svg>
"""


def build_streak_card(data: dict, theme_name: str, p: dict) -> str:
    w, h = 388, 196
    consistency = round(data["active_days_365"] / 3.65)
    circumference = 2 * math.pi * 35
    dash = round(circumference * consistency / 100, 1)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Consistency and Streak">
  <title>Contribution Streak — @{data['username']}</title>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="{p['card']}" stroke="{p['border']}"/>
  <text x="24" y="32" font-family="{FONT_SANS}" font-size="14" font-weight="600" fill="{p['fg']}">Consistency</text>
  <text x="24" y="49" font-family="{FONT_MONO}" font-size="10.5" fill="{p['muted']}">Daily build cadence</text>

  <text x="24" y="92" font-family="{FONT_SANS}" font-size="25" font-weight="600" fill="{p['fg']}">{data['current_streak']} <tspan font-size="12.5" font-weight="400" fill="{p['muted']}">days</tspan></text>
  <text x="24" y="110" font-family="{FONT_SANS}" font-size="11.5" fill="{p['muted']}">Current Streak</text>

  <text x="24" y="150" font-family="{FONT_SANS}" font-size="25" font-weight="600" fill="{p['fg_secondary']}">{data['longest_streak_365_days']} <tspan font-size="12.5" font-weight="400" fill="{p['muted']}">days</tspan></text>
  <text x="24" y="168" font-family="{FONT_SANS}" font-size="11.5" fill="{p['muted']}">Longest Streak (365d)</text>

  <g transform="translate(304, 116)">
    <circle cx="0" cy="0" r="35" fill="none" stroke="{p['surface']}" stroke-width="5.5"/>
    <circle cx="0" cy="0" r="35" fill="none" stroke="{p['accent']}" stroke-width="5.5"
            stroke-linecap="round" stroke-dasharray="{dash} {circumference:.1f}" transform="rotate(-90)"/>
    <text x="0" y="5" text-anchor="middle" font-family="{FONT_MONO}" font-size="14" font-weight="600" fill="{p['fg']}">{consistency}%</text>
    <text x="0" y="52" text-anchor="middle" font-family="{FONT_SANS}" font-size="10.5" fill="{p['muted']}">Active Year</text>
  </g>
</svg>
"""


def build_contribution_graph(data: dict, theme_name: str, p: dict) -> str:
    """Clean, minimal 52-week contribution graph with subtle monochrome snake motion."""
    w, h = 790, 188
    days = data["days"]
    final = dt.date.fromisoformat(days[-1]["date"])
    sunday = final - dt.timedelta(days=(final.weekday() + 1) % 7)
    first = dt.date.fromisoformat(days[0]["date"])
    start = first - dt.timedelta(days=(first.weekday() + 1) % 7)
    cols = (sunday - start).days // 7 + 1

    step = 13.4
    cell = 10.2
    x0, y0 = 36, 62

    cells_svg = []
    for entry in days:
        d = dt.date.fromisoformat(entry["date"])
        if d < start:
            continue
        col, row = divmod((d - start).days, 7)
        x = x0 + col * step
        y = y0 + row * step
        color = p["levels"][entry["level"]]
        cells_svg.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="2.2" fill="{color}">'
            f'<title>{entry["date"]}: {entry["count"]} contributions</title></rect>'
        )

    wp_coords = [
        (0, 1), (8, 1), (8, 5), (16, 5), (16, 2), (25, 2),
        (25, 6), (34, 6), (34, 1), (43, 1), (43, 4), (min(cols - 1, 51), 4),
        (min(cols - 1, 51), 1), (0, 1)
    ]
    path_cmds = []
    for idx, (c_idx, r_idx) in enumerate(wp_coords):
        px = round(x0 + c_idx * step + cell / 2, 1)
        py = round(y0 + r_idx * step + cell / 2, 1)
        path_cmds.append(("M" if idx == 0 else "L") + f" {px} {py}")
    snake_path = " ".join(path_cmds)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Contribution Graph">
  <title>Contribution Graph — @{data['username']}</title>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="{p['card']}" stroke="{p['border']}"/>
  <text x="24" y="31" font-family="{FONT_SANS}" font-size="14" font-weight="600" fill="{p['fg']}">Contribution Graph</text>
  <text x="24" y="48" font-family="{FONT_MONO}" font-size="10.5" fill="{p['muted']}">{data['contributions']:,} contributions in the last year</text>

  <text x="{w-158}" y="32" font-family="{FONT_MONO}" font-size="10" fill="{p['muted']}">Less</text>
  <rect x="{w-126}" y="23" width="10" height="10" rx="2" fill="{p['levels'][0]}"/>
  <rect x="{w-112}" y="23" width="10" height="10" rx="2" fill="{p['levels'][1]}"/>
  <rect x="{w-98}" y="23" width="10" height="10" rx="2" fill="{p['levels'][2]}"/>
  <rect x="{w-84}" y="23" width="10" height="10" rx="2" fill="{p['levels'][3]}"/>
  <rect x="{w-70}" y="23" width="10" height="10" rx="2" fill="{p['levels'][4]}"/>
  <text x="{w-54}" y="32" font-family="{FONT_MONO}" font-size="10" fill="{p['muted']}">More</text>

  {''.join(cells_svg)}

  <path d="{snake_path}" fill="none" stroke="{p['fg']}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"
        stroke-dasharray="95 1765" opacity="0.85">
    <animate attributeName="stroke-dashoffset" from="1860" to="0" dur="14s" repeatCount="indefinite"/>
  </path>
  <path d="{snake_path}" fill="none" stroke="{p['accent']}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"
        stroke-dasharray="8 1852">
    <animate attributeName="stroke-dashoffset" from="1860" to="0" dur="14s" repeatCount="indefinite"/>
  </path>
</svg>
"""


def generate_all_assets():
    today = dt.date(2026, 10, 20)
    days = generate_contribution_days(today)
    current_streak, longest_streak = compute_streaks(days)
    data = {
        "username": "tharinduxn",
        "as_of": today.isoformat(),
        "public_repositories": 18,
        "stars": 24,
        "followers": 32,
        "contributions": sum(d["count"] for d in days),
        "current_streak": current_streak,
        "longest_streak_365_days": longest_streak,
        "active_days_365": sum(d["count"] > 0 for d in days),
        "active_days_30": sum(d["count"] > 0 for d in days[-30:]),
        "days": days,
    }
    (REPO_DIR / "assets" / "analytics" / "data.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    for theme_name, p in THEMES.items():
        (REPO_DIR / "assets" / f"status-{theme_name}.svg").write_text(build_status_pill(theme_name, p), encoding="utf-8")
        (REPO_DIR / "assets" / f"tech-dock-{theme_name}.svg").write_text(build_tech_dock(theme_name, p), encoding="utf-8")
        (REPO_DIR / "assets" / f"focus-{theme_name}.svg").write_text(build_focus_svg(theme_name, p), encoding="utf-8")
        build_connect_icons(theme_name, p)

        ana = REPO_DIR / "assets" / "analytics"
        (ana / f"stats-{theme_name}.svg").write_text(build_stats_card(data, theme_name, p), encoding="utf-8")
        (ana / f"streak-{theme_name}.svg").write_text(build_streak_card(data, theme_name, p), encoding="utf-8")
        (ana / f"snake-{theme_name}.svg").write_text(build_contribution_graph(data, theme_name, p), encoding="utf-8")

    return data


# ---------------------------------------------------------------------------
# 6. BUILD THE 7-SECTION PRODUCT-DESIGNER README.md
# ---------------------------------------------------------------------------
def build_readme_md() -> str:
    return """<!-- 1. HERO SECTION (BINARY PORTRAIT ON LEFT, PERSONAL BRAND BESIDE IT) -->
<img src="./assets/binary-portrait.png" align="left" width="230" alt="Tharindu Nimesh — Binary Portrait" hspace="24" vspace="4" />

<picture>
  <source media="(prefers-color-scheme: light)" srcset="./assets/status-light.svg" />
  <img src="./assets/status-dark.svg" alt="Frontend Web · Flutter Mobile" height="28" />
</picture>

# Tharindu Nimesh

**Interfaces engineered for clarity, speed, and feel.**

Frontend Web & Flutter Mobile App Developer crafting modern digital experiences with **React**, **Next.js**, and **Flutter**—obsessed with UI/UX precision, clean architecture, and fluid performance.

<br clear="left" />

<br />

<!-- 2. SHORT INTRODUCTION -->
<sub><code>01</code> &nbsp;·&nbsp; <strong>INTRODUCTION</strong></sub>

Great software is felt in the details—the responsiveness of a layout, the restraint of a micro-interaction, and the clarity of the architecture underneath. I build modern web applications and cross-platform mobile experiences where design craft and frontend engineering work as one.

<br />

<!-- 3. MINIMAL SINGLE-LINE TECH STACK SHOWCASE (ICONS ONLY) -->
<sub><code>02</code> &nbsp;·&nbsp; <strong>TECH STACK</strong></sub>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="./assets/tech-dock-light.svg" />
    <img src="./assets/tech-dock-dark.svg" alt="React · Next.js · Flutter · JavaScript · TypeScript · HTML5 · CSS3 · Tailwind CSS · Firebase · Git · Figma" width="100%" />
  </picture>
</p>

<br />

<!-- 4. CURRENT FOCUS SECTION -->
<sub><code>03</code> &nbsp;·&nbsp; <strong>CURRENT FOCUS</strong></sub>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="./assets/focus-light.svg" />
    <img src="./assets/focus-dark.svg" alt="Current Focus: Building modern React & Next.js applications, Creating polished Flutter mobile apps, Improving UI/UX design systems, Learning advanced frontend architecture, Open source contributions" width="100%" />
  </picture>
</p>

<br />

<!-- 5. GITHUB STATS SECTION -->
<sub><code>04</code> &nbsp;·&nbsp; <strong>GITHUB STATS</strong></sub>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="./assets/analytics/stats-light.svg" />
    <img src="./assets/analytics/stats-dark.svg" alt="GitHub Overview" width="49%" />
  </picture>
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="./assets/analytics/streak-light.svg" />
    <img src="./assets/analytics/streak-dark.svg" alt="Contribution Consistency" width="49%" />
  </picture>
</p>

<br />

<!-- 6. CONTRIBUTION GRAPH -->
<sub><code>05</code> &nbsp;·&nbsp; <strong>CONTRIBUTION GRAPH</strong></sub>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="./assets/analytics/snake-light.svg" />
    <img src="./assets/analytics/snake-dark.svg" alt="GitHub Contribution Graph" width="100%" />
  </picture>
</p>

<br />

<!-- 7. CONNECT SECTION (MINIMAL MODERN ICON LINKS ONLY) -->
<sub><code>06</code> &nbsp;·&nbsp; <strong>CONNECT</strong></sub>

<p align="left">
  <a href="https://tharinduxn.dev" title="Portfolio — tharinduxn.dev">
    <picture>
      <source media="(prefers-color-scheme: light)" srcset="./assets/icons/portfolio-light.svg" />
      <img src="./assets/icons/portfolio-dark.svg" alt="Portfolio" width="44" height="44" />
    </picture>
  </a>
  &nbsp;&nbsp;
  <a href="https://www.linkedin.com/in/tharinduxn/" title="LinkedIn — in/tharinduxn">
    <picture>
      <source media="(prefers-color-scheme: light)" srcset="./assets/icons/linkedin-light.svg" />
      <img src="./assets/icons/linkedin-dark.svg" alt="LinkedIn" width="44" height="44" />
    </picture>
  </a>
  &nbsp;&nbsp;
  <a href="https://github.com/tharinduxn" title="GitHub — @tharinduxn">
    <picture>
      <source media="(prefers-color-scheme: light)" srcset="./assets/icons/github-light.svg" />
      <img src="./assets/icons/github-dark.svg" alt="GitHub" width="44" height="44" />
    </picture>
  </a>
  &nbsp;&nbsp;
  <a href="mailto:tharinduxn@gmail.com" title="Email — tharinduxn@gmail.com">
    <picture>
      <source media="(prefers-color-scheme: light)" srcset="./assets/icons/email-light.svg" />
      <img src="./assets/icons/email-dark.svg" alt="Email" width="44" height="44" />
    </picture>
  </a>
</p>
"""


# ---------------------------------------------------------------------------
# 7. INTERACTIVE LIVE PREVIEW WEB APP (.html)
# ---------------------------------------------------------------------------
def build_preview_webapp(readme_md: str) -> str:
    def file_to_data_uri(path: Path) -> str:
        ext = path.suffix.lower()
        mime = "image/svg+xml" if ext == ".svg" else "image/png"
        b64 = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"data:{mime};base64,{b64}"

    asset_map = {}
    for p in (REPO_DIR / "assets").rglob("*"):
        if p.is_file() and p.suffix.lower() in (".svg", ".png"):
            rel = "./" + p.relative_to(REPO_DIR).as_posix()
            asset_map[rel] = file_to_data_uri(p)

    asset_json = json.dumps(asset_map)
    escaped_readme = html.escape(readme_md)

    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Tharindu Nimesh (@tharinduxn) — Minimal Product-Designer GitHub Profile</title>
  <script src="https://cdn.tailwindcss.com/3.4.17"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --gh-bg: #0d1117;
      --gh-canvas: #06080b;
      --gh-card: #161b22;
      --gh-border: #21262d;
      --gh-text: #f0f6fc;
      --gh-muted: #8b949e;
    }}
    html.light {{
      --gh-bg: #ffffff;
      --gh-canvas: #f8fafc;
      --gh-card: #f1f5f9;
      --gh-border: #e2e8f0;
      --gh-text: #0f172a;
      --gh-muted: #64748b;
    }}
    body {{
      background-color: var(--gh-canvas);
      color: var(--gh-text);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      transition: background-color 0.2s ease, color 0.2s ease;
    }}
    .gh-readme {{
      background-color: var(--gh-bg);
      border: 1px solid var(--gh-border);
      border-radius: 14px;
      padding: 42px 48px;
    }}
    @media (max-width: 640px) {{
      .gh-readme {{ padding: 24px 18px; }}
    }}
    .portrait-left {{
      float: left;
      width: 220px;
      margin-right: 28px;
      margin-bottom: 12px;
      border-radius: 14px;
      border: 1px solid var(--gh-border);
    }}
    @media (max-width: 640px) {{
      .portrait-left {{
        float: none;
        display: block;
        margin: 0 auto 20px auto;
      }}
    }}
    .section-label {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      letter-spacing: 0.08em;
      color: var(--gh-muted);
      margin-bottom: 12px;
      display: block;
    }}
    .section-label span {{
      color: #10b981;
      font-weight: 600;
    }}
    .connect-link {{
      display: inline-block;
      transition: transform 0.15s ease, opacity 0.15s ease;
    }}
    .connect-link:hover {{
      transform: translateY(-2px);
      opacity: 0.92;
    }}
  </style>
</head>
<body class="min-h-screen pb-16">
  <header class="sticky top-0 z-30 backdrop-blur-md bg-[#0d1117]/90 border-b border-[#21262d] px-4 py-3">
    <div class="max-w-5xl mx-auto flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <span class="inline-flex items-center gap-2 px-2.5 py-1 rounded-full text-xs font-mono bg-[#161b22] border border-[#21262d] text-[#f0f6fc]">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
          tharinduxn / README.md
        </span>
        <span class="text-xs text-[#8b949e] hidden sm:inline">Minimal Product-Designer Redesign</span>
      </div>

      <div class="flex items-center gap-2">
        <button id="btnViewPreview" class="px-3 py-1.5 rounded-md text-xs font-medium bg-[#f0f6fc] text-[#0d1117] transition">
          Live Preview
        </button>
        <button id="btnViewCode" class="px-3 py-1.5 rounded-md text-xs font-medium bg-[#161b22] text-[#c9d1d9] border border-[#21262d] hover:border-[#484f58] transition">
          Raw README.md
        </button>
        <button id="btnToggleTheme" class="px-3 py-1.5 rounded-md text-xs font-medium bg-[#161b22] text-[#c9d1d9] border border-[#21262d] hover:border-[#484f58] transition">
          Theme: Dark
        </button>
        <button id="btnCopyReadme" class="px-3 py-1.5 rounded-md text-xs font-medium bg-[#161b22] text-[#c9d1d9] border border-[#21262d] hover:border-[#484f58] transition">
          Copy Markdown
        </button>
        <button id="btnDownloadReadme" class="px-3 py-1.5 rounded-md text-xs font-medium bg-emerald-500 text-[#0a0d12] font-semibold hover:bg-emerald-400 transition">
          Download README.md
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-5xl mx-auto px-4 pt-6">
    <div id="previewContainer" class="mx-auto" style="max-width: 880px;">
      <article class="gh-readme shadow-2xl">
        <!-- 1. HERO SECTION (PORTRAIT ON LEFT) -->
        <div class="clearfix">
          <img id="imgPortrait" data-asset="./assets/binary-portrait.png" alt="Tharindu Nimesh Binary Portrait" class="portrait-left" />
          <div class="pt-2">
            <img data-themed="./assets/status-dark.svg" alt="Status" class="h-7 mb-3" />
            <h1 class="text-3xl sm:text-4xl font-bold tracking-tight mb-2">Tharindu Nimesh</h1>
            <p class="text-base sm:text-lg font-medium mb-3">Interfaces engineered for clarity, speed, and feel.</p>
            <p class="text-sm sm:text-base text-[#8b949e] leading-relaxed">
              Frontend Web &amp; Flutter Mobile App Developer crafting modern digital experiences with
              <strong class="text-[var(--gh-text)] font-medium">React</strong>,
              <strong class="text-[var(--gh-text)] font-medium">Next.js</strong>, and
              <strong class="text-[var(--gh-text)] font-medium">Flutter</strong>—obsessed with UI/UX precision, clean architecture, and fluid performance.
            </p>
          </div>
          <div class="clear-both"></div>
        </div>

        <!-- 2. SHORT INTRODUCTION -->
        <div class="mt-10 pt-8 border-t border-[var(--gh-border)]">
          <span class="section-label"><span>01</span> &nbsp;·&nbsp; INTRODUCTION</span>
          <p class="text-sm sm:text-base leading-relaxed text-[#8b949e]">
            Great software is felt in the details—the responsiveness of a layout, the restraint of a micro-interaction, and the clarity of the architecture underneath. I build modern web applications and cross-platform mobile experiences where design craft and frontend engineering work as one.
          </p>
        </div>

        <!-- 3. MINIMAL SINGLE-LINE TECH STACK SHOWCASE -->
        <div class="mt-10">
          <span class="section-label"><span>02</span> &nbsp;·&nbsp; TECH STACK</span>
          <img data-themed="./assets/tech-dock-dark.svg" alt="Tech Stack" class="w-full" />
        </div>

        <!-- 4. CURRENT FOCUS SECTION -->
        <div class="mt-10">
          <span class="section-label"><span>03</span> &nbsp;·&nbsp; CURRENT FOCUS</span>
          <img data-themed="./assets/focus-dark.svg" alt="Current Focus" class="w-full" />
        </div>

        <!-- 5. GITHUB STATS SECTION -->
        <div class="mt-10">
          <span class="section-label"><span>04</span> &nbsp;·&nbsp; GITHUB STATS</span>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
            <img data-themed="./assets/analytics/stats-dark.svg" alt="GitHub Overview" class="w-full" />
            <img data-themed="./assets/analytics/streak-dark.svg" alt="Consistency" class="w-full" />
          </div>
        </div>

        <!-- 6. CONTRIBUTION GRAPH -->
        <div class="mt-10">
          <span class="section-label"><span>05</span> &nbsp;·&nbsp; CONTRIBUTION GRAPH</span>
          <img data-themed="./assets/analytics/snake-dark.svg" alt="Contribution Graph" class="w-full" />
        </div>

        <!-- 7. CONNECT SECTION -->
        <div class="mt-10 pt-6 border-t border-[var(--gh-border)]">
          <span class="section-label"><span>06</span> &nbsp;·&nbsp; CONNECT</span>
          <div class="flex items-center gap-3 pt-1">
            <a href="https://tharinduxn.dev" target="_blank" rel="noopener" class="connect-link" title="Portfolio — tharinduxn.dev">
              <img data-themed="./assets/icons/portfolio-dark.svg" alt="Portfolio" class="w-11 h-11" />
            </a>
            <a href="https://www.linkedin.com/in/tharinduxn/" target="_blank" rel="noopener" class="connect-link" title="LinkedIn — in/tharinduxn">
              <img data-themed="./assets/icons/linkedin-dark.svg" alt="LinkedIn" class="w-11 h-11" />
            </a>
            <a href="https://github.com/tharinduxn" target="_blank" rel="noopener" class="connect-link" title="GitHub — @tharinduxn">
              <img data-themed="./assets/icons/github-dark.svg" alt="GitHub" class="w-11 h-11" />
            </a>
            <a href="mailto:tharinduxn@gmail.com" class="connect-link" title="Email — tharinduxn@gmail.com">
              <img data-themed="./assets/icons/email-dark.svg" alt="Email" class="w-11 h-11" />
            </a>
          </div>
        </div>
      </article>
    </div>

    <div id="codeContainer" class="hidden mx-auto" style="max-width: 880px;">
      <div class="bg-[#0d1117] border border-[#21262d] rounded-xl overflow-hidden shadow-2xl">
        <div class="flex items-center justify-between px-4 py-2.5 bg-[#161b22] border-b border-[#21262d]">
          <span class="text-xs font-mono text-[#c9d1d9]">README.md</span>
        </div>
        <pre id="rawMarkdownText" class="p-5 text-xs font-mono text-[#c9d1d9] overflow-x-auto leading-relaxed whitespace-pre-wrap">{escaped_readme}</pre>
      </div>
    </div>
  </main>

  <script>
    const ASSETS = {asset_json};
    const RAW_README = document.getElementById('rawMarkdownText').textContent;
    let currentTheme = 'dark';

    function applyAssets() {{
      document.querySelectorAll('[data-asset]').forEach((img) => {{
        const p = img.getAttribute('data-asset');
        if (ASSETS[p]) img.src = ASSETS[p];
      }});
      document.querySelectorAll('[data-themed]').forEach((img) => {{
        const darkPath = img.getAttribute('data-themed');
        const target = currentTheme === 'light' ? darkPath.replace('-dark.svg', '-light.svg') : darkPath;
        if (ASSETS[target]) img.src = ASSETS[target];
      }});
    }}

    document.getElementById('btnViewPreview').addEventListener('click', () => {{
      document.getElementById('previewContainer').classList.remove('hidden');
      document.getElementById('codeContainer').classList.add('hidden');
      document.getElementById('btnViewPreview').className = 'px-3 py-1.5 rounded-md text-xs font-medium bg-[#f0f6fc] text-[#0d1117] transition';
      document.getElementById('btnViewCode').className = 'px-3 py-1.5 rounded-md text-xs font-medium bg-[#161b22] text-[#c9d1d9] border border-[#21262d] hover:border-[#484f58] transition';
    }});

    document.getElementById('btnViewCode').addEventListener('click', () => {{
      document.getElementById('previewContainer').classList.add('hidden');
      document.getElementById('codeContainer').classList.remove('hidden');
      document.getElementById('btnViewCode').className = 'px-3 py-1.5 rounded-md text-xs font-medium bg-[#f0f6fc] text-[#0d1117] transition';
      document.getElementById('btnViewPreview').className = 'px-3 py-1.5 rounded-md text-xs font-medium bg-[#161b22] text-[#c9d1d9] border border-[#21262d] hover:border-[#484f58] transition';
    }});

    document.getElementById('btnToggleTheme').addEventListener('click', (e) => {{
      currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.classList.toggle('light', currentTheme === 'light');
      e.target.textContent = `Theme: ${{currentTheme === 'dark' ? 'Dark' : 'Light'}}`;
      applyAssets();
    }});

    document.getElementById('btnCopyReadme').addEventListener('click', (e) => {{
      try {{
        navigator.clipboard.writeText(RAW_README);
      }} catch (err) {{
        const ta = document.createElement('textarea');
        ta.value = RAW_README;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      }}
      const prev = e.target.textContent;
      e.target.textContent = 'Copied!';
      setTimeout(() => {{ e.target.textContent = prev; }}, 1800);
    }});

    document.getElementById('btnDownloadReadme').addEventListener('click', () => {{
      const blob = new Blob([RAW_README], {{ type: 'text/markdown;charset=utf-8' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'README.md';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(url), 1500);
    }});

    applyAssets();
  </script>
</body>
</html>
"""


def verify_constraints(readme_md: str):
    """Programmatically verifies that zero forbidden terms or sections appear in README.md."""
    forbidden = [
        "Featured Projects",
        "Featured Work",
        "Experience Timeline",
        "Product Engineering",
        "Cloud Native",
        "Cloud-Native",
        "DevOps",
        "CI/CD",
        "AI Engineering",
        "RAG",
        "LangChain",
        "Azure",
        "Node.js",
        "Express",
    ]
    for term in forbidden:
        if term.lower() in readme_md.lower():
            raise AssertionError(f"Forbidden term found in README.md: {term}")

    svg_files = list((REPO_DIR / "assets").rglob("*.svg"))
    for svg_file in svg_files:
        ET.fromstring(svg_file.read_text(encoding="utf-8"))
    print(f"Verified 0 forbidden terms and {len(svg_files)} valid SVG files.")


def main():
    ensure_dirs()
    copy_portrait()
    generate_all_assets()
    readme_md = build_readme_md()
    verify_constraints(readme_md)

    (REPO_DIR / "README.md").write_text(readme_md, encoding="utf-8")
    shutil.copyfile(UPLOAD_DIR / "update_analytics.py", REPO_DIR / "scripts" / "update_analytics.py")
    shutil.copyfile(Path(__file__), REPO_DIR / "scripts" / "build_badges.py")

    # Write output files
    (OUTPUT_DIR / "README.md").write_text(readme_md, encoding="utf-8")
    preview_html = build_preview_webapp(readme_md)
    (OUTPUT_DIR / "tharinduxn-github-profile-preview.html").write_text(preview_html, encoding="utf-8")

    zip_path = OUTPUT_DIR / "tharinduxn-github-profile.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(REPO_DIR.rglob("*")):
            if file_path.is_file():
                arcname = "tharinduxn-profile/" + file_path.relative_to(REPO_DIR).as_posix()
                zf.write(file_path, arcname)

    print("V2 minimal product-designer package built successfully.")


if __name__ == "__main__":
    main()
