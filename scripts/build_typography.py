"""Generate README headings as outlined Pixelify Sans SVGs.

Install fonttools, then run: python scripts/build_typography.py
Font source: https://github.com/google/fonts/tree/main/ofl/pixelifysans
The bundled font is licensed under assets/fonts/OFL.txt.
Outlines avoid dependence on installed fonts or external font loading.
"""

from html import escape
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
FONT = TTFont(ROOT / "assets/fonts/PixelifySans.ttf")
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UNITS = FONT["head"].unitsPerEm
OUT = ROOT / "assets/typography"


def text_path(text, size, baseline, color, width):
    scale = size / UNITS
    advance = sum(GLYPHS[CMAP[ord(char)]].width for char in text) * scale
    assert advance <= width - 24, f"Text exceeds canvas: {text}"
    x = (width - advance) / 2
    pen = SVGPathPen(GLYPHS)
    for char in text:
        glyph = GLYPHS[CMAP[ord(char)]]
        glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        x += glyph.width * scale
    return f'<path fill="{color}" d="{pen.getCommands()}"/>'


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    headings = {
        "tools": "Tools I build with",
        "focus": "What I'm focused on",
        "activity": "My GitHub activity",
        "contributions": "Contributions over the past year",
    }
    for theme, foreground, accent in (
        ("light", "#0F172A", "#2563EB"),
        ("dark", "#E6EDF3", "#79B8FF"),
    ):
        artworks = {
            "intro": (720, 116, [
                ("Hi, I'm Tharindu Nimesh", 44, 51, foreground),
                ("Creative Developer", 25, 94, accent),
            ]),
            **{
                key: (600, 52, [(label, 28, 36, foreground)])
                for key, label in headings.items()
            },
        }
        for key, (width, height, lines) in artworks.items():
            title = escape(" · ".join(line[0] for line in lines))
            paths = "\n".join(text_path(*line, width) for line in lines)
            svg = (
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
                f'height="{height}" viewBox="0 0 {width} {height}" '
                f'role="img" aria-labelledby="title">\n'
                f"<title id=\"title\">{title}</title>\n{paths}\n</svg>\n"
            )
            (OUT / f"{key}-{theme}.svg").write_text(svg, encoding="utf-8")
    print("Generated 10 Pixelify Sans SVGs for light and dark themes.")


if __name__ == "__main__":
    build()
