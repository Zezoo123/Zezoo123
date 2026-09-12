#!/usr/bin/env python3
"""Generates self-hosted SVG assets for the profile README.

Nothing here calls an external service — the SVGs live in the profile repo, so
they render even when the free badge/stats hosts are down.
"""
import os

MONO = "ui-monospace, 'JetBrains Mono', 'SF Mono', SFMono-Regular, Menlo, Consolas, monospace"
SANS = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

ACCENT = "#38bdf8"
DIM = "#8b949e"
FAINT = "#4b5966"

os.makedirs("assets", exist_ok=True)


# --------------------------------------------------------------------------- header
def header():
    w, h = 1000, 220
    # broadcast arcs on the right
    arcs = []
    for i, r in enumerate((48, 76, 104)):
        arcs.append(
            f'<path d="M {w-168} {h/2-r} A {r} {r} 0 0 1 {w-168} {h/2+r}" '
            f'fill="none" stroke="{ACCENT}" stroke-width="1.5" opacity="0.30" stroke-linecap="round">'
            f'<animate attributeName="opacity" values="0.30;0.06;0.30" dur="3s" '
            f'begin="{i*0.4}s" repeatCount="indefinite"/></path>'
        )
    arcs = "\n    ".join(arcs)

    # typewriter tagline — same effect the readme-typing-svg service gives, but
    # self-hosted, so it can't break when that service is down
    lines = [
        "compliance infrastructure for emerging-market fintech",
        "desktop tooling that runs in production, unattended",
        "applied ML on messy financial data",
    ]
    slot = 4.5
    total = slot * len(lines)
    fs = 14.5
    adv = fs * 0.58  # monospace advance
    clips, typed = [], []
    for i, line in enumerate(lines):
        t0 = i * slot
        lw = len(line) * adv
        kt = lambda t: round(t / total, 4)
        clips.append(
            f'<clipPath id="type{i}"><rect x="56" y="162" height="22" width="0">'
            f'<animate attributeName="width" dur="{total}s" repeatCount="indefinite" '
            f'keyTimes="0;{kt(t0)};{kt(t0+1.3)};{kt(t0+3.9)};1" '
            f'values="0;0;{lw:.0f};{lw:.0f};0"/></rect></clipPath>'
        )
        # The cursor sits OUTSIDE the clip (inside it, it would be clipped away)
        # and its x travels with the reveal edge, so it leads the typing and
        # comes to rest against the last character.
        typed.append(
            f'<g opacity="0">'
            # discrete: the line must switch on at its slot, not fade in across the
            # whole cycle (linear interpolation ghosts the next line's cursor)
            f'<animate attributeName="opacity" dur="{total}s" repeatCount="indefinite" '
            f'calcMode="discrete" keyTimes="0;{kt(t0)};{kt(t0+4.0)};1" values="0;1;0;0"/>'
            f'<g clip-path="url(#type{i})">'
            # textLength pins the rendered width, so the cursor lands exactly at the
            # end of the line whatever monospace font the viewer's machine picks
            f'<text x="56" y="178" font-family="{MONO}" font-size="{fs}" fill="{DIM}" '
            f'textLength="{lw:.0f}" lengthAdjust="spacing">{line}</text></g>'
            f'<rect y="166" width="8" height="15" fill="{ACCENT}" x="56">'
            f'<animate attributeName="x" dur="{total}s" repeatCount="indefinite" '
            f'keyTimes="0;{kt(t0)};{kt(t0+1.3)};{kt(t0+3.9)};1" '
            f'values="56;56;{56+lw+4:.0f};{56+lw+4:.0f};56"/>'
            f'<animate attributeName="opacity" values="1;1;0;1" dur="1.1s" '
            f'begin="{t0+1.3}s" repeatCount="indefinite" calcMode="discrete"/>'
            f'</rect></g>'
        )
    clips = "\n    ".join(clips)
    typed = "\n    ".join(typed)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Zeyad Awadalla - software engineer. Compliance infrastructure for emerging-market fintech, desktop tooling that runs in production, applied ML on messy financial data.">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0b1017"/>
      <stop offset="55%" stop-color="#111d2b"/>
      <stop offset="100%" stop-color="#0b1017"/>
    </linearGradient>
    <radialGradient id="glow" cx="78%" cy="50%" r="55%">
      <stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{ACCENT}"/>
      <stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.1" fill="#ffffff" opacity="0.05"/>
    </pattern>
    <clipPath id="round"><rect width="{w}" height="{h}" rx="14"/></clipPath>
    {clips}
  </defs>

  <g clip-path="url(#round)">
    <rect width="{w}" height="{h}" fill="url(#bg)"/>
    <rect width="{w}" height="{h}" fill="url(#dots)"/>
    <rect width="{w}" height="{h}" fill="url(#glow)"/>
    {arcs}

    <text x="56" y="58" font-family="{MONO}" font-size="13" fill="{ACCENT}" opacity="0.85" letter-spacing="1.5">~/Zezoo123</text>

    <text x="54" y="122" font-family="{SANS}" font-size="52" font-weight="700" fill="#e8edf3" letter-spacing="-0.5">Zeyad Awadalla</text>

    <rect x="56" y="142" width="0" height="2" rx="1" fill="url(#rule)">
      <animate attributeName="width" from="0" to="300" dur="1.1s" fill="freeze" calcMode="spline" keySplines="0.2 0 0 1"/>
    </rect>

    {typed}

    <rect width="{w}" height="{h}" rx="14" fill="none" stroke="#ffffff" stroke-opacity="0.07"/>
  </g>
</svg>
"""


# ---------------------------------------------------------------------------- stack
def stack():
    rows = [
        ("languages", ["TypeScript", "Python", "JavaScript", "SQL", "Solidity"]),
        ("product", ["React", "Next.js", "Electron", "Expo", "Node", "Express", "Prisma", "PostgreSQL"]),
        ("data / ml", ["FastAPI", "Flask", "scikit-learn", "pandas", "Jupyter"]),
        ("tooling", ["Git", "GitHub Actions", "Vite", "Vitest", "Docker-free CI"]),
    ]
    rows[3] = ("tooling", ["Git", "GitHub Actions", "Vite", "Vitest"])

    w = 1000
    pad_x, label_w, row_h, top = 26, 120, 46, 26
    h = top * 2 + row_h * len(rows) - 12

    parts = []
    for ri, (label, items) in enumerate(rows):
        y = top + ri * row_h
        parts.append(
            f'<text x="{pad_x}" y="{y+21}" font-family="{MONO}" font-size="12.5" '
            f'fill="{FAINT}" letter-spacing="1.2">{label}</text>'
        )
        x = pad_x + label_w
        for item in items:
            pw = int(len(item) * 7.3) + 26
            parts.append(
                f'<g><rect x="{x}" y="{y}" width="{pw}" height="30" rx="7" fill="#121a24" '
                f'stroke="{ACCENT}" stroke-opacity="0.22"/>'
                f'<text x="{x+pw/2}" y="{y+20}" font-family="{MONO}" font-size="12.5" '
                f'fill="#c3ced9" text-anchor="middle">{item}</text></g>'
            )
            x += pw + 9

    body = "\n    ".join(parts)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Tech stack">
  <defs>
    <linearGradient id="sbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0b1017"/>
      <stop offset="100%" stop-color="#0e1620"/>
    </linearGradient>
    <clipPath id="sround"><rect width="{w}" height="{h}" rx="14"/></clipPath>
  </defs>
  <g clip-path="url(#sround)">
    <rect width="{w}" height="{h}" fill="url(#sbg)"/>
    {body}
    <rect width="{w}" height="{h}" rx="14" fill="none" stroke="#ffffff" stroke-opacity="0.07"/>
  </g>
</svg>
"""


for name, svg in (("header.svg", header()), ("stack.svg", stack())):
    with open(f"assets/{name}", "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote assets/" + name, len(svg), "bytes")
