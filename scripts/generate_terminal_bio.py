"""Terminal bio card — assets/terminal-bio.svg.

A fully looping 30s terminal session: typed commands (steps() reveal),
streamed output, an animated progress bar, then a clean restart.
"""

from svgtools import ASSETS_DIR, MONO_STACK, PALETTE, write_svg

P = PALETTE
W, H = 860, 470
T = 30.0          # loop duration in seconds
CHAR_W = 8.15     # advance width of 13.5px system mono (approx)
LEFT = 24
PROMPT = ('<tspan fill="#3FB950" font-weight="700">marways@github</tspan>'
          '<tspan fill="#8B949E">:</tspan>'
          '<tspan fill="#79C0FF" font-weight="700">~/universe</tspan>'
          '<tspan fill="#8B949E">$ </tspan>')
PROMPT_W = CHAR_W * len("marways@github:~/universe$ ")


def pct(t):
    return round(t / T * 100, 2)


keyframes = []
elements = []
_uid = [0]


def appear(t_start, fade=0.35):
    """CSS animation that reveals an element at t_start (stays until loop end)."""
    _uid[0] += 1
    name = f"ap{_uid[0]}"
    keyframes.append(
        f"@keyframes {name} {{ 0%,{pct(t_start)}% {{opacity:0;}} "
        f"{pct(t_start + fade)}%,100% {{opacity:1;}} }}")
    return f"opacity:0;animation:{name} {T}s linear infinite"


def typing_cover(x, y_top, text_len, t_start, t_end, height=18):
    """A bg-colored rect sliding right in char steps, revealing typed text."""
    _uid[0] += 1
    name = f"tp{_uid[0]}"
    w = text_len * CHAR_W + 4
    keyframes.append(
        f"@keyframes {name} {{ 0%,{pct(t_start)}% {{transform:translateX(0);"
        f"animation-timing-function:steps({text_len},end);}} "
        f"{pct(t_end)}%,100% {{transform:translateX({w:.0f}px);}} }}")
    return (f'<rect x="{x:.0f}" y="{y_top}" width="{w:.0f}" height="{height}" fill="#0D1117" '
            f'style="animation:{name} {T}s linear infinite"/>')


def cursor(x, y_top, t_start, t_end, ride=None):
    """Blinking block cursor visible in [t_start, t_end]; optionally rides typing."""
    _uid[0] += 1
    name = f"cu{_uid[0]}"
    keyframes.append(
        f"@keyframes {name} {{ 0%,{pct(t_start)}% {{opacity:0;}} "
        f"{pct(t_start + 0.05)}%,{pct(t_end)}% {{opacity:1;}} "
        f"{pct(t_end + 0.05)}%,100% {{opacity:0;}} }}")
    inner_anim = "animation:blink 1.05s step-end infinite"
    if ride:
        text_len, rt_start, rt_end = ride
        _uid[0] += 1
        rname = f"rd{_uid[0]}"
        w = text_len * CHAR_W
        keyframes.append(
            f"@keyframes {rname} {{ 0%,{pct(rt_start)}% {{transform:translateX(0);"
            f"animation-timing-function:steps({text_len},end);}} "
            f"{pct(rt_end)}%,100% {{transform:translateX({w:.0f}px);}} }}")
        inner_anim = f"animation:{rname} {T}s linear infinite, blink 1.05s step-end infinite"
    return (f'<g style="opacity:0;animation:{name} {T}s linear infinite">'
            f'<rect x="{x:.0f}" y="{y_top}" width="8" height="16" fill="#C9D1D9" '
            f'style="{inner_anim}"/></g>')


def cmd_line(y, command, t_type_start, t_type_end):
    """Prompt + typed command with riding cursor."""
    x_cmd = LEFT + PROMPT_W
    n = len(command)
    frag = (
        f'<g style="{appear(t_type_start - 0.15)}">'
        f'<text x="{LEFT}" y="{y}" class="t">{PROMPT}'
        f'<tspan fill="#D2A8FF">{command}</tspan></text>'
        f'{typing_cover(x_cmd, y - 13, n, t_type_start, t_type_end)}'
        f'</g>'
        f'{cursor(x_cmd, y - 13, t_type_start, t_type_end + 0.7, ride=(n, t_type_start, t_type_end))}'
    )
    return frag


Y0 = 74            # first baseline inside the body
LH = 22

# ---------------------------------------------------------------- timeline --
# 1) whoami
elements.append(cmd_line(Y0, "whoami", 0.8, 1.7))
elements.append(
    f'<g style="{appear(2.1)}"><text x="{LEFT}" y="{Y0 + LH}" class="t">'
    f'<tspan fill="#E6EDF3">marways</tspan>'
    f'<tspan fill="#8B949E"> · </tspan><tspan fill="#A78BFA">vibe coder</tspan>'
    f'<tspan fill="#8B949E"> / </tspan><tspan fill="#67E8F9">ai alchemist</tspan>'
    f'<tspan fill="#8B949E"> / </tspan><tspan fill="#F472B6">full-stack builder</tspan>'
    f'</text></g>')

# 2) cat stack.json
y2 = Y0 + LH * 2 + 12
elements.append(cmd_line(y2, "cat stack.json", 3.6, 5.0))
json_lines = [
    ('<tspan fill="#A5D6FF">{</tspan>', 5.4),
    ('<tspan fill="#79C0FF">  "ai"</tspan><tspan fill="#8B949E">:   </tspan>'
     '<tspan fill="#A5D6FF">[</tspan><tspan fill="#7EE787">"PyTorch", "Agents", "MCP", "LLMs"</tspan>'
     '<tspan fill="#A5D6FF">]</tspan><tspan fill="#8B949E">,</tspan>', 5.7),
    ('<tspan fill="#79C0FF">  "web"</tspan><tspan fill="#8B949E">:  </tspan>'
     '<tspan fill="#A5D6FF">[</tspan><tspan fill="#7EE787">"React", "Next.js", "TypeScript"</tspan>'
     '<tspan fill="#A5D6FF">]</tspan><tspan fill="#8B949E">,</tspan>', 6.0),
    ('<tspan fill="#79C0FF">  "core"</tspan><tspan fill="#8B949E">: </tspan>'
     '<tspan fill="#A5D6FF">[</tspan><tspan fill="#7EE787">"Python", "Node.js", "Docker"</tspan>'
     '<tspan fill="#A5D6FF">]</tspan><tspan fill="#8B949E">,</tspan>', 6.3),
    ('<tspan fill="#79C0FF">  "vibe"</tspan><tspan fill="#8B949E">: </tspan>'
     '<tspan fill="#FBBF24">"∞"</tspan>', 6.6),
    ('<tspan fill="#A5D6FF">}</tspan>', 6.9),
]
for i, (line, t) in enumerate(json_lines):
    elements.append(
        f'<g style="{appear(t)}"><text x="{LEFT}" y="{y2 + LH * (i + 1)}" class="t">{line}</text></g>')

# 3) ./build_future.sh
y3 = y2 + LH * 7 + 12
elements.append(cmd_line(y3, "./build_future.sh --now", 8.6, 10.8))
elements.append(
    f'<g style="{appear(11.3)}"><text x="{LEFT}" y="{y3 + LH}" class="t">'
    f'<tspan fill="#67E8F9">[▸]</tspan><tspan fill="#C9D1D9"> compiling wild ideas → production software ...</tspan>'
    f'</text></g>')

# progress bar
bar_y = y3 + LH + 12
bar_w = 420
keyframes.append(
    f"@keyframes barFill {{ 0%,{pct(11.8)}% {{transform:scaleX(0);}} "
    f"{pct(15.2)}%,100% {{transform:scaleX(1);}} }}")
elements.append(f'''
  <g style="{appear(11.7)}">
    <rect x="{LEFT + 2}" y="{bar_y}" width="{bar_w}" height="12" rx="6" fill="#161B22" stroke="#30363D" stroke-width="1"/>
    <g style="transform-origin:{LEFT + 2}px 0;animation:barFill {T}s linear infinite">
      <rect x="{LEFT + 2}" y="{bar_y}" width="{bar_w}" height="12" rx="6" fill="url(#barGrad)"/>
    </g>
  </g>''')
elements.append(
    f'<g style="{appear(15.4)}"><text x="{LEFT + bar_w + 16}" y="{bar_y + 11}" class="t" '
    f'fill="#3FB950" font-weight="700">100%</text></g>')

elements.append(
    f'<g style="{appear(15.9)}"><text x="{LEFT}" y="{bar_y + LH + 12}" class="t">'
    f'<tspan fill="#3FB950">[✓]</tspan><tspan fill="#C9D1D9"> future built successfully — deploying to </tspan>'
    f'<tspan fill="#F472B6">reality</tspan><tspan fill="#C9D1D9"> ...</tspan></text></g>')
elements.append(
    f'<g style="{appear(16.8)}"><text x="{LEFT}" y="{bar_y + LH * 2 + 12}" class="t">'
    f'<tspan fill="#3FB950">[✓]</tspan><tspan fill="#C9D1D9"> open-source spirit </tspan>'
    f'<tspan fill="#FBBF24">enabled</tspan><tspan fill="#8B949E"> — never stop building.</tspan></text></g>')

# 4) resting prompt
y4 = bar_y + LH * 3 + 20
elements.append(
    f'<g style="{appear(18.2)}"><text x="{LEFT}" y="{y4}" class="t">{PROMPT}</text></g>')
elements.append(cursor(LEFT + PROMPT_W, y4 - 13, 18.4, 27.5))

# ------------------------------------------------------------------ shell --
kf = "\n      ".join(keyframes)
body = "\n  ".join(elements)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xml:space="preserve" role="img" aria-label="Marways terminal profile">
  <defs>
    <style>
      @keyframes blink {{ 0%,49% {{opacity:1;}} 50%,100% {{opacity:0;}} }}
      @keyframes masterFade {{ 0%,1% {{opacity:0;}} 3%,92% {{opacity:1;}} 97%,100% {{opacity:0;}} }}
      @keyframes glowPulse {{ 0%,100% {{opacity:.5;}} 50% {{opacity:1;}} }}
      .t {{ font-family:{MONO_STACK}; font-size:13.5px; }}
      {kf}
    </style>
    <linearGradient id="barGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8B5CF6"/>
      <stop offset=".6" stop-color="#22D3EE"/>
      <stop offset="1" stop-color="#34D399"/>
    </linearGradient>
    <linearGradient id="headGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1C2330"/>
      <stop offset="1" stop-color="#161B22"/>
    </linearGradient>
    <clipPath id="win"><rect width="{W}" height="{H}" rx="12"/></clipPath>
  </defs>

  <g clip-path="url(#win)">
    <rect width="{W}" height="{H}" fill="#0D1117"/>
    <rect width="{W}" height="34" fill="url(#headGrad)"/>
    <circle cx="22" cy="17" r="6" fill="#FF5F56"/>
    <circle cx="44" cy="17" r="6" fill="#FFBD2E"/>
    <circle cx="66" cy="17" r="6" fill="#27C93F"/>
    <text x="{W / 2}" y="22" text-anchor="middle" class="t" font-size="12.5" fill="#8B949E">marways@github: ~/universe — zsh</text>
    <text x="{W - 18}" y="22" text-anchor="end" class="t" font-size="11" fill="#484F58">⟳ 30s</text>

    <g style="animation:masterFade {T}s linear infinite">
      {body}
    </g>
  </g>
  <rect x=".8" y=".8" width="{W - 1.6}" height="{H - 1.6}" rx="11" fill="none"
    stroke="#8B5CF6" stroke-opacity=".45" stroke-width="1.5" style="animation:glowPulse 4s ease-in-out infinite"/>
</svg>
'''

write_svg(ASSETS_DIR / "terminal-bio.svg", svg)
