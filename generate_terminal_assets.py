#!/usr/bin/env python3
"""Terminal-look SVGs for the profile README.

GitHub does NOT render ANSI escape codes in markdown code fences — it prints the
raw bytes. So the terminal look is drawn as SVG instead and hosted in the repo.

The block letters are drawn as rectangles, not text, so they can't break on a
machine that lacks box-drawing glyphs in its monospace font.
"""
import os

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', monospace"

BG = "#0d1117"
BAR = "#161b22"
FG = "#c9d1d9"
DIM = "#8b949e"
FAINT = "#6e7681"
GREEN = "#7ee787"
CYAN = "#38bdf8"
AMBER = "#e3b341"

os.makedirs("assets", exist_ok=True)

# 5x7 block font, hand-drawn so it needs no font on the viewer's machine
GLYPHS = {
    "Z": ["11111", "....1", "...1.", "..1..", ".1...", "1....", "11111"],
    "E": ["11111", "1....", "1....", "1111.", "1....", "1....", "11111"],
    "Y": ["1...1", "1...1", ".1.1.", "..1..", "..1..", "..1..", "..1.."],
    "A": [".111.", "1...1", "1...1", "11111", "1...1", "1...1", "1...1"],
    "D": ["1111.", "1...1", "1...1", "1...1", "1...1", "1...1", "1111."],
    "O": [".111.", "1...1", "1...1", "1...1", "1...1", "1...1", ".111."],
}


def chrome(w, h, title):
    """Window frame: returns (defs_extra, body_prefix)."""
    dots = "".join(
        f'<circle cx="{22 + i*19}" cy="20" r="6" fill="{c}"/>'
        for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840"))
    )
    return f"""  <g clip-path="url(#clip)">
    <rect width="{w}" height="{h}" fill="{BG}"/>
    <rect width="{w}" height="40" fill="{BAR}"/>
    <line x1="0" y1="40" x2="{w}" y2="40" stroke="#ffffff" stroke-opacity="0.07"/>
    {dots}
    <text x="{w/2}" y="25" font-family="{MONO}" font-size="12.5" fill="{FAINT}" text-anchor="middle">{title}</text>"""


def led_word(word, x, y, cell=15, gap=1.6):
    """Block letters as rects — no font dependency."""
    out = []
    cx = x
    for ch in word:
        rows = GLYPHS[ch]
        for r, row in enumerate(rows):
            run = 0
            for c in range(len(row) + 1):
                filled = c < len(row) and row[c] == "1"
                if filled:
                    run += 1
                    continue
                if run:
                    rx = cx + (c - run) * cell
                    out.append(
                        f'<rect x="{rx:.1f}" y="{y + r*cell:.1f}" '
                        f'width="{run*cell - gap:.1f}" height="{cell - gap:.1f}" rx="1.5"/>'
                    )
                    run = 0
        cx += 5 * cell + cell * 1.4
    width = cx - cell * 1.4 - x
    return "\n      ".join(out), width


def terminal_header():
    w, h = 1000, 326
    cell = 17
    blocks, _ = led_word("ZEZO", 0, 0, cell=cell)
    bx, by = 58, 108

    info = [
        ("zezo", "@github", None),
        ("rule", None, None),
        ("role", "Software Engineer", None),
        ("education", "BSc Computer Science, Manchester", None),
        ("focus", "compliance infra · desktop tooling · ML", None),
        ("building", "CorridorComply", "KYC/AML for remittance corridors"),
        ("shipping", "Radio", "playout scheduling, used daily"),
        ("stack", "TypeScript · Python · React · FastAPI", None),
    ]

    ix, iy, lh = 512, 96, 25
    key_w = 96
    out = []
    for i, (k, v, note) in enumerate(info):
        y = iy + i * lh
        if k == "rule":
            out.append(
                f'<line x1="{ix}" y1="{y-8}" x2="{ix+430}" y2="{y-8}" '
                f'stroke="#ffffff" stroke-opacity="0.10"/>'
            )
            continue
        if i == 0:
            out.append(
                f'<text x="{ix}" y="{y}" font-family="{MONO}" font-size="14" font-weight="700" '
                f'fill="{CYAN}">{k}<tspan fill="{DIM}" font-weight="400">{v}</tspan></text>'
            )
            continue
        line = (
            f'<text y="{y}" font-family="{MONO}" font-size="13">'
            f'<tspan x="{ix}" fill="{FAINT}">{k}</tspan>'
            f'<tspan x="{ix+key_w}" fill="{FG}">{v}</tspan>'
        )
        if note:
            line += f'<tspan fill="{FAINT}">  {note}</tspan>'
        out.append(line + "</text>")
    info_block = "\n    ".join(out)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="zezo@github — software engineer. Compliance infrastructure, desktop tooling, applied ML. BSc Computer Science, Manchester.">
  <defs>
    <clipPath id="clip"><rect width="{w}" height="{h}" rx="12"/></clipPath>
    <linearGradient id="led" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0%" stop-color="#22d3ee"/>
      <stop offset="55%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#6366f1"/>
    </linearGradient>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
  </defs>
{chrome(w, h, "zezo@github: ~")}

    <text x="28" y="72" font-family="{MONO}" font-size="14" fill="{FG}"><tspan fill="{GREEN}">$</tspan> neofetch</text>

    <g transform="translate({bx},{by})" fill="url(#led)" opacity="0.5" filter="url(#glow)">
      {blocks}
    </g>
    <g transform="translate({bx},{by})" fill="url(#led)">
      {blocks}
    </g>
    <text x="{bx+3}" y="{by+7*cell+27}" font-family="{MONO}" font-size="12.5" fill="{FAINT}" letter-spacing="2.2">ZEYAD AWADALLA</text>

    {info_block}

    <text x="28" y="{h-20}" font-family="{MONO}" font-size="14" fill="{FG}"><tspan fill="{GREEN}">$</tspan> <tspan fill="{CYAN}">█<animate attributeName="fill-opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite" calcMode="discrete"/></tspan></text>

    <rect width="{w}" height="{h}" rx="12" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>
  </g>
</svg>
"""


def projects_panel():
    rows = [
        ("corridorcomply/", "python · fastapi", "corridor-specific KYC/AML + sanctions screening"),
        ("radio/", "electron · react · ts", "playout logs for BSI Simian Pro, in daily use"),
        ("defi-arbitrage/", "flask · lstm · sklearn", "arbitrage detection + price forecasting"),
        ("handyman/", "next · expo · prisma", "home-services marketplace, monorepo"),
        ("nlu_group1/", "jupyter · nlp", "natural language understanding, group project"),
        ("portfolio/", "typescript", "personal site, built from scratch"),
    ]
    w = 1000
    top = 72
    lh = 26
    h = top + lh * len(rows) + 46

    # fixed column x positions so alignment never depends on font metrics
    col_perm, col_name, col_stack, col_desc = 28, 132, 288, 468

    lines = [
        f'<text x="28" y="70" font-family="{MONO}" font-size="14" fill="{FG}">'
        f'<tspan fill="{GREEN}">$</tspan> ls -la ~/projects</text>'
    ]
    for i, (name, stack, desc) in enumerate(rows):
        y = top + 26 + i * lh
        lines.append(
            f'<text y="{y}" font-family="{MONO}" font-size="13.5">'
            f'<tspan x="{col_perm}" fill="{FAINT}">drwxr-xr-x</tspan>'
            f'<tspan x="{col_name}" fill="{CYAN}" font-weight="600">{name}</tspan>'
            f'<tspan x="{col_stack}" fill="{AMBER}">{stack}</tspan>'
            f'<tspan x="{col_desc}" fill="{DIM}">{desc}</tspan></text>'
        )
    lines.append(
        f'<text x="28" y="{h-18}" font-family="{MONO}" font-size="14" fill="{FG}">'
        f'<tspan fill="{GREEN}">$</tspan> <tspan fill="{CYAN}">█'
        f'<animate attributeName="fill-opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite" calcMode="discrete"/>'
        f'</tspan></text>'
    )
    body = "\n    ".join(lines)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Project listing: CorridorComply, Radio, DeFi arbitrage tool, Handyman, nlu_group1, Portfolio">
  <defs>
    <clipPath id="clip"><rect width="{w}" height="{h}" rx="12"/></clipPath>
  </defs>
{chrome(w, h, "zezo@github: ~/projects")}
    {body}
    <rect width="{w}" height="{h}" rx="12" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>
  </g>
</svg>
"""


for name, svg in (("terminal.svg", terminal_header()), ("projects.svg", projects_panel())):
    with open(f"assets/{name}", "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote assets/" + name, len(svg), "bytes")
