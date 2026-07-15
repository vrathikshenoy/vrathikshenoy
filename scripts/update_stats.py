#!/usr/bin/env python3
"""Refresh the live fields in assets/neofetch.svg — uptime, GitHub stats and the
rotating fortune. Runs daily in CI (.github/workflows/update.yml).

STDLIB ONLY on purpose: no dependency install in CI, and it never needs the
source photo — the ASCII portrait is baked into the committed SVG by
render_neofetch.py. This script only rewrites the <tspan data-k="..."> anchors.
"""
import os
import re
import json
import random
import datetime
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
SVG = os.path.join(REPO_DIR, "assets", "neofetch.svg")
USERNAME = "vrathikshenoy"

FORTUNES = [
    "while(alive){ learn(); build(); ship(); }",
    "gradient descent writes programs we could never conceive.",
    "the best model is the one that ships.",
    "attention is all you need — and a good night's sleep.",
    "make the machine see, then make it think.",
    "a computer that deceives you into thinking it's human. — Turing",
]


def _get(url):
    headers = {"User-Agent": "aios-neofetch"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=15))


def fetch_stats():
    """Public GitHub API. Falls back to last-known values if unavailable."""
    fallback = {"repos": 32, "stars": 11, "followers": 2, "uptime": "7 years, 6 months"}
    try:
        u = _get(f"https://api.github.com/users/{USERNAME}")
        created = datetime.datetime.strptime(u["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        now = datetime.datetime.utcnow()
        months = (now.year - created.year) * 12 + (now.month - created.month)
        y, m = divmod(months, 12)
        stars = sum(r.get("stargazers_count", 0)
                    for r in _get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100"))
        return {"repos": u["public_repos"], "stars": stars,
                "followers": u["followers"], "uptime": f"{y} years, {m} months"}
    except Exception as e:  # noqa: BLE001 — offline/rate-limited is fine
        print("stats fetch failed, using fallback:", e)
        return fallback


def _esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def set_field(svg, key, value):
    return re.sub(r'(data-k="%s"[^>]*>).*?(</tspan>)' % re.escape(key),
                  lambda m: m.group(1) + _esc(value) + m.group(2), svg, count=1)


def main():
    with open(SVG, encoding="utf-8") as f:
        svg = f.read()
    stats = fetch_stats()
    for k in ("uptime", "repos", "stars", "followers"):
        svg = set_field(svg, k, stats[k])
    svg = set_field(svg, "fortune", random.choice(FORTUNES))
    with open(SVG, "w", encoding="utf-8") as f:
        f.write(svg)
    print("updated", SVG, "|", stats)


if __name__ == "__main__":
    main()
