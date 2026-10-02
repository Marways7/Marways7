"""Build the Ideas take shape profile. No network or third-party image services.

Run from any directory with Python 3.11+ and fonttools installed.
Public metadata is refreshed separately by refresh_public_data.py.
"""
from pathlib import Path
from html import escape
import json
import math

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "shape"
OUT.mkdir(parents=True, exist_ok=True)
FONT = instantiateVariableFont(TTFont(ROOT / "assets/fonts/Sora.ttf"), {"wght": 600})
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UPEM = FONT["head"].unitsPerEm
BG, FG, MUTED, BLUE, CORAL, AQUA = "#081C2C", "#EDF7FA", "#9DB3C4", "#527CFF", "#FFAA8A", "#93E5DD"


def display(value, x, y, size, color=FG, tracking=-.7):
    commands, cursor = [], 0
    scale = size / UPEM
    for char in value:
        glyph = GLYPHS[CMAP[ord(char)]]
        pen = SVGPathPen(GLYPHS, ntos=lambda n: f"{n:.2f}")
        glyph.draw(TransformPen(pen, Transform(scale, 0, 0, -scale, cursor, 0)))
        commands.append(pen.getCommands())
        cursor += glyph.width * scale + tracking
    return f'<g aria-label="{escape(value)}" transform="translate({x},{y})"><path fill="{color}" d="{" ".join(commands)}"/></g>'


def text(value, x, y, size=20, color=MUTED, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(value)}</text>'


def path(d, color=BLUE, width=1.2, extra=""):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" {extra}/>'


STYLE = """
text{font-family:Arial,'Microsoft YaHei','PingFang SC',sans-serif}
.sculpture{transform-origin:880px 340px;animation:breath 12s ease-in-out infinite}
.light{stroke-dasharray:90 1150;animation:travel 9s linear infinite}
.signal{stroke-dasharray:50 780;animation:travel 10s linear infinite}
.float{animation:lift 8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
.thread{animation:threadflow 8s linear infinite;stroke-dasharray:24 980}
@keyframes breath{0%,100%{transform:translate(0,0) rotate(-3deg)}50%{transform:translate(-9px,-13px) rotate(2deg)}}
@keyframes travel{to{stroke-dashoffset:-1240}}
@keyframes lift{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@keyframes threadflow{to{stroke-dashoffset:-1004}}
@media(prefers-reduced-motion:reduce){.sculpture,.light,.signal,.float,.fiber,.thread{animation:none!important}}
"""


def svg(w, h, title, body, static=False, light=False):
    bg = "#EAF2F6" if light else BG
    style = STYLE + (".sculpture,.light,.signal,.float,.fiber,.thread{animation:none!important}" if static else "")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">Original vector artwork for Marways. Ideas take shape. Slow light travels through a sculptural number seven.</desc>
<defs>
<linearGradient id="fiber" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{AQUA}"/><stop offset=".32" stop-color="{BLUE}"/><stop offset=".64" stop-color="#BDCAFF"/><stop offset="1" stop-color="{CORAL}"/></linearGradient>
<linearGradient id="wash"><stop stop-color="{BLUE}" stop-opacity="0"/><stop offset=".55" stop-color="{BLUE}" stop-opacity=".11"/><stop offset="1" stop-color="{AQUA}" stop-opacity="0"/></linearGradient>
<radialGradient id="halo"><stop stop-color="#386AA8" stop-opacity=".19"/><stop offset="1" stop-color="#386AA8" stop-opacity="0"/></radialGradient>
<clipPath id="frame"><rect width="{w}" height="{h}" rx="20"/></clipPath>
</defs><style>{style}</style><g clip-path="url(#frame)"><rect width="{w}" height="{h}" fill="{bg}"/>{body}</g></svg>'''


def sculpture():
    # Elliptical cross-sections along a seven-shaped bent fiber bundle.
    bits = ['<g class="sculpture">']
    for i in range(76):
        a = i / 76 * math.tau
        s = math.sin(a)
        def strand(phase):
            c, s = math.cos(a+phase), math.sin(a+phase)
            twist_c, twist_s = math.cos(a-phase*.8), math.sin(a-phase*.8)
            return (f'M {634+58*c:.2f} {182+58*s:.2f} '
                    f'C {756+68*c:.2f} {140+48*s:.2f} {959+45*twist_c:.2f} {127+56*twist_s:.2f} {1063+27*twist_c:.2f} {165+54*twist_s:.2f} '
                    f'C {1032+27*twist_c:.2f} {244+61*twist_s:.2f} {800+51*c:.2f} {401+50*s:.2f} {815+55*c:.2f} {548+37*s:.2f}')
        d, middle = strand(0), strand(.72)
        bits.append(f'<style>@keyframes fiber{i}{{0%,100%{{d:path("{d}")}}50%{{d:path("{middle}")}}}}</style>')
        bits.append(path(d, "url(#fiber)", 1.35, f'class="fiber" opacity="{.27+.55*(s+1)/2:.2f}" style="animation:fiber{i} 12s ease-in-out infinite"'))
        if i % 11 == 0:
            bits.append(path(d, FG, 1.55, f'class="light" opacity=".75" style="animation-delay:-{i*.23:.2f}s"'))
    # End-cap filaments reveal depth without a raster glow or filter.
    for k in range(7):
        bits.append(f'<ellipse cx="815" cy="548" rx="{55-k*5}" ry="{37-k*3.3}" fill="none" stroke="{CORAL}" stroke-width=".6" opacity=".28"/>')
    bits.append('</g>')
    return ''.join(bits)


def hero(mobile=False, static=False):
    w, h = (640, 890) if mobile else (1200, 690)
    body = f'<ellipse cx="{w*.75}" cy="{h*.50}" rx="490" ry="360" fill="url(#halo)"/>'
    if mobile:
        body += display("Marways", 38, 78, 34)
        body += text("Vibe coder since 2023", 38, 108, 17)
        body += '<g transform="translate(-479,37) scale(1.00)">' + sculpture() + '</g>'
        body += display("Ideas take", 38, 680, 65)
        body += display("shape.", 38, 752, 65)
        body += text("把想法，做成看得见的作品。", 40, 803, 29, FG)
        body += text("AI tools / Signal intelligence / Creative code", 40, 852, 20)
    else:
        body += display("Marways", 56, 94, 44)
        body += text("Vibe coder since 2023", 58, 129, 18)
        body += sculpture()
        body += display("Ideas take", 56, 311, 76)
        body += display("shape.", 56, 397, 76)
        body += text("把想法，做成看得见的作品。", 60, 459, 27, FG)
        body += text("AI tools. Signal intelligence. Creative code.", 60, 498, 20)
        body += path("M60 589 H1140", "#2D4659", .8)
        body += text("An idea", 60, 639, 18, FG)
        body += path("M150 633 H202 M195 629 L202 633 195 637", MUTED, 1.3)
        body += text("A prototype", 220, 639, 18, FG)
        body += path("M340 633 H392 M385 629 L392 633 385 637", MUTED, 1.3)
        body += text("Something real", 410, 639, 18, FG)
        body += text("Always in the making.", 940, 639, 17)
    return svg(w, h, "Marways — Ideas take shape / 让想法成形", body, static)


PROJECTS = [
    ("ECG Identification", "ECG_IdentificationX", "A heartbeat becomes an identity.", "心电身份识别", "Python / PyTorch", CORAL, "ecg"),
    ("AiliaoX", "AiliaoX", "A conversation becomes an interface.", "AI 医院信息系统", "TypeScript / MCP", AQUA, "chat"),
    ("DeepReadX", "DeepReadX", "A difficult page becomes clear.", "AI 辅助 PDF 阅读 · Android", "Java / OCR / AI", "#B9C9FF", "book"),
    ("Desktop Operator", "cua_desktop_operator_skill", "An intention becomes an action.", "让 AI 操作桌面", "Python / MCP / CLI", "#B5DDD6", "cursor"),
    ("Signal Sprint", "signal-sprint", "A live stream gets a shorter path.", "直播本地播放优化", "JavaScript / Browser", "#9CBDFF", "signal"),
    ("Campus Guide", "college_student_self-rescue_guide_website", "Shared knowledge finds its people.", "学习资源发现与分享", "TypeScript / Web", "#EABBA9", "campus"),
]


def motif(kind, color):
    out = []
    if kind == "ecg":
        for i in range(16):
            y = 22+i*3.2
            d = f'M0 {y} H25 l12 -12 10 12 h14 l11 -{50+i*.5} 13 {93+i*.5} 12 -43 h17 l12 -18 15 18 h32'
            out.append(path(d, color, .8, f'opacity="{.15+i*.04:.2f}"'))
    elif kind == "chat":
        for i in range(12):
            out.append(f'<rect x="{i*3.6}" y="{i*2.1}" width="105" height="66" rx="{19+i*.5}" stroke="{color}" stroke-width=".8" fill="none" opacity="{.17+i*.045:.2f}"/>')
        out.append(path("M31 66 L19 92 59 73 M83 47 H117", color, 2))
    elif kind == "book":
        for i in range(15):
            out.append(path(f'M85 84 C56 {32-i*3} 20 {54-i*2} 0 {44-i*2} V{86-i*.9} Q48 {90-i*1.5} 85 104 C112 65 137 91 166 53 V{10+i*2} Q116 {3+i*3} 85 84', color, .9, f'opacity="{.2+i*.045:.2f}"'))
    elif kind == "cursor":
        for i in range(15):
            out.append(path(f'M{18+i*3} {-12+i} l18 98 21 -28 28 28 13 -14 -26 -26 35 -8 Z', color, .85, f'opacity="{.15+i*.05:.2f}"'))
    elif kind == "signal":
        for i in range(17):
            out.append(path(f'M0 {14+i*5} C40 {14+i*5} 36 {90-i*4} 82 {50+i*1.7} S127 {82-i*4} 177 {20+i*2.8}', color, 1, f'opacity="{.25+i*.035:.2f}"'))
    else:
        for i in range(11):
            out.append(path(f'M0 {28+i*4} L83 {-10+i*4} 166 {28+i*4} 83 {66+i*4} Z', color, .9, f'opacity="{.2+i*.06:.2f}"'))
    return ''.join(out)


def projects(mobile=False, static=False, light=False):
    w, h = (640, 1880) if mobile else (1200, 1080)
    fg, muted = (BG, "#456174") if light else (FG, MUTED)
    body = display("Different questions.", 40 if mobile else 52, 78, 36 if mobile else 43, fg)
    body += display("Same curiosity.", 40 if mobile else 52, 126, 36 if mobile else 43, fg)
    body += text("从一个问题出发，让作品给出答案。", 40 if mobile else 54, 170, 21, muted)
    # Each project is a node on a shared vertical thread, not an isolated badge.
    body += path(f'M{30 if mobile else 600} 224 V{h-53}', "#48647B" if light else "#284358", 1)
    body += path(f'M{30 if mobile else 600} 224 V{h-53}', AQUA, 2, 'class="thread" opacity=".8"')
    for i, (name, repo, tagline, cn, stack, color, kind) in enumerate(PROJECTS):
        x = 52 if mobile else (54 if i % 2 == 0 else 652)
        y = 242 + (i if mobile else i//2)*270
        node_x = 30 if mobile else 600
        body += f'<circle cx="{node_x}" cy="{y+102}" r="5" fill="{color}"/>'
        body += path(f'M{node_x} {y+102} H{x-12 if mobile or i%2 else x+492}', "#48647B" if light else "#284358", .8)
        body += f'<a xlink:href="https://github.com/Marways7/{repo}" href="https://github.com/Marways7/{repo}" target="_top"><g>'
        body += f'<rect x="{x-8}" y="{y-13}" width="490" height="240" fill="transparent"/>'
        body += f'<g transform="translate({x+301},{y+8}) scale(.80)">{motif(kind, color if not light else "#41648D")}</g>'
        body += text(stack, x, y+20, 20 if mobile else 16, muted)
        body += display(name, x, y+119, 28 if kind=="ecg" else 31, fg)
        body += text(cn, x, y+155, 27 if mobile else 21, fg)
        body += text(tagline, x, y+185, 19 if mobile else 16, muted)
        body += '</g></a>'
        if i < 4 or mobile:
            body += path(f'M{x} {y+218} H{x+485}', "#C7D7E1" if light else "#233E52", .7)
    return svg(w, h, "Six projects, one curiosity — Marways project atlas", body, static, light)


def pulse(mobile=False):
    data = json.loads((ROOT / "data/public-profile.json").read_text(encoding="utf-8-sig"))
    repos = data["repositories"]
    lang = sorted({r["language"] for r in repos if r.get("language")})
    stars = sum(r["stargazers_count"] for r in repos)
    w, h = (640, 320) if mobile else (1200, 190)
    body = display("Open by nature.", 40 if mobile else 52, 70, 32)
    body += text("公开作品，持续生长。", 42 if mobile else 54, 107, 21)
    counts = [(len(repos), "public repos"), (stars, "repo stars"), (len(lang), "languages")]
    for i, (number, label) in enumerate(counts):
        x, y = (44+i*195, 204) if mobile else (595+i*195, 82)
        body += display(str(number).zfill(2), x, y, 39, AQUA)
        body += text(label, x, y+29, 22 if mobile else 17)
    date = data["updated_at"][:10]
    body += text(f'Public GitHub snapshot / {date}', 42 if mobile else 54, h-28, 14)
    return svg(w, h, f"Public GitHub snapshot: {len(repos)} repositories, {stars} repository stars, {len(lang)} languages. Updated {date}.", body, True)


def footer(mobile=False, static=False):
    w, h = (640, 290) if mobile else (1200, 245)
    body = display("The next idea", 40 if mobile else 52, 81, 38 if mobile else 47)
    body += display("is already taking shape.", 40 if mobile else 52, 135, 30 if mobile else 47)
    body += text("保持好奇。把下一次灵感，做出来。", 42 if mobile else 55, 198, 22, MUTED)
    if not mobile:
        for i in range(18):
            body += path(f'M892 {185+i*.8} C{845+i*3} {40+i*6} {1100-i*4} {50-i} 1148 {152+i*1.8}', "url(#fiber)", .9, 'opacity=".55"')
    return svg(w, h, "The next idea is already taking shape.", body, static)


def main():
    for mobile in (False, True):
        suffix = "-mobile" if mobile else ""
        for static in (False, True):
            ending = "-still" if static else ""
            for name, maker in (("hero", hero), ("projects", projects), ("footer", footer)):
                (OUT / f"{name}{suffix}{ending}.svg").write_text(maker(mobile, static), encoding="utf-8")
        (OUT / f"pulse{suffix}.svg").write_text(pulse(mobile), encoding="utf-8")
    total = sum(p.stat().st_size for p in OUT.glob("*.svg"))
    print(f"Built {len(list(OUT.glob('*.svg')))} SVG assets ({total/1024:.0f} KiB including static/mobile alternatives).")


if __name__ == "__main__":
    main()
