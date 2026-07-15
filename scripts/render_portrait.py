#!/usr/bin/env python3
"""Render the animated ASCII portrait as a self-contained SVG (assets/portrait.svg).

Why SVG instead of a GIF: the desired behaviour is "reveal once, hold, then let
the background breathe forever". A GIF loop is all-or-nothing (it would re-play
the reveal every cycle). An <img>-embedded SVG can freeze the reveal
(animation-fill forwards) and run an independent, infinite breathing loop — and
it's crisp vector text at any size. Run locally (needs the source photo).
"""
import os

import generate_ascii as ga  # reuse preprocess_image + compute_ascii_grid

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
OUT = os.path.join(REPO_DIR, "assets", "portrait.svg")

BG = "#0D1117"
COLS = 80
FONT, CW, LH = 10, 6.0, 12
PAD = 16

REVEAL_STEP = 0.05   # s between row reveals (top -> bottom)
ROW_DUR = 0.6        # s per-row fade


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def color(c):
    # Higher-contrast ramp: near-white highlights -> faint blue shadows.
    if c in "@%#":
        return "#EAF4FF"
    if c == "*":
        return "#B7E5FF"
    if c in "|/\\":
        return "#39D0FF"
    if c in "+=":
        return "#3B82F6"
    if c == "-":
        return "#2F6FEB"
    if c == ":":
        return "#245C8C"
    if c == ".":
        return "#1E4A73"
    return "#173352"


def row_spans(row):
    spans, cur, buf = [], None, ""
    for ch in row:
        col = color(ch) if ch != " " else (cur or "#173352")
        if col != cur and buf:
            spans.append('<tspan fill="%s">%s</tspan>' % (cur, esc(buf)))
            buf = ""
        cur = col
        buf += ch
    if buf:
        spans.append('<tspan fill="%s">%s</tspan>' % (cur, esc(buf)))
    return "".join(spans)


def main():
    img = ga.preprocess_image(ga.SOURCE_IMG, target_width=COLS)
    grid, _, _ = ga.compute_ascii_grid(img)
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    width = int(cols * CW + 2 * PAD)
    status_y = PAD + rows * LH + LH + 4
    height = int(status_y + PAD)

    reveal_end = (rows - 1) * REVEAL_STEP + ROW_DUR
    breathe_start = reveal_end + 0.2

    p = []
    p.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
             'role="img" aria-label="Animated ASCII portrait of Vrathik Shenoy">'
             % (width, height, width, height))
    # NOTE: one single format string (implicit concatenation, no '+') so every
    # '%%' collapses to a literal '%'. Building this with '+' left '%%' intact in
    # the non-formatted pieces, producing invalid '0%%' keyframe selectors that
    # silently killed the breathe + blink animations.
    p.append(
        "<style>"
        "text{font-family:ui-monospace,'JetBrains Mono',Menlo,Consolas,monospace;font-size:%dpx;white-space:pre}"
        "@keyframes rowin{from{opacity:0}to{opacity:1}}"
        ".r{opacity:0;animation:rowin %ss ease-out forwards}"
        "@keyframes breathe{0%%,100%%{opacity:1}50%%{opacity:0.6}}"
        ".breath{animation:breathe 4.5s ease-in-out infinite;animation-delay:%ss}"
        "@keyframes blink{0%%,50%%{opacity:1}51%%,100%%{opacity:0}}"
        ".cur{animation:blink 1.1s infinite}"
        "</style>" % (FONT, ROW_DUR, round(breathe_start, 2))
    )
    p.append('<rect x="0.5" y="0.5" width="%d" height="%d" rx="8" fill="%s" stroke="#30363D"/>'
             % (width - 1, height - 1, BG))

    # Portrait rows, revealed top->bottom (freeze), inside a breathing group
    p.append('<g class="breath">')
    for r, row in enumerate(grid):
        y = PAD + (r + 1) * LH
        p.append('<text class="r" style="animation-delay:%ss" x="%d" y="%d" xml:space="preserve">%s</text>'
                 % (round(r * REVEAL_STEP, 2), PAD, y, row_spans(row)))
    p.append("</g>")

    # Status line fades in after the reveal, steady (not breathing), with cursor
    p.append('<text class="r" style="animation-delay:%ss" x="%d" y="%d" fill="#39D0FF">'
             '❯ system ready <tspan class="cur" fill="#39D0FF">█</tspan></text>'
             % (round(reveal_end, 2), PAD, status_y))

    p.append("</svg>")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("".join(p))
    print("wrote %s (%dx%d, reveal %.1fs, breathe from %.1fs)" % (OUT, width, height, reveal_end, breathe_start))


if __name__ == "__main__":
    main()
