"""Featured project cards — assets/sota-project-N.svg.

Live stars / language come from the GitHub API (with graceful fallbacks),
rendered as glass HUD cards with animated gradient borders.
"""

import json
import urllib.request

from svgtools import (ASSETS_DIR, MONO_STACK, PALETTE, display_text,
                      display_text_width, esc, write_svg)

P = PALETTE
W, H = 420, 232

REPOS = [
    {
        "name": "Marways7/ECG_IdentificationX",
        "desc": ["Deep-learning ST-segment classification", "for biomedical ECG signals — SOTA accuracy."],
        "tag": "DEEP LEARNING",
        "accent": P["cyan_light"],
        "fallback_lang": "Python",
    },
    {
        "name": "Marways7/AiliaoX",
        "desc": ["Intelligent medical healthcare system.", "Bridging AI and real-world medicine."],
        "tag": "HEALTHCARE AI",
        "accent": P["pink"],
        "fallback_lang": "TypeScript",
    },
    {
        "name": "Marways7/DeepReadX",
        "desc": ["Autonomous research agent that reads,", "digests and distills insight from papers."],
        "tag": "AI AGENT",
        "accent": P["violet_light"],
        "fallback_lang": "Python",
    },
    {
        "name": "Marways7/cua_desktop_operator_skill",
        "desc": ["Computer-use automation via MCP —", "AI operating a full desktop, hands-free."],
        "tag": "MCP · AUTOMATION",
        "accent": P["green"],
        "fallback_lang": "Python",
    },
]

LANG_COLORS = {
    "Python": "#3572A5", "TypeScript": "#3178C6", "JavaScript": "#F1E05A",
    "MATLAB": "#E16737", "Jupyter Notebook": "#DA5B0B", "HTML": "#E34C26",
    "C++": "#F34B7D", "Go": "#00ADD8", "Rust": "#DEA584",
}

STAR_PATH = ("M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 "
             "1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 "
             "1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 "
             "01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z")


def fetch_repo(full_name, fallback_lang):
    url = f"https://api.github.com/repos/{full_name}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Marways7-profile-generator"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return (data.get("language") or fallback_lang,
                str(data.get("stargazers_count", 0)))
    except Exception as exc:  # noqa: BLE001 - offline fallback
        print(f"[projects] fetch failed for {full_name}: {exc}")
        return fallback_lang, "★"


def build_card(i, repo, lang, stars):
    accent = repo["accent"]
    short = repo["name"].split("/")[-1]
    tsize = 21
    while display_text_width(short, tsize, 0.5) > W - 130 and tsize > 11:
        tsize -= 1
    title = display_text(short, tsize, 52, 52, accent, 0.5, "start")
    lang_color = LANG_COLORS.get(lang, P["violet_light"])
    delay = i * 0.55
    d1, d2 = repo["desc"]

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto" role="img" aria-label="{esc(short)}">
  <defs>
    <style>
      @keyframes borderFlow {{ to {{ stroke-dashoffset:-320; }} }}
      @keyframes scanline {{ 0% {{ transform:translateY(-60px); }} 100% {{ transform:translateY({H + 20}px); }} }}
      @keyframes cardFloat {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-3px); }} }}
      @keyframes blinkDot {{ 0%,88%,100% {{ opacity:1; }} 92%,96% {{ opacity:.25; }} }}
      @keyframes chipPulse {{ 0%,100% {{ opacity:.75; }} 50% {{ opacity:1; }} }}
      @keyframes arrowNudge {{ 0%,100% {{ transform:translateX(0); }} 50% {{ transform:translateX(3px); }} }}
      @keyframes trace {{ to {{ stroke-dashoffset:-120; }} }}
      .mono {{ font-family:{MONO_STACK}; }}
    </style>
    <linearGradient id="cardBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0D1117"/>
      <stop offset="1" stop-color="#11182a"/>
    </linearGradient>
    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{accent}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{accent}" stop-opacity=".12"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="clip"><rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="14"/></clipPath>
  </defs>

  <g style="animation:cardFloat 6s ease-in-out {delay:.2f}s infinite">
    <g clip-path="url(#clip)">
      <rect x="4" y="4" width="{W - 8}" height="{H - 8}" fill="url(#cardBg)"/>
      <rect x="4" y="0" width="{W - 8}" height="48" fill="url(#scan)"
        style="animation:scanline 4.5s linear {delay:.2f}s infinite"/>
      <path d="M {W - 118} {H - 4} v -26 h 44 v -18 h 62" fill="none" stroke="{accent}"
        stroke-opacity=".28" stroke-width="1.3" stroke-dasharray="7 5"
        style="animation:trace 5s linear infinite"/>
      <circle cx="{W - 118}" cy="{H - 30}" r="2.2" fill="{accent}" opacity=".5"/>
    </g>

    <rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="14" fill="none"
      stroke="{P["violet"]}" stroke-opacity=".35" stroke-width="1.3"/>
    <rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="14" fill="none"
      stroke="{accent}" stroke-width="1.6" stroke-dasharray="46 114" stroke-opacity=".9"
      style="animation:borderFlow 7s linear infinite"/>

    <path d="M 16 34 L 16 16 L 34 16" fill="none" stroke="{accent}" stroke-width="2.2" opacity=".9"/>
    <path d="M {W - 16} {H - 34} L {W - 16} {H - 16} L {W - 34} {H - 16}" fill="none" stroke="{accent}" stroke-width="2.2" opacity=".9"/>

    <svg x="22" y="36" viewBox="0 0 16 16" width="20" height="20">
      <path fill="{accent}" fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8z"/>
    </svg>
    {title}

    <rect x="22" y="70" width="{display_text_width(repo["tag"], 10, 2) + 26:.0f}" height="20" rx="10"
      fill="{accent}" fill-opacity=".1" stroke="{accent}" stroke-opacity=".45" stroke-width="1"/>
    <text x="35" y="84" class="mono" font-size="10.5" letter-spacing="2" fill="{accent}">{esc(repo["tag"])}</text>

    <text x="24" y="122" class="mono" font-size="13" fill="{P["text"]}" opacity=".88">{esc(d1)}</text>
    <text x="24" y="143" class="mono" font-size="13" fill="{P["text"]}" opacity=".88">{esc(d2)}</text>

    <line x1="22" y1="{H - 62}" x2="{W - 22}" y2="{H - 62}" stroke="{P["violet"]}" stroke-opacity=".25" stroke-width="1"/>

    <circle cx="32" cy="{H - 38}" r="5.5" fill="{lang_color}" style="animation:blinkDot 4s ease-in-out infinite"/>
    <text x="45" y="{H - 33}" class="mono" font-size="12.5" font-weight="600" fill="{lang_color}">{esc(lang)}</text>

    <svg x="168" y="{H - 47}" viewBox="0 0 16 16" width="15" height="15">
      <path fill="{P["amber"]}" fill-rule="evenodd" d="{STAR_PATH}"/>
    </svg>
    <text x="189" y="{H - 33}" class="mono" font-size="12.5" font-weight="600" fill="{P["amber"]}">{esc(stars)}</text>

    <g style="animation:chipPulse 2.8s ease-in-out infinite">
      <rect x="{W - 126}" y="{H - 50}" width="104" height="26" rx="13"
        fill="{accent}" fill-opacity=".14" stroke="{accent}" stroke-opacity=".6" stroke-width="1.1"/>
      <text x="{W - 112}" y="{H - 32}" class="mono" font-size="11.5" letter-spacing="1" fill="{accent}">EXPLORE</text>
      <g style="animation:arrowNudge 1.6s ease-in-out infinite">
        <text x="{W - 40}" y="{H - 32}" class="mono" font-size="12.5" fill="{accent}">→</text>
      </g>
    </g>
  </g>
</svg>
'''


for i, repo in enumerate(REPOS):
    lang, stars = fetch_repo(repo["name"], repo["fallback_lang"])
    write_svg(ASSETS_DIR / f"sota-project-{i + 1}.svg", build_card(i, repo, lang, stars))
