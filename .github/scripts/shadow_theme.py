"""Restyle the Pac-Man contribution graph as the Shadow Army.

The generator embeds each ghost as a PNG inside a <symbol> and uses GitHub's
colors for the grid. This script swaps the ghosts for vector shadow soldiers
and recolors the grid to the profile palette, keeping symbol ids, viewBoxes
and the animation timeline untouched.
"""

import re
import sys
from pathlib import Path

EYE_COLORS = {
    "blinky": "#e879f9",
    "inky": "#60a5fa",
    "pinky": "#c4b5fd",
    "clyde": "#f5f3ff",
}
# Eye offset so each soldier looks where it moves.
LOOK = {"up": (0, -1), "down": (0, 1), "left": (-1.4, 0), "right": (1.4, 0)}

PALETTE = {
    "#0d1117": "#07060b",
    "#161b22": "#120d1f",
    "#0e4429": "#3b1f6e",
    "#006d32": "#5b2ba8",
    "#26a641": "#7c3aed",
    "#39d353": "#a855f7",
    "#8b949e": "#9b95b8",
    "#ffffff": "#5b3a9a",
    '"yellow"': '"#60a5fa"',
}

SYMBOL = re.compile(
    r'(<symbol id="(ghost-[a-z-]+)" viewBox="0 0 20 20">)\s*<image [^>]*/>\s*(</symbol>)'
)

BODY = (
    "M10 1.5C6 1.5 3.6 4.4 3.6 8.2V14.5L2.2 19L5 17.4L7.4 19.2L10 17.2"
    "L12.6 19.2L15 17.4L17.8 19L16.4 14.5V8.2C16.4 4.4 14 1.5 10 1.5Z"
)
HORNS = "M5.2 4.6L3.4 1.2L6.8 3.4ZM14.8 4.6L16.6 1.2L13.2 3.4Z"


def eyes(color: str, dx: float, dy: float) -> str:
    return (
        f'<path d="M{6.2 + dx} {8.6 + dy}L{8.8 + dx} {9.6 + dy}L{6.4 + dx} {10.4 + dy}Z" fill="{color}"/>'
        f'<path d="M{13.8 + dx} {8.6 + dy}L{11.2 + dx} {9.6 + dy}L{13.6 + dx} {10.4 + dy}Z" fill="{color}"/>'
    )


def soldier(eye: str, dx: float, dy: float, body: str = "#140c26", rim: str = "#8b5cf6") -> str:
    return (
        f'<path d="{BODY}" fill="{body}" stroke="{rim}" stroke-width="0.9"/>'
        f'<path d="{HORNS}" fill="{rim}"/>' + eyes(eye, dx, dy)
    )


def sprite(symbol_id: str) -> str:
    parts = symbol_id.split("-")[1:]
    if parts == ["scared"]:
        return soldier("#f5f3ff", 0, 0, body="#1e3a8a", rim="#60a5fa")
    kind, direction = parts
    dx, dy = LOOK[direction]
    if kind == "eyes":
        return eyes("#a855f7", dx, dy)
    return soldier(EYE_COLORS[kind], dx, dy)


def convert(svg: str) -> tuple[str, int]:
    svg, count = SYMBOL.subn(lambda m: f"{m[1]}{sprite(m[2])}{m[3]}", svg)
    for old, new in PALETTE.items():
        svg = svg.replace(old, new)
    return svg, count


def main(paths: list[str]) -> None:
    if not paths:
        sys.exit("usage: shadow_theme.py file.svg [file.svg ...]")
    for name in paths:
        path = Path(name)
        converted, count = convert(path.read_text(encoding="utf-8"))
        if count == 0:
            sys.exit(f"{path}: no ghost sprites found, the generator format may have changed")
        path.write_text(converted, encoding="utf-8")
        print(f"{path}: replaced {count} sprites")


if __name__ == "__main__":
    main(sys.argv[1:])
