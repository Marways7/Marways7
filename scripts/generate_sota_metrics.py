"""Live metrics board — assets/sota-metrics.svg.

Fetches real GitHub numbers (REST works unauthenticated; the contribution
count needs GITHUB_TOKEN and falls back gracefully without it), then renders
five glass stat tiles with staggered reveal animations.
"""

import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone
from urllib.error import HTTPError, URLError

from svgtools import (ASSETS_DIR, MONO_STACK, PALETTE, display_text,
                      write_svg)

P = PALETTE
GITHUB_USER = os.environ.get("GITHUB_USER", "Marways7")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
API = "https://api.github.com"
TIMEOUT = 20

DEFAULTS = {
    "repos": "12",
    "stars": "26",
    "commits": "260",
    "followers": "6",
    "since": "2023",
}

CONTRIB_QUERY = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    contributionsCollection(from:$from, to:$to) {
      contributionCalendar { totalContributions }
    }
  }
}
"""


def _headers():
    h = {"Accept": "application/vnd.github+json",
         "User-Agent": "Marways7-profile-generator",
         "X-GitHub-Api-Version": "2022-11-28"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h


def _get(url):
    req = urllib.request.Request(url, headers=_headers())
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _compact(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}".rstrip("0").rstrip(".") + "M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}".rstrip("0").rstrip(".") + "K"
    return str(n)


def fetch_metrics():
    metrics = DEFAULTS.copy()
    try:
        user = _get(f"{API}/users/{GITHUB_USER}")
        metrics["followers"] = _compact(int(user.get("followers", 0) or 0))
        created = user.get("created_at") or ""
        if len(created) >= 4:
            metrics["since"] = created[:4]

        repo_count = int(user.get("public_repos", 0) or 0)
        metrics["repos"] = _compact(repo_count)
        stars = 0
        for page in range(1, (repo_count // 100) + 2):
            repos = _get(f"{API}/users/{GITHUB_USER}/repos?per_page=100&type=owner&page={page}")
            stars += sum(r.get("stargazers_count", 0) for r in repos)
            if len(repos) < 100:
                break
        metrics["stars"] = _compact(stars)
    except (URLError, HTTPError, TimeoutError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"[metrics] REST fetch failed, using defaults: {exc}")

    if GITHUB_TOKEN:
        try:
            now = datetime.now(timezone.utc)
            payload = json.dumps({
                "query": CONTRIB_QUERY,
                "variables": {"login": GITHUB_USER,
                              "from": (now - timedelta(days=365)).isoformat(),
                              "to": now.isoformat()},
            }).encode("utf-8")
            req = urllib.request.Request(
                f"{API}/graphql", data=payload,
                headers={**_headers(), "Content-Type": "application/json"},
                method="POST")
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            total = (data.get("data", {}).get("user", {})
                     .get("contributionsCollection", {})
                     .get("contributionCalendar", {})
                     .get("totalContributions", 0))
            if total:
                metrics["commits"] = _compact(int(total))
        except (URLError, HTTPError, TimeoutError, json.JSONDecodeError, KeyError, TypeError) as exc:
            print(f"[metrics] GraphQL fetch failed, keeping default commits: {exc}")

    print(f"[metrics] {metrics}")
    return metrics


# ----------------------------------------------------------------- rendering
W, H = 1100, 250
TILE_W, TILE_H, GAP = 196, 168, 20
BOARD_X = (W - (TILE_W * 5 + GAP * 4)) / 2
TILE_Y = 46

ICONS = {
    # 16x16 octicon-style paths
    "repos": ('<path fill="{c}" fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8z"/>'),
    "stars": ('<path fill="{c}" fill-rule="evenodd" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"/>'),
    "commits": ('<path fill="{c}" d="M9.5 0 2.2 9.3h4.2L5.6 16l7.4-9.6H8.6L9.5 0z"/>'),
    "followers": ('<path fill="{c}" d="M5.5 3.5a2.5 2.5 0 115 0 2.5 2.5 0 01-5 0zM2 13.2C2 10.6 4.7 9 8 9s6 1.6 6 4.2c0 .5-.4.8-.9.8H2.9c-.5 0-.9-.3-.9-.8z"/>'),
    "since": ('<path fill="{c}" d="M8 0l1.8 6.2L16 8l-6.2 1.8L8 16 6.2 9.8 0 8l6.2-1.8L8 0z"/>'),
}

TILES = [
    ("repos", "REPOSITORIES", "仓库", P["violet_light"]),
    ("stars", "STARS EARNED", "星标", P["amber"]),
    ("commits", "COMMITS · 365D", "年度提交", P["cyan_light"]),
    ("followers", "FOLLOWERS", "关注者", P["pink"]),
    ("since", "VIBE SINCE", "启程之年", P["green"]),
]


def build_svg(metrics):
    tiles = []
    for i, (key, label, cjk, accent) in enumerate(TILES):
        x = BOARD_X + i * (TILE_W + GAP)
        delay = 0.35 * i
        value = metrics[key]
        num = display_text(str(value), 38, x + TILE_W / 2, TILE_Y + 92,
                           accent, 1.5, "middle")
        icon = ICONS[key].format(c=accent)
        tiles.append(f'''
  <g style="animation:tileIn .8s cubic-bezier(.2,.8,.2,1) {delay:.2f}s both">
    <g style="animation:floatTile 5.5s ease-in-out {delay:.2f}s infinite">
      <rect x="{x}" y="{TILE_Y}" width="{TILE_W}" height="{TILE_H}" rx="14"
        fill="#161B22" fill-opacity=".92" stroke="{P["violet"]}" stroke-opacity=".3" stroke-width="1.2"/>
      <path d="M {x + 14} {TILE_Y + 1.5} H {x + TILE_W - 14}" stroke="{accent}" stroke-opacity=".9"
        stroke-width="2.5" stroke-linecap="round"/>
      <g transform="translate({x + 16},{TILE_Y + 16}) scale(1.15)" opacity=".95">{icon}</g>
      <path d="M {x + TILE_W - 24} {TILE_Y + TILE_H - 8} h 16" stroke="{accent}" stroke-opacity=".55" stroke-width="2"/>
      <g style="animation:numGlow 3.4s ease-in-out {delay:.2f}s infinite">{num}</g>
      <text x="{x + TILE_W / 2}" y="{TILE_Y + 124}" text-anchor="middle" class="mono"
        font-size="11.5" letter-spacing="2" fill="{P["muted"]}">{label}</text>
      <text x="{x + TILE_W / 2}" y="{TILE_Y + 146}" text-anchor="middle" class="sans"
        font-size="11" letter-spacing="3" fill="{P["muted"]}" opacity=".75">{cjk}</text>
    </g>
  </g>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto" role="img" aria-label="Live GitHub metrics">
  <defs>
    <style>
      @keyframes tileIn {{ from {{ opacity:0; transform:translateY(22px); }} to {{ opacity:1; transform:translateY(0); }} }}
      @keyframes floatTile {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-5px); }} }}
      @keyframes numGlow {{ 0%,100% {{ filter:drop-shadow(0 0 2px rgba(103,232,249,.25)); }} 50% {{ filter:drop-shadow(0 0 9px rgba(139,92,246,.6)); }} }}
      @keyframes scan {{ 0% {{ transform:translateX(-220px); opacity:0; }} 10% {{ opacity:.6; }} 90% {{ opacity:.6; }} 100% {{ transform:translateX({W + 220}px); opacity:0; }} }}
      @keyframes breathe {{ 0%,100% {{ opacity:.5; }} 50% {{ opacity:1; }} }}
      .mono {{ font-family:{MONO_STACK}; }}
      .sans {{ font-family:-apple-system,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif; }}
    </style>
    <linearGradient id="scanG" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#67E8F9" stop-opacity="0"/>
      <stop offset=".5" stop-color="#67E8F9" stop-opacity=".14"/>
      <stop offset="1" stop-color="#67E8F9" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="hair" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8B5CF6" stop-opacity="0"/>
      <stop offset=".5" stop-color="#22D3EE" stop-opacity=".9"/>
      <stop offset="1" stop-color="#EC4899" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="board"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  </defs>

  <g clip-path="url(#board)">
    <rect width="{W}" height="{H}" fill="{P["bg_card"]}"/>
    <line x1="40" y1="24" x2="{W / 2 - 210}" y2="24" stroke="url(#hair)" stroke-width="1.4"/>
    <line x1="{W / 2 + 210}" y1="24" x2="{W - 40}" y2="24" stroke="url(#hair)" stroke-width="1.4"/>
    <text x="{W / 2}" y="29" text-anchor="middle" class="mono" font-size="12" letter-spacing="4"
      fill="{P["muted"]}"><tspan fill="{P["green"]}">●</tspan> LIVE TELEMETRY — 实时数据流</text>

    {''.join(tiles)}

    <rect x="0" y="0" width="200" height="{H}" fill="url(#scanG)"
      style="animation:scan 6.5s ease-in-out infinite"/>

    <path d="M 18 40 L 18 18 L 40 18" fill="none" stroke="{P["cyan"]}" stroke-width="2" opacity=".7"/>
    <path d="M {W - 18} {H - 40} L {W - 18} {H - 18} L {W - 40} {H - 18}" fill="none" stroke="{P["cyan"]}" stroke-width="2" opacity=".7"/>
    <circle cx="26" cy="{H - 24}" r="3" fill="{P["green"]}" style="animation:breathe 2.2s ease-in-out infinite"/>
    <text x="38" y="{H - 20}" class="mono" font-size="11" letter-spacing="2" fill="{P["muted"]}">SYNCED · EVERY 6H</text>
  </g>
  <rect x=".8" y=".8" width="{W - 1.6}" height="{H - 1.6}" rx="15" fill="none"
    stroke="{P["violet"]}" stroke-opacity=".38" stroke-width="1.5"/>
</svg>
'''


metrics = fetch_metrics()
write_svg(ASSETS_DIR / "sota-metrics.svg", build_svg(metrics))
