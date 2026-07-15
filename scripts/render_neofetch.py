#!/usr/bin/env python3
"""Generate ONE neofetch-style panel SVG (assets/neofetch.svg).

ASCII portrait (left) + neofetch info (right) in a single self-contained SVG —
the whole profile is this one image, so there are no markdown code blocks and
thus no GitHub 'copy' buttons. Live fields (uptime, stats, fortune) are wrapped
in <tspan data-k="..."> anchors so scripts/update_stats.py can refresh them in
CI via regex WITHOUT needing the source photo (the ASCII is baked in here).

Run locally (needs the source photo) whenever the photo or layout changes.
"""
import os
import random

import generate_ascii as ga  # reuse preprocess_image + compute_ascii_grid
import update_stats as us     # single source of truth for stats + fortunes

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
OUT = os.path.join(REPO_DIR, "assets", "neofetch.svg")
USERNAME = "vrathikshenoy"

# Theme (GitHub Dark / AI.OS)
BG, PANEL, BORDER = "#0D1117", "#161B22", "#30363D"
ACCENT, CYAN, PURPLE, GREEN = "#58A6FF", "#39D0FF", "#A371F7", "#3FB950"
TXT, DIM = "#C9D1D9", "#8B949E"

# ASCII char -> colour (edges bright, shading dim = depth)
EDGE, BRIGHT, MID, SHADE = "#58A6FF", "#39D0FF", "#2f6f9f", "#24435c"

# Layout
PAD = 30
ASC_FONT, ASC_LH, ASC_CW = 12, 19, 7.2
INFO_FONT, INFO_LH = 14, 23
COL_GAP = 40
LABEL_W = 92
ASCII_COLS = 40


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def ascii_color(c):
    if c in "|/\\":
        return EDGE
    if c in "@%#*":
        return BRIGHT
    if c in "+=-":
        return MID
    return SHADE


def build_svg(grid, stats, fortune):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    ascii_w = cols * ASC_CW
    ascii_h = rows * ASC_LH

    info_x = PAD + ascii_w + COL_GAP
    val_x = info_x + LABEL_W

    # (label, value, data-key) — label None = section spacer
    info = [
        ("OS", 'AI.OS 2.0 "Latent Space"', None),
        ("Host", "Computer Vision · Generative AI", None),
        ("Kernel", "6.13-neural-cuda", None),
        ("Uptime", stats["uptime"], "uptime"),
        ("Shell", "zsh · python 3.12", None),
        ("Role", "AI Engineer", None),
        ("Editor", "Neovim · VS Code", None),
        (None, "", None),
        ("Stack", "PyTorch · CUDA · OpenCV · Diffusers", None),
        ("Focus", "Latent Diffusion · VTON · VLMs", None),
        ("Projects", "wearify ●  ·  gemini-vton ○", None),
        (None, "", None),
        ("GitHub", "github.com/vrathikshenoy", None),
        ("LinkedIn", "in/vrathik-shenoy", None),
        ("Email", "shenoyvrathik@gmail.com", None),
        (None, "", None),
    ]

    header_h = INFO_LH * 2  # user@host + rule
    info_h = header_h + len(info) * INFO_LH + INFO_LH * 2  # + stats + fortune
    body_h = max(ascii_h, info_h)
    palette_h = 34
    width = int(val_x + 320 + PAD)
    height = int(PAD + body_h + palette_h + PAD)

    p = []
    p.append(
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
        'role="img" aria-label="vrathik@aios neofetch: AI Engineer in Computer Vision and Generative AI, '
        'GitHub %d repos %d stars %d followers, contact github.com/vrathikshenoy">'
        % (width, height, width, height, stats["repos"], stats["stars"], stats["followers"])
    )
    p.append(
        "<style>"
        "text{font-family:ui-monospace,'JetBrains Mono','Fira Code',Menlo,Consolas,monospace}"
        ".a{font-size:%dpx}.i{font-size:%dpx}"
        "@keyframes blink{0%%,49%%{opacity:1}50%%,100%%{opacity:0}}"
        ".cur{animation:blink 1.1s steps(1) infinite}"
        "</style>" % (ASC_FONT, INFO_FONT)
    )
    # Panel
    p.append('<rect x="0.5" y="0.5" width="%d" height="%d" rx="12" fill="%s" stroke="%s"/>'
             % (width - 1, height - 1, PANEL, BORDER))
    p.append('<rect x="10.5" y="10.5" width="%d" height="%d" rx="8" fill="%s" stroke="%s"/>'
             % (width - 21, height - 21, BG, BORDER))

    # ASCII portrait (left), coloured per char, runs merged by colour
    for r, row in enumerate(grid):
        y = PAD + r * ASC_LH + ASC_FONT
        spans, cur, buf = [], None, ""
        for ch in row:
            col = ascii_color(ch) if ch != " " else (cur or SHADE)
            if col != cur and buf:
                spans.append('<tspan fill="%s">%s</tspan>' % (cur, esc(buf)))
                buf = ""
            cur = col
            buf += ch
        if buf:
            spans.append('<tspan fill="%s">%s</tspan>' % (cur, esc(buf)))
        p.append('<text class="a" x="%d" y="%.1f" xml:space="preserve">%s</text>'
                 % (PAD, y, "".join(spans)))

    # Info header
    hy = PAD + INFO_FONT
    p.append('<text class="i" x="%d" y="%d" font-weight="bold">'
             '<tspan fill="%s">vrathik</tspan><tspan fill="%s">@aios</tspan></text>'
             % (info_x, hy, ACCENT, CYAN))
    p.append('<text class="i" x="%d" y="%d" fill="%s">%s</text>'
             % (info_x, hy + INFO_LH, DIM, "─" * 22))

    # Info rows
    y = hy + INFO_LH * 2
    for label, value, key in info:
        if label is not None and value:
            p.append('<text class="i" x="%d" y="%d" fill="%s">%s</text>' % (info_x, y, ACCENT, esc(label)))
            inner = esc(value)
            if key:
                inner = '<tspan data-k="%s">%s</tspan>' % (key, esc(value))
            p.append('<text class="i" x="%d" y="%d" fill="%s">%s</text>' % (val_x, y, TXT, inner))
        y += INFO_LH

    # Stats line
    p.append(
        '<text class="i" x="%d" y="%d">'
        '<tspan fill="%s">Repos </tspan><tspan data-k="repos" fill="%s">%d</tspan>'
        '<tspan fill="%s">   Stars </tspan><tspan data-k="stars" fill="%s">%d</tspan>'
        '<tspan fill="%s">   Followers </tspan><tspan data-k="followers" fill="%s">%d</tspan>'
        '</text>' % (info_x, y, DIM, GREEN, stats["repos"], DIM, CYAN, stats["stars"],
                     DIM, PURPLE, stats["followers"])
    )
    y += INFO_LH * 2

    # Fortune prompt line (full width, bottom). Cursor is an inline tspan so it
    # tracks the fortune length even after CI swaps the text.
    p.append('<text class="i" x="%d" y="%d" fill="%s">❯ '
             '<tspan data-k="fortune" fill="%s">%s</tspan>'
             '<tspan class="cur" fill="%s"> █</tspan></text>'
             % (PAD, y, CYAN, DIM, esc(fortune), CYAN))

    # Palette blocks
    py = height - PAD - 14
    for j, col in enumerate([BG, EDGE, CYAN, GREEN, PURPLE, "#FFBD2E", "#FF5F56", TXT]):
        p.append('<rect x="%d" y="%d" width="26" height="14" rx="3" fill="%s" stroke="%s"/>'
                 % (info_x + j * 32, py, col, BORDER))

    p.append("</svg>")
    return "".join(p)


def main():
    img = ga.preprocess_image(ga.SOURCE_IMG, target_width=ASCII_COLS)
    grid, _, _ = ga.compute_ascii_grid(img)
    stats = us.fetch_stats()
    fortune = random.choice(us.FORTUNES)
    svg = build_svg(grid, stats, fortune)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", OUT, "| stats:", stats)


if __name__ == "__main__":
    main()
