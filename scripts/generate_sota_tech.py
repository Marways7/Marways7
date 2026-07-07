"""Tech orbit — assets/sota-tech.svg.

Real devicon vectors are inlined at build time (immune to GitHub's CSP),
arranged on three tilted orbits around a pulsing AI core.
"""

import math
import random
import re
import urllib.request

from svgtools import (ASSETS_DIR, MONO_STACK, PALETTE, display_text,
                      write_svg)

random.seed(42)
P = PALETTE
W, H = 1200, 620
CX, CY = W / 2, H / 2 - 10

ICON_BASE = "https://raw.githubusercontent.com/devicons/devicon/master/icons"
ICONS = {
    "python": f"{ICON_BASE}/python/python-original.svg",
    "typescript": f"{ICON_BASE}/typescript/typescript-original.svg",
    "javascript": f"{ICON_BASE}/javascript/javascript-original.svg",
    "react": f"{ICON_BASE}/react/react-original.svg",
    "html5": f"{ICON_BASE}/html5/html5-original.svg",
    "css3": f"{ICON_BASE}/css3/css3-original.svg",
    "pytorch": f"{ICON_BASE}/pytorch/pytorch-original.svg",
    "tensorflow": f"{ICON_BASE}/tensorflow/tensorflow-original.svg",
    "nodejs": f"{ICON_BASE}/nodejs/nodejs-original.svg",
    "nextjs": f"{ICON_BASE}/nextjs/nextjs-original.svg",
    "docker": f"{ICON_BASE}/docker/docker-original.svg",
    "mongodb": f"{ICON_BASE}/mongodb/mongodb-original.svg",
    "java": f"{ICON_BASE}/java/java-original.svg",
    "mysql": f"{ICON_BASE}/mysql/mysql-original.svg",
    "redis": f"{ICON_BASE}/redis/redis-original.svg",
    "git": f"{ICON_BASE}/git/git-original.svg",
    "linux": f"{ICON_BASE}/linux/linux-original.svg",
    "vscode": f"{ICON_BASE}/vscode/vscode-original.svg",
}

FALLBACK_COLORS = {
    "python": "#3776AB", "typescript": "#3178C6", "javascript": "#F7DF1E",
    "react": "#61DAFB", "html5": "#E34C26", "css3": "#1572B6",
    "pytorch": "#EE4C2C", "tensorflow": "#FF6F00", "nodejs": "#339933",
    "nextjs": "#888888", "docker": "#2496ED", "mongodb": "#47A248",
    "java": "#E76F00", "mysql": "#00758F", "redis": "#DC382D",
    "git": "#F05032", "linux": "#FBC02D", "vscode": "#007ACC",
}


def fetch_icon(name, url):
    """Return (inner_svg, scale, translate) sized for a 40px box."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode("utf-8")
        match = re.search(r"<svg[^>]*>(.*?)</svg>", data, re.IGNORECASE | re.DOTALL)
        if not match:
            return None
        inner = match.group(1)
        vb = re.search(r'viewBox="([^"]+)"', data)
        if vb:
            x0, y0, vw, vh = (float(v) for v in vb.group(1).split())
            return inner, 40.0 / max(vw, vh), (-x0, -y0)
        return inner, 40.0 / 128.0, (0, 0)
    except Exception as exc:  # noqa: BLE001 - fallback glyph below
        print(f"[tech] icon fetch failed for {name}: {exc}")
        return None


print("[tech] inlining devicon vectors ...")
raw_icons = {name: fetch_icon(name, url) for name, url in ICONS.items()}

ORBITS = [
    {"rx": 218, "ry": 74, "dur": 26, "dir": 1, "tilt": 14,
     "items": ["python", "typescript", "javascript", "react", "html5", "css3"]},
    {"rx": 375, "ry": 122, "dur": 40, "dir": -1, "tilt": -10,
     "items": ["pytorch", "tensorflow", "nodejs", "nextjs", "docker", "mongodb"]},
    {"rx": 532, "ry": 172, "dur": 56, "dir": 1, "tilt": 7,
     "items": ["java", "mysql", "redis", "git", "linux", "vscode"]},
]

parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto" role="img" aria-label="Tech stack orbit">
  <defs>
    <style>
      @keyframes spinCW  {{ to {{ transform:rotate(360deg); }} }}
      @keyframes spinCCW {{ to {{ transform:rotate(-360deg); }} }}
      @keyframes corePulse {{
        0%,100% {{ transform:scale(1); filter:drop-shadow(0 0 18px rgba(139,92,246,.7)); }}
        50% {{ transform:scale(1.06); filter:drop-shadow(0 0 42px rgba(34,211,238,.9)); }}
      }}
      @keyframes twinkle {{ 0%,100% {{ opacity:.12; }} 50% {{ opacity:.8; }} }}
      @keyframes breathe {{ 0%,100% {{ opacity:.5; }} 50% {{ opacity:1; }} }}
      @keyframes arcFlow {{ to {{ stroke-dashoffset:-1200; }} }}
      .mono {{ font-family:{MONO_STACK}; }}
      .orbitRing {{ fill:none; stroke:rgba(139,92,246,.22); stroke-width:1.4; stroke-dasharray:5 9; }}
      .node {{ fill:#0D1117; stroke:rgba(167,139,250,.65); stroke-width:2;
               filter:drop-shadow(0 0 9px rgba(139,92,246,.45)); }}
    </style>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{P["bg_deep"]}"/>
      <stop offset=".5" stop-color="#0C0A22"/>
      <stop offset="1" stop-color="#071018"/>
    </linearGradient>
    <radialGradient id="coreGrad" cx="50%" cy="42%" r="60%">
      <stop offset="0" stop-color="#F472B6"/>
      <stop offset=".55" stop-color="#8B5CF6"/>
      <stop offset="1" stop-color="#0EA5B7"/>
    </radialGradient>
    <radialGradient id="vign" cx="50%" cy="50%" r="72%">
      <stop offset=".62" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity=".55"/>
    </radialGradient>
    <radialGradient id="coreHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#8B5CF6" stop-opacity=".35"/>
      <stop offset="1" stop-color="#8B5CF6" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  </defs>

  <g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bgGrad)"/>
  <circle cx="{CX}" cy="{CY}" r="360" fill="url(#coreHalo)"/>
''']

for _ in range(70):
    x, y = random.uniform(6, W - 6), random.uniform(6, H - 6)
    parts.append(
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(.5, 1.7):.1f}" fill="#E6EDF3" '
        f'style="animation:twinkle {random.uniform(2.5, 6):.1f}s ease-in-out {random.uniform(0, 5):.1f}s infinite"/>')

for orbit in ORBITS:
    rx, ry, dur, tilt = orbit["rx"], orbit["ry"], orbit["dur"], orbit["tilt"]
    spin = "spinCW" if orbit["dir"] == 1 else "spinCCW"
    counter = "spinCCW" if orbit["dir"] == 1 else "spinCW"
    circumference = 2 * math.pi * math.sqrt((rx * rx + ry * ry) / 2)
    parts.append(f'''
  <g style="transform-origin:{CX}px {CY}px;transform:rotate({tilt}deg)">
    <ellipse cx="{CX}" cy="{CY}" rx="{rx}" ry="{ry}" class="orbitRing"/>
    <ellipse cx="{CX}" cy="{CY}" rx="{rx}" ry="{ry}" fill="none" stroke="rgba(34,211,238,.6)"
      stroke-width="2" stroke-dasharray="90 {circumference:.0f}" stroke-linecap="round"
      style="animation:arcFlow {dur * 1.1:.0f}s linear infinite"/>
    <g style="transform-origin:{CX}px {CY}px;animation:{spin} {dur}s linear infinite">''')

    for i, item in enumerate(orbit["items"]):
        angle = 2 * math.pi * i / len(orbit["items"])
        x = CX + rx * math.cos(angle)
        y = CY + ry * math.sin(angle)
        icon = raw_icons.get(item)
        if icon:
            inner, scale, (tx, ty) = icon
            glyph = (f'<g transform="translate({x - 20:.1f},{y - 20:.1f}) '
                     f'scale({scale:.4f}) translate({tx},{ty})">{inner}</g>')
        else:
            color = FALLBACK_COLORS.get(item, P["violet_light"])
            glyph = (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="{color}"/>'
                     f'<text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle" class="mono" '
                     f'font-size="14" font-weight="700" fill="#0D1117">{item[0].upper()}</text>')
        parts.append(f'''
      <g style="transform-origin:{x:.1f}px {y:.1f}px;animation:{counter} {dur}s linear infinite">
        <g style="transform-origin:{x:.1f}px {y:.1f}px;transform:rotate({-tilt}deg)">
          <circle cx="{x:.1f}" cy="{y:.1f}" r="27" class="node"/>
          {glyph}
        </g>
      </g>''')
    parts.append("\n    </g>\n  </g>")

core_text = display_text("AI", 40, CX, CY + 6, "#FFFFFF", 3, "middle")
core_sub = display_text("CORE", 13, CX, CY + 30, "rgba(230,237,243,.85)", 5, "middle")
parts.append(f'''
  <g style="transform-origin:{CX}px {CY}px;animation:corePulse 4.5s ease-in-out infinite">
    <circle cx="{CX}" cy="{CY}" r="62" fill="url(#coreGrad)"/>
    <circle cx="{CX}" cy="{CY}" r="74" fill="none" stroke="#F472B6" stroke-width="2.4"
      stroke-dasharray="16 30" style="transform-origin:{CX}px {CY}px;animation:spinCW 11s linear infinite"/>
    <circle cx="{CX}" cy="{CY}" r="88" fill="none" stroke="#22D3EE" stroke-width="1.6"
      stroke-dasharray="4 18 40 12" style="transform-origin:{CX}px {CY}px;animation:spinCCW 17s linear infinite"/>
    <polygon points="{CX},{CY - 50} {CX + 43},{CY - 25} {CX + 43},{CY + 25} {CX},{CY + 50} {CX - 43},{CY + 25} {CX - 43},{CY - 25}"
      fill="none" stroke="rgba(255,255,255,.4)" stroke-width="1.6"
      style="transform-origin:{CX}px {CY}px;animation:spinCW 24s linear infinite"/>
    {core_text}
    {core_sub}
  </g>

  <g class="mono" font-size="12" fill="{P["muted"]}" letter-spacing="2">
    <text x="34" y="{H - 74}">ORBIT-01 <tspan fill="{P["cyan_light"]}">LANGUAGES / FRONTEND</tspan></text>
    <text x="34" y="{H - 52}">ORBIT-02 <tspan fill="{P["violet_light"]}">AI / RUNTIME / DATA</tspan></text>
    <text x="34" y="{H - 30}">ORBIT-03 <tspan fill="{P["pink"]}">INFRA / TOOLING</tspan></text>
    <text x="{W - 34}" y="{H - 30}" text-anchor="end" style="animation:breathe 3s ease-in-out infinite"><tspan fill="{P["green"]}">●</tspan> ALL SYSTEMS ROTATING</text>
  </g>

  <rect width="{W}" height="{H}" fill="url(#vign)" pointer-events="none"/>
  </g>
  <rect x=".8" y=".8" width="{W - 1.6}" height="{H - 1.6}" rx="15" fill="none"
    stroke="{P["violet"]}" stroke-opacity=".38" stroke-width="1.5"/>
</svg>
''')

write_svg(ASSETS_DIR / "sota-tech.svg", "".join(parts))
