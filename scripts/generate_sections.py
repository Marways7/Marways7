"""Section headers, divider and footer — the connective tissue of the page.

Headers use a transparent background so they adapt to GitHub light/dark,
with mid-saturation gradient ink that stays legible on both.
"""

import math
import random

from svgtools import (ASSETS_DIR, MONO_STACK, PALETTE, SANS_STACK,
                      display_text, display_text_width, write_svg)

random.seed(7)
P = PALETTE

GRAD = ('<linearGradient id="ink" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#8B5CF6"/>'
        '<stop offset=".55" stop-color="#06B6D4"/>'
        '<stop offset="1" stop-color="#EC4899"/>'
        '</linearGradient>')

SECTIONS = [
    ("about",     "01", "ABOUT ME",           "关于我 · 数字世界的另一个我",   "#8B5CF6"),
    ("tech",      "02", "TECH ARSENAL",       "技术军火库 · 从想法到武器",     "#06B6D4"),
    ("analytics", "03", "GITHUB ANALYTICS",   "数据观测站 · 用数字讲故事",     "#EC4899"),
    ("projects",  "04", "FEATURED PROJECTS",  "精选项目 · 让想法落地生根",     "#8B5CF6"),
    ("activity",  "05", "CONTRIBUTION GALAXY", "贡献星图 · 每一格都是热爱",    "#06B6D4"),
    ("terminal",  "06", "TERMINAL",           "终端名片 · root@marways",      "#10B981"),
    ("connect",   "07", "CONNECT",            "联系我 · 一起创造点什么",       "#EC4899"),
]


def build_header(sid, index, title_en, subtitle, accent):
    W, H = 1100, 118
    cx = W / 2
    size = 40
    tw = display_text_width(title_en, size, 4)
    line_gap = tw / 2 + 44
    title = display_text(title_en, size, cx, 62, "url(#ink)", 4, "middle")
    ghost = display_text(index, 84, 60, 92, "none", 2, "start",
                         f'stroke="{accent}" stroke-width="1.6" opacity=".38"')
    ghost_r = display_text(index, 84, W - 60, 92, "none", 2, "end",
                           f'stroke="{accent}" stroke-width="1.6" opacity=".18"')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto" role="img" aria-label="{title_en}">
  <defs>
    <style>
      @keyframes sweep {{ 0% {{ transform:translateX(-260px); opacity:0; }} 15% {{ opacity:1; }} 85% {{ opacity:1; }} 100% {{ transform:translateX(260px); opacity:0; }} }}
      @keyframes spin {{ to {{ transform:rotate(360deg); }} }}
      @keyframes breathe {{ 0%,100% {{ opacity:.45; }} 50% {{ opacity:1; }} }}
      @keyframes dotTravelL {{ 0% {{ transform:translateX(0); opacity:0; }} 10% {{ opacity:1; }} 90% {{ opacity:1; }} 100% {{ transform:translateX({line_gap - 60:.0f}px); opacity:0; }} }}
      @keyframes dotTravelR {{ 0% {{ transform:translateX(0); opacity:0; }} 10% {{ opacity:1; }} 90% {{ opacity:1; }} 100% {{ transform:translateX(-{line_gap - 60:.0f}px); opacity:0; }} }}
    </style>
    {GRAD}
    <linearGradient id="lineL" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{accent}" stop-opacity="0"/>
      <stop offset="1" stop-color="{accent}" stop-opacity=".85"/>
    </linearGradient>
    <linearGradient id="lineR" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="{accent}" stop-opacity="0"/>
      <stop offset="1" stop-color="{accent}" stop-opacity=".85"/>
    </linearGradient>
    <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{accent}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{accent}"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="barClip"><rect x="{cx - 130:.0f}" y="78" width="260" height="4"/></clipPath>
  </defs>

  {ghost}{ghost_r}

  <line x1="130" y1="50" x2="{cx - line_gap:.0f}" y2="50" stroke="url(#lineL)" stroke-width="1.6"/>
  <line x1="{cx + line_gap:.0f}" y1="50" x2="{W - 130}" y2="50" stroke="url(#lineR)" stroke-width="1.6"/>
  <g style="animation:dotTravelL 3.2s ease-in-out infinite">
    <circle cx="150" cy="50" r="3" fill="{accent}"/>
  </g>
  <g style="animation:dotTravelR 3.2s ease-in-out 1.6s infinite">
    <circle cx="{W - 150}" cy="50" r="3" fill="{accent}"/>
  </g>

  <rect x="{cx - line_gap - 16:.0f}" y="44" width="12" height="12" fill="none" stroke="{accent}"
    stroke-width="1.6" transform="rotate(45 {cx - line_gap - 10:.0f} 50)"
    style="transform-origin:{cx - line_gap - 10:.0f}px 50px;animation:spin 8s linear infinite"/>
  <rect x="{cx + line_gap + 4:.0f}" y="44" width="12" height="12" fill="none" stroke="{accent}"
    stroke-width="1.6" transform="rotate(45 {cx + line_gap + 10:.0f} 50)"
    style="transform-origin:{cx + line_gap + 10:.0f}px 50px;animation:spin 8s linear infinite reverse"/>

  {title}

  <g clip-path="url(#barClip)">
    <rect x="{cx - 130:.0f}" y="78" width="260" height="3" rx="1.5" fill="url(#bar)"
      style="animation:sweep 3s ease-in-out infinite"/>
  </g>

  <text x="{cx}" y="106" text-anchor="middle" font-family="{SANS_STACK}" font-size="15"
    fill="#8B949E" letter-spacing="3" style="animation:breathe 4s ease-in-out infinite">{subtitle}</text>
</svg>
'''


for sid, index, en, sub, accent in SECTIONS:
    write_svg(ASSETS_DIR / f"section-{sid}.svg", build_header(sid, index, en, sub, accent))


# ------------------------------------------------------------------- divider
def build_divider():
    W, H = 1200, 30
    cy = H / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto" aria-hidden="true">
  <defs>
    <style>
      @keyframes flow {{ to {{ stroke-dashoffset:-144; }} }}
      @keyframes spark {{ 0% {{ transform:translateX(0); opacity:0; }} 8% {{ opacity:1; }} 92% {{ opacity:1; }} 100% {{ transform:translateX(480px); opacity:0; }} }}
      @keyframes sparkR {{ 0% {{ transform:translateX(0); opacity:0; }} 8% {{ opacity:1; }} 92% {{ opacity:1; }} 100% {{ transform:translateX(-480px); opacity:0; }} }}
      @keyframes pulse {{ 0%,100% {{ transform:scale(1); opacity:.9; }} 50% {{ transform:scale(1.35); opacity:.45; }} }}
    </style>
    <linearGradient id="dl" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8B5CF6" stop-opacity="0"/>
      <stop offset="1" stop-color="#06B6D4" stop-opacity=".8"/>
    </linearGradient>
    <linearGradient id="dr" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="#8B5CF6" stop-opacity="0"/>
      <stop offset="1" stop-color="#06B6D4" stop-opacity=".8"/>
    </linearGradient>
  </defs>
  <line x1="30" y1="{cy}" x2="560" y2="{cy}" stroke="url(#dl)" stroke-width="1.5" stroke-dasharray="10 8" style="animation:flow 4s linear infinite"/>
  <line x1="640" y1="{cy}" x2="{W - 30}" y2="{cy}" stroke="url(#dr)" stroke-width="1.5" stroke-dasharray="10 8" style="animation:flow 4s linear infinite reverse"/>
  <g style="animation:spark 5s ease-in-out infinite"><circle cx="60" cy="{cy}" r="2.6" fill="#67E8F9"/></g>
  <g style="animation:sparkR 5s ease-in-out 2.5s infinite"><circle cx="{W - 60}" cy="{cy}" r="2.6" fill="#A78BFA"/></g>
  <rect x="{W / 2 - 6}" y="{cy - 6}" width="12" height="12" fill="none" stroke="#8B5CF6" stroke-width="1.6"
    transform="rotate(45 {W / 2} {cy})" style="transform-origin:{W / 2}px {cy}px;animation:pulse 2.6s ease-in-out infinite"/>
  <circle cx="{W / 2}" cy="{cy}" r="2" fill="#EC4899"/>
</svg>
'''


write_svg(ASSETS_DIR / "neon-divider.svg", build_divider())


# -------------------------------------------------------------------- footer
def wave(amp, period, y0, w, step=16):
    pts = [f"M-10,{y0 + amp * math.sin(-10 / period * 2 * math.pi):.1f}"]
    for x in range(0, w + step, step):
        pts.append(f"L{x},{y0 + amp * math.sin(2 * math.pi * x / period):.1f}")
    return " ".join(pts)


def build_footer():
    W, H = 1280, 250
    cx = W / 2
    quote = display_text("IS TO BUILD IT.", 46, cx, 128, "url(#ink)", 4, "middle")
    sheen = display_text("IS TO BUILD IT.", 46, cx, 128, "url(#fsheen)", 4, "middle")

    stars = []
    for _ in range(45):
        x, y = random.uniform(10, W - 10), random.uniform(10, 150)
        stars.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(0.5, 1.6):.1f}" fill="#E6EDF3" '
            f'style="animation:twk {random.uniform(2, 6):.1f}s ease-in-out {random.uniform(0, 5):.1f}s infinite"/>')

    bubbles = []
    for i in range(10):
        x = random.uniform(80, W - 80)
        d, dl = random.uniform(5, 9), random.uniform(0, 8)
        bubbles.append(
            f'<circle cx="{x:.0f}" cy="235" r="{random.uniform(1.4, 2.6):.1f}" fill="#67E8F9" opacity="0" '
            f'style="animation:rise {d:.1f}s linear {dl:.1f}s infinite"/>')

    w1 = wave(12, 340, 185, W * 2)
    w2 = wave(16, 460, 198, W * 2)
    w3 = wave(10, 260, 212, W * 2)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto" role="img" aria-label="The best way to predict the future is to build it.">
  <defs>
    <style>
      @keyframes twk {{ 0%,100% {{ opacity:.12; }} 50% {{ opacity:.85; }} }}
      @keyframes drift1 {{ to {{ transform:translateX(-340px); }} }}
      @keyframes drift2 {{ to {{ transform:translateX(-460px); }} }}
      @keyframes drift3 {{ to {{ transform:translateX(-260px); }} }}
      @keyframes rise {{ 0% {{ transform:translateY(0); opacity:0; }} 12% {{ opacity:.8; }} 100% {{ transform:translateY(-150px); opacity:0; }} }}
      @keyframes breathe {{ 0%,100% {{ opacity:.55; }} 50% {{ opacity:1; }} }}
      .mono {{ font-family:{MONO_STACK}; }}
    </style>
    {GRAD}
    <linearGradient id="fbg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{P["bg_deep"]}"/>
      <stop offset="1" stop-color="#0B0820"/>
    </linearGradient>
    <linearGradient id="fsheen" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".47" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".5" stop-color="#fff" stop-opacity=".7"/>
      <stop offset=".53" stop-color="#fff" stop-opacity="0"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate" from="-{W} 0" to="{W} 0" dur="6s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="wv1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#8B5CF6" stop-opacity=".5"/>
      <stop offset="1" stop-color="#8B5CF6" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="wv2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#06B6D4" stop-opacity=".45"/>
      <stop offset="1" stop-color="#06B6D4" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="wv3" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#EC4899" stop-opacity=".38"/>
      <stop offset="1" stop-color="#EC4899" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="fframe"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>

  <g clip-path="url(#fframe)">
    <rect width="{W}" height="{H}" fill="url(#fbg)"/>
    {''.join(stars)}

    <text x="{cx}" y="72" text-anchor="middle" class="mono" font-size="15" fill="#8B949E"
      letter-spacing="4">// THE BEST WAY TO PREDICT THE FUTURE</text>
    {quote}{sheen}
    <text x="{cx}" y="160" text-anchor="middle" font-family="{SANS_STACK}" font-size="14"
      fill="#8B949E" letter-spacing="4" style="animation:breathe 4s ease-in-out infinite">预测未来的最好方式，就是亲手创造它</text>

    <g style="animation:drift1 9s linear infinite">
      <path d="{w1} L{W * 2},{H} L-10,{H} Z" fill="url(#wv1)"/>
    </g>
    <g style="animation:drift2 13s linear infinite">
      <path d="{w2} L{W * 2},{H} L-10,{H} Z" fill="url(#wv2)"/>
    </g>
    <g style="animation:drift3 7s linear infinite">
      <path d="{w3} L{W * 2},{H} L-10,{H} Z" fill="url(#wv3)"/>
    </g>
    {''.join(bubbles)}

    <text x="{cx}" y="{H - 16}" text-anchor="middle" class="mono" font-size="12.5"
      fill="#C9D1D9" letter-spacing="2">MADE WITH 💜 × ☕ × AI — MARWAYS7</text>
    <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none" stroke="#8B5CF6" stroke-opacity=".35" stroke-width="1.5"/>
  </g>
</svg>
'''


write_svg(ASSETS_DIR / "footer.svg", build_footer())
