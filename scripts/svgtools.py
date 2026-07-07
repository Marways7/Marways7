"""Shared toolkit for the Marways profile SVG generators.

Design system: "AURORA CYBERPUNK"
- Deep-space backgrounds, violet/cyan/pink aurora accents
- Display typography (Orbitron) converted to vector paths at build time,
  so it renders pixel-perfect inside GitHub's sandboxed <img> context
  (where @import / external fonts are blocked).
"""

from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = REPO_ROOT / "assets"
DISPLAY_FONT_PATH = ASSETS_DIR / "fonts" / "Orbitron-ExtraBold.ttf"

# ----------------------------------------------------------------------------
# Palette
# ----------------------------------------------------------------------------
PALETTE = {
    "bg_deep": "#05060E",
    "bg_mid": "#0B0820",
    "bg_card": "#0D1117",
    "surface": "#161B22",
    "violet": "#8B5CF6",
    "violet_light": "#A78BFA",
    "cyan": "#22D3EE",
    "cyan_light": "#67E8F9",
    "pink": "#F472B6",
    "green": "#34D399",
    "amber": "#FBBF24",
    "text": "#E6EDF3",
    "muted": "#8B949E",
}

MONO_STACK = (
    "ui-monospace,'SFMono-Regular','SF Mono','Cascadia Code',"
    "'JetBrains Mono',Menlo,Consolas,monospace"
)
SANS_STACK = (
    "-apple-system,'Segoe UI','PingFang SC','Hiragino Sans GB',"
    "'Microsoft YaHei',sans-serif"
)


# ----------------------------------------------------------------------------
# Vector typography
# ----------------------------------------------------------------------------
class DisplayFont:
    """Converts text into baked SVG path data using the display font."""

    def __init__(self, font_path=DISPLAY_FONT_PATH):
        self.font = TTFont(str(font_path))
        self.cmap = self.font.getBestCmap()
        self.glyph_set = self.font.getGlyphSet()
        self.upem = self.font["head"].unitsPerEm

    def text_path_data(self, text, size, letter_spacing=0.0):
        """Return (path_d, total_width) for `text` at `size` px, baseline y=0."""
        scale = size / self.upem
        cursor = 0.0
        commands = []
        for char in text:
            glyph_name = self.cmap.get(ord(char))
            if glyph_name is None:
                cursor += size * 0.6 + letter_spacing
                continue
            glyph = self.glyph_set[glyph_name]
            svg_pen = SVGPathPen(self.glyph_set, ntos=lambda v: f"{v:.1f}")
            pen = TransformPen(svg_pen, Transform(scale, 0, 0, -scale, cursor, 0))
            glyph.draw(pen)
            d = svg_pen.getCommands()
            if d:
                commands.append(d)
            cursor += glyph.width * scale + letter_spacing
        return " ".join(commands), max(cursor - letter_spacing, 0.0)

    def text_element(self, text, size, x=0.0, y=0.0, fill="#FFFFFF",
                     letter_spacing=0.0, anchor="start", attrs=""):
        """Return an SVG fragment drawing `text` as vector paths.

        `y` is the text baseline; `anchor` in {start, middle, end}.
        """
        d, width = self.text_path_data(text, size, letter_spacing)
        if anchor == "middle":
            x -= width / 2
        elif anchor == "end":
            x -= width
        fill_attr = f' fill="{fill}"' if fill else ""
        return (
            f'<g transform="translate({x:.1f},{y:.1f})">'
            f'<path d="{d}"{fill_attr} {attrs}/></g>'
        ), width


_display_font = None


def get_display_font():
    """Load the display font once; returns None when unavailable."""
    global _display_font
    if _display_font is None:
        try:
            _display_font = DisplayFont()
        except Exception as exc:  # noqa: BLE001 - fall back to system text
            print(f"[svgtools] display font unavailable ({exc}); "
                  "falling back to system font text")
            _display_font = False
    return _display_font or None


def display_text(text, size, x=0.0, y=0.0, fill="#FFFFFF",
                 letter_spacing=0.0, anchor="middle", attrs=""):
    """Vector-path text with graceful <text> fallback."""
    font = get_display_font()
    if font is not None:
        fragment, _ = font.text_element(
            text, size, x, y, fill, letter_spacing, anchor, attrs)
        return fragment
    anchor_attr = {"start": "start", "middle": "middle", "end": "end"}[anchor]
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor_attr}" '
        f'font-family="Arial Black,Arial,sans-serif" font-weight="900" '
        f'font-size="{size}" fill="{fill}" '
        f'letter-spacing="{letter_spacing}" {attrs}>{text}</text>'
    )


def display_text_width(text, size, letter_spacing=0.0):
    font = get_display_font()
    if font is None:
        return len(text) * size * 0.72
    _, width = font.text_path_data(text, size, letter_spacing)
    return width


# ----------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------
def esc(value):
    return (str(value).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def write_svg(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    size_kb = path.stat().st_size / 1024
    print(f"[svgtools] wrote {path} ({size_kb:.1f} KB)")
