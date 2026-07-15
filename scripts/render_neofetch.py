#!/usr/bin/env python3
"""Generate the info-only neofetch panel (assets/neofetch.svg).

The ASCII portrait is NOT baked in here — it lives as the animated
assets/portrait.gif (rendered by generate_ascii.py) and sits to the LEFT of
this panel in the README, because an animated GIF embedded inside an SVG won't
animate when GitHub renders the SVG as an <img>.

This panel is a single self-contained SVG (no markdown code blocks => no GitHub
'copy' buttons). Live fields carry <tspan data-k="..."> anchors so
scripts/update_stats.py can refresh them daily in CI (stdlib only, no photo).
"""
import os
import random

import update_stats as us  # single source of truth for stats + fortunes

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
OUT = os.path.join(REPO_DIR, "assets", "neofetch.svg")

# Theme (GitHub Dark / AI.OS)
BG, PANEL, BORDER = "#0D1117", "#161B22", "#30363D"
ACCENT, CYAN, PURPLE, GREEN = "#58A6FF", "#39D0FF", "#A371F7", "#3FB950"
TXT, DIM = "#C9D1D9", "#8B949E"

# Layout
PAD = 30
FONT, LH, CW = 15, 24, 9.0
LABEL_W = 104


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_svg(stats, fortune):
    info_x = PAD
    val_x = PAD + LABEL_W

    # (label, value, data-key) — label None = blank spacer row
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
    ]

    p = []           # svg body pieces
    ends = []        # rightmost pixel of each drawn line (for width calc)

    # Header
    hy = PAD + FONT
    p.append('<text class="i" x="%d" y="%d" font-weight="bold">'
             '<tspan fill="%s">vrathik</tspan><tspan fill="%s">@aios</tspan></text>'
             % (info_x, hy, ACCENT, CYAN))
    ends.append(info_x + 12 * CW)
    p.append('<text class="i" x="%d" y="%d" fill="%s">%s</text>' % (info_x, hy + LH, DIM, "─" * 24))
    ends.append(info_x + 24 * CW)

    # Info rows
    y = hy + LH * 2
    for label, value, key in info:
        if label is not None and value:
            p.append('<text class="i" x="%d" y="%d" fill="%s">%s</text>' % (info_x, y, ACCENT, esc(label)))
            inner = '<tspan data-k="%s">%s</tspan>' % (key, esc(value)) if key else esc(value)
            p.append('<text class="i" x="%d" y="%d" fill="%s">%s</text>' % (val_x, y, TXT, inner))
            ends.append(val_x + len(value) * CW)
        y += LH

    # Stats line
    y += LH // 2
    p.append(
        '<text class="i" x="%d" y="%d">'
        '<tspan fill="%s">Repos </tspan><tspan data-k="repos" fill="%s">%d</tspan>'
        '<tspan fill="%s">   Stars </tspan><tspan data-k="stars" fill="%s">%d</tspan>'
        '<tspan fill="%s">   Followers </tspan><tspan data-k="followers" fill="%s">%d</tspan>'
        '</text>' % (info_x, y, DIM, GREEN, stats["repos"], DIM, CYAN, stats["stars"],
                     DIM, PURPLE, stats["followers"])
    )
    ends.append(info_x + 34 * CW)

    # Fortune line + inline blinking cursor (tracks length after CI swaps it)
    y += LH + LH // 2
    p.append('<text class="i" x="%d" y="%d" fill="%s">❯ '
             '<tspan data-k="fortune" fill="%s">%s</tspan>'
             '<tspan class="cur" fill="%s"> █</tspan></text>'
             % (info_x, y, CYAN, DIM, esc(fortune), CYAN))
    # reserve width for the LONGEST fortune — CI swaps these daily and the
    # panel width is fixed at generation time.
    ends.append(info_x + (max(len(f) for f in us.FORTUNES) + 4) * CW)

    # Palette blocks
    y += LH
    for j, col in enumerate([BG, ACCENT, CYAN, GREEN, PURPLE, "#FFBD2E", "#FF5F56", TXT]):
        p.append('<rect x="%d" y="%d" width="28" height="15" rx="3" fill="%s" stroke="%s"/>'
                 % (info_x + j * 34, y - 12, col, BORDER))

    width = int(max(ends) + PAD)
    height = int(y + PAD)

    head = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
        'role="img" aria-label="vrathik@aios neofetch panel: AI Engineer in Computer Vision and '
        'Generative AI; stack PyTorch, CUDA, OpenCV, Diffusers; GitHub %d repos %d stars %d followers; '
        'contact github.com/vrathikshenoy, in/vrathik-shenoy, shenoyvrathik@gmail.com">'
        % (width, height, width, height, stats["repos"], stats["stars"], stats["followers"])
    )
    style = (
        "<style>"
        "text.i{font-family:ui-monospace,'JetBrains Mono','Fira Code',Menlo,Consolas,monospace;font-size:%dpx}"
        "@keyframes blink{0%%,50%%{opacity:1}51%%,100%%{opacity:0}}"
        ".cur{animation:blink 1.1s infinite}"
        "</style>" % FONT
    )
    frame = ('<rect x="0.5" y="0.5" width="%d" height="%d" rx="12" fill="%s" stroke="%s"/>'
             % (width - 1, height - 1, PANEL, BORDER)
             + '<rect x="9.5" y="9.5" width="%d" height="%d" rx="8" fill="%s" stroke="%s"/>'
             % (width - 19, height - 19, BG, BORDER))
    return head + style + frame + "".join(p) + "</svg>"


def main():
    svg = build_svg(us.fetch_stats(), random.choice(us.FORTUNES))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
