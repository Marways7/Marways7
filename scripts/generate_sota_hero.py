"""AURORA CYBERPUNK hero banner — assets/sota-hero.svg.

All display typography is baked to vector paths (see svgtools), so the
banner renders identically inside GitHub's sandboxed <img> pipeline.
"""

import math
import random

from svgtools import (ASSETS_DIR, MONO_STACK, PALETTE, display_text,
                      display_text_width, write_svg)

random.seed(2077)  # deterministic output → no diff churn on scheduled runs

W, H = 1280, 420
CX = W / 2
P = PALETTE

parts = []

# ---------------------------------------------------------------- defs / css
parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto" role="img" aria-label="Marways — Vibe Coder and AI Builder">
  <defs>
    <style>
      @keyframes twinkle {{ 0%,100% {{ opacity:.15; }} 50% {{ opacity:.9; }} }}
      @keyframes floaty  {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-8px); }} }}
      @keyframes auroraA {{ 0%,100% {{ transform:translate(0,0) scale(1); }} 50% {{ transform:translate(60px,18px) scale(1.15); }} }}
      @keyframes auroraB {{ 0%,100% {{ transform:translate(0,0) scale(1.1); }} 50% {{ transform:translate(-70px,-14px) scale(0.95); }} }}
      @keyframes auroraC {{ 0%,100% {{ transform:translate(0,0); }} 50% {{ transform:translate(30px,-24px); }} }}
      @keyframes shoot {{
        0%   {{ transform:translate(0,0); opacity:0; }}
        6%   {{ opacity:.9; }}
        22%  {{ transform:translate(-460px,300px); opacity:0; }}
        100% {{ transform:translate(-460px,300px); opacity:0; }}
      }}
      @keyframes gridFall {{
        0%   {{ transform:translateY(0); opacity:0; }}
        12%  {{ opacity:.55; }}
        100% {{ transform:translateY(115px); opacity:0; }}
      }}
      @keyframes spin    {{ to {{ transform:rotate(360deg); }} }}
      @keyframes spinRev {{ to {{ transform:rotate(-360deg); }} }}
      @keyframes cursorBlink {{ 0%,49% {{ opacity:1; }} 50%,100% {{ opacity:0; }} }}
      @keyframes glitch {{
        0%,93%,100% {{ transform:translate(0,0); opacity:0; }}
        94%  {{ transform:translate(-5px,2px); opacity:.55; }}
        95%  {{ transform:translate(4px,-2px); opacity:.4; }}
        96%  {{ transform:translate(-3px,1px); opacity:.5; }}
        97%  {{ transform:translate(0,0); opacity:0; }}
      }}
      @keyframes waveSlide  {{ to {{ transform:translateX(-320px); }} }}
      @keyframes waveSlide2 {{ to {{ transform:translateX(-440px); }} }}
      @keyframes phrase1 {{ 0%,4% {{opacity:0;}} 7%,29% {{opacity:1;}} 32%,100% {{opacity:0;}} }}
      @keyframes phrase2 {{ 0%,37% {{opacity:0;}} 40%,62% {{opacity:1;}} 65%,100% {{opacity:0;}} }}
      @keyframes phrase3 {{ 0%,70% {{opacity:0;}} 73%,95% {{opacity:1;}} 98%,100% {{opacity:0;}} }}
      @keyframes breathe {{ 0%,100% {{ opacity:.5; }} 50% {{ opacity:1; }} }}
      @keyframes dashFlow {{ to {{ stroke-dashoffset:-200; }} }}

      .mono {{ font-family:{MONO_STACK}; }}
      .star {{ fill:#E6EDF3; }}
      .hud  {{ fill:none; stroke:{P["cyan"]}; stroke-width:2; opacity:.65; }}
    </style>

    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{P["bg_deep"]}"/>
      <stop offset=".55" stop-color="{P["bg_mid"]}"/>
      <stop offset="1" stop-color="#060B18"/>
    </linearGradient>

    <radialGradient id="blobViolet" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{P["violet"]}" stop-opacity=".34"/>
      <stop offset="1" stop-color="{P["violet"]}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="blobCyan" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{P["cyan"]}" stop-opacity=".26"/>
      <stop offset="1" stop-color="{P["cyan"]}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="blobPink" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{P["pink"]}" stop-opacity=".2"/>
      <stop offset="1" stop-color="{P["pink"]}" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{P["cyan_light"]}"/>
      <stop offset=".35" stop-color="{P["violet_light"]}"/>
      <stop offset=".7" stop-color="{P["violet"]}"/>
      <stop offset="1" stop-color="{P["pink"]}"/>
    </linearGradient>

    <linearGradient id="sheen" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".46" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".5" stop-color="#fff" stop-opacity=".85"/>
      <stop offset=".54" stop-color="#fff" stop-opacity="0"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate"
        from="-{W} 0" to="{W} 0" dur="5.5s" repeatCount="indefinite"/>
    </linearGradient>

    <linearGradient id="hairline" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{P["violet"]}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{P["cyan"]}"/>
      <stop offset="1" stop-color="{P["pink"]}" stop-opacity="0"/>
    </linearGradient>

    <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>

  <g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bgGrad)"/>

  <g style="mix-blend-mode:screen">
    <ellipse cx="250" cy="150" rx="430" ry="230" fill="url(#blobViolet)" style="animation:auroraA 16s ease-in-out infinite"/>
    <ellipse cx="1030" cy="190" rx="470" ry="250" fill="url(#blobCyan)"  style="animation:auroraB 20s ease-in-out infinite"/>
    <ellipse cx="660" cy="360" rx="500" ry="200" fill="url(#blobPink)"   style="animation:auroraC 24s ease-in-out infinite"/>
  </g>
''')

# ------------------------------------------------------------------ starfield
stars = []
for _ in range(90):
    x, y = random.uniform(8, W - 8), random.uniform(8, H - 60)
    r = random.uniform(0.5, 1.9)
    dur, delay = random.uniform(2.2, 6.5), random.uniform(0, 6)
    stars.append(
        f'<circle class="star" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" '
        f'style="animation:twinkle {dur:.1f}s ease-in-out {delay:.1f}s infinite"/>')
parts.append("  " + "\n  ".join(stars))

# -------------------------------------------------------------- shooting stars
for i in range(4):
    sx = random.uniform(520, W + 260)
    sy = random.uniform(-40, 120)
    delay = 2.5 * i + random.uniform(0, 2)
    parts.append(f'''
  <g style="animation:shoot {random.uniform(9, 13):.1f}s linear {delay:.1f}s infinite;opacity:0">
    <line x1="{sx:.0f}" y1="{sy:.0f}" x2="{sx + 130:.0f}" y2="{sy - 86:.0f}"
      stroke="#E6EDF3" stroke-width="1.6" stroke-linecap="round" opacity=".8" filter="url(#soft)"/>
    <circle cx="{sx:.0f}" cy="{sy:.0f}" r="2" fill="#fff"/>
  </g>''')

# --------------------------------------------------------- perspective horizon
VPX, VPY = CX, 302
rays = []
for i in range(-13, 14):
    bx = VPX + i * 110
    rays.append(f'<line x1="{VPX}" y1="{VPY}" x2="{bx:.0f}" y2="{H + 30}" '
                f'stroke="{P["violet"]}" stroke-opacity=".16" stroke-width="1"/>')
falls = []
for i in range(6):
    falls.append(
        f'<line x1="0" y1="{VPY + 4}" x2="{W}" y2="{VPY + 4}" stroke="{P["cyan"]}" '
        f'stroke-opacity=".3" stroke-width="1" '
        f'style="animation:gridFall 4.2s linear {i * 0.7:.1f}s infinite"/>')
parts.append(f'''
  <g>
    <line x1="0" y1="{VPY}" x2="{W}" y2="{VPY}" stroke="url(#hairline)" stroke-width="1.4" opacity=".8"/>
    {''.join(rays)}
    {''.join(falls)}
  </g>''')

# ---------------------------------------------------------------- side orbits
for ox, direction in ((150, "spin"), (W - 150, "spinRev")):
    parts.append(f'''
  <g style="animation:floaty 9s ease-in-out infinite">
    <g style="transform-origin:{ox}px 168px;animation:{direction} 26s linear infinite">
      <circle cx="{ox}" cy="168" r="66" fill="none" stroke="{P["violet"]}" stroke-opacity=".5"
        stroke-width="1.6" stroke-dasharray="30 14"/>
      <circle cx="{ox}" cy="168" r="94" fill="none" stroke="{P["cyan"]}" stroke-opacity=".32"
        stroke-width="1.2" stroke-dasharray="4 10 44 10"/>
      <circle cx="{ox + 66}" cy="168" r="3.4" fill="{P["cyan_light"]}" filter="url(#glow)"/>
    </g>
    <rect x="{ox - 7}" y="161" width="14" height="14" fill="none" stroke="{P["pink"]}"
      stroke-width="1.6" transform="rotate(45 {ox} 168)" opacity=".8"
      style="transform-origin:{ox}px 168px;animation:{direction} 12s linear infinite"/>
  </g>''')

# ---------------------------------------------------------------------- title
TITLE, TSIZE, TLS = "MARWAYS", 118, 8
title_w = display_text_width(TITLE, TSIZE, TLS)
base_y = 208
glow_copy = display_text(TITLE, TSIZE, CX, base_y, P["violet"], TLS, "middle",
                         'filter="url(#soft)" opacity=".85"')
main_copy = display_text(TITLE, TSIZE, CX, base_y, "url(#titleGrad)", TLS, "middle")
sheen_copy = display_text(TITLE, TSIZE, CX, base_y, "url(#sheen)", TLS, "middle")
glitch_cyan = display_text(TITLE, TSIZE, CX, base_y, P["cyan"], TLS, "middle")
glitch_pink = display_text(TITLE, TSIZE, CX, base_y, P["pink"], TLS, "middle")

parts.append(f'''
  <g style="animation:floaty 10s ease-in-out infinite">
    {glow_copy}
    {main_copy}
    {sheen_copy}
    <g opacity="0" style="animation:glitch 7s steps(1) infinite">{glitch_cyan}</g>
    <g opacity="0" style="animation:glitch 9s steps(1) 3.5s infinite">{glitch_pink}</g>
    <line x1="{CX - title_w / 2 - 40:.0f}" y1="{base_y + 26}" x2="{CX + title_w / 2 + 40:.0f}" y2="{base_y + 26}"
      stroke="url(#hairline)" stroke-width="2"/>
    <rect x="{CX - 5}" y="{base_y + 21}" width="10" height="10" fill="none" stroke="{P["cyan_light"]}"
      stroke-width="1.6" transform="rotate(45 {CX} {base_y + 26})" style="animation:breathe 3s ease-in-out infinite"/>
  </g>''')

# ------------------------------------------------------------- eyebrow captain
parts.append(f'''
  <g class="mono" font-size="15" style="animation:floaty 10s ease-in-out infinite">
    <text x="{CX}" y="96" text-anchor="middle" fill="{P["muted"]}" letter-spacing="6">— 欢迎来到我的数字宇宙 —</text>
  </g>''')

# ----------------------------------------------------------- subtitle rotator
phrases = [
    ('<tspan fill="' + P["violet_light"] + '">Vibe Coder</tspan>'
     '<tspan fill="' + P["muted"] + '"> · </tspan>'
     '<tspan fill="' + P["cyan_light"] + '">AI Alchemist</tspan>'
     '<tspan fill="' + P["muted"] + '"> · </tspan>'
     '<tspan fill="' + P["pink"] + '">Full-Stack Builder</tspan>'),
    ('<tspan fill="' + P["pink"] + '">const</tspan>'
     '<tspan fill="' + P["text"] + '"> future = </tspan>'
     '<tspan fill="' + P["pink"] + '">await</tspan>'
     '<tspan fill="' + P["cyan_light"] + '"> ai</tspan>'
     '<tspan fill="' + P["text"] + '">.build(</tspan>'
     '<tspan fill="' + P["violet_light"] + '">wildIdeas</tspan>'
     '<tspan fill="' + P["text"] + '">)</tspan>'),
    ('<tspan fill="' + P["cyan_light"] + '">AI × Creativity</tspan>'
     '<tspan fill="' + P["muted"] + '"> → </tspan>'
     '<tspan fill="' + P["green"] + '">Infinite Possibilities ∞</tspan>'),
]
sub_y = 286
phrase_texts = "".join(
    f'<text x="{CX + 6}" y="{sub_y + 21}" text-anchor="middle" font-size="17" '
    f'style="animation:phrase{i + 1} 18s ease-in-out infinite;opacity:0">{p}</text>'
    for i, p in enumerate(phrases))
parts.append(f'''
  <g class="mono">
    <rect x="{CX - 330}" y="{sub_y - 10}" width="660" height="44" rx="22"
      fill="#0D1117" fill-opacity=".55" stroke="{P["violet"]}" stroke-opacity=".45" stroke-width="1.2"/>
    <text x="{CX - 306}" y="{sub_y + 21}" font-size="17" fill="{P["green"]}" font-weight="700">❯</text>
    {phrase_texts}
    <rect x="{CX + 296}" y="{sub_y + 6}" width="9" height="20" fill="{P["cyan_light"]}"
      style="animation:cursorBlink 1.1s steps(1) infinite"/>
  </g>''')

# -------------------------------------------------------------------- waveform
def wave_path(amp, period, y0):
    pts = []
    for x in range(-period, W + period * 2 + 1, 8):
        y = y0 + amp * math.sin(2 * math.pi * x / period)
        pts.append(f"{x},{y:.1f}")
    return "M" + " L".join(pts)


parts.append(f'''
  <g opacity=".55">
    <path d="{wave_path(7, 320, H - 26)}" fill="none" stroke="{P["cyan"]}" stroke-width="1.6"
      style="animation:waveSlide 7s linear infinite"/>
    <path d="{wave_path(10, 440, H - 18)}" fill="none" stroke="{P["violet"]}" stroke-width="1.2"
      style="animation:waveSlide2 11s linear infinite"/>
  </g>''')

# ------------------------------------------------------------------ HUD frame
parts.append(f'''
  <g>
    <path class="hud" d="M 26 62 L 26 26 L 62 26"/>
    <path class="hud" d="M {W - 26} {H - 62} L {W - 26} {H - 26} L {W - 62} {H - 26}"/>
    <path class="hud" d="M {W - 62} 26 L {W - 26} 26 L {W - 26} 62"/>
    <path class="hud" d="M 62 {H - 26} L 26 {H - 26} L 26 {H - 62}"/>
    <g class="mono" font-size="12" fill="{P["muted"]}" letter-spacing="2">
      <text x="44" y="34">SYS.ONLINE</text>
      <circle cx="36" cy="30" r="3" fill="{P["green"]}" style="animation:breathe 2s ease-in-out infinite"/>
      <text x="{W - 44}" y="34" text-anchor="end">EST. 2023</text>
      <text x="44" y="{H - 30}">GITHUB.COM/MARWAYS7</text>
      <text x="{W - 44}" y="{H - 30}" text-anchor="end">OPEN SOURCE ∞</text>
    </g>
  </g>

  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none"
    stroke="{P["violet"]}" stroke-opacity=".4" stroke-width="1.5"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none"
    stroke="{P["cyan"]}" stroke-opacity=".5" stroke-width="1.5"
    stroke-dasharray="60 140" style="animation:dashFlow 6s linear infinite"/>
  </g>
</svg>
''')

write_svg(ASSETS_DIR / "sota-hero.svg", "".join(parts))
