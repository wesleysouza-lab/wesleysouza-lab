"""Replace the ghost sprites of the Pac-Man contribution graph with robots.

The generator embeds each ghost as a PNG inside a <symbol>. This script swaps
those images for vector robots, keeping the symbol ids and the 20x20 viewBox so
the generated animation keeps working untouched.
"""

import re
import sys
from pathlib import Path

ROBOT_COLORS = {
    "blinky": "#ef4444",
    "inky": "#22d3ee",
    "pinky": "#94a3b8",
    "clyde": "#f59e0b",
}
# Eye offset inside the visor so each robot looks where it moves.
LOOK = {"up": (0, -1.2), "down": (0, 1.2), "left": (-1.6, 0), "right": (1.6, 0)}

SYMBOL = re.compile(
    r'(<symbol id="(ghost-[a-z-]+)" viewBox="0 0 20 20">)\s*<image [^>]*/>\s*(</symbol>)'
)


def robot(color: str, dx: float, dy: float) -> str:
    return (
        f'<line x1="10" y1="2.4" x2="10" y2="4.6" stroke="{color}" stroke-width="1.2"/>'
        f'<circle cx="10" cy="2" r="1.4" fill="#f1f5f9"/>'
        f'<rect x="2.5" y="4.5" width="15" height="12" rx="3" fill="{color}"/>'
        f'<rect x="4" y="6.5" width="12" height="6" rx="2" fill="#0b1118"/>'
        f'<circle cx="{7.2 + dx}" cy="{9.5 + dy}" r="1.5" fill="#a5f3fc"/>'
        f'<circle cx="{12.8 + dx}" cy="{9.5 + dy}" r="1.5" fill="#a5f3fc"/>'
        f'<rect x="6.5" y="13.7" width="7" height="1.2" rx="0.6" fill="#0b1118" opacity="0.55"/>'
        f'<rect x="4" y="16.5" width="3.2" height="2.5" rx="1" fill="{color}"/>'
        f'<rect x="12.8" y="16.5" width="3.2" height="2.5" rx="1" fill="{color}"/>'
    )


def scared_robot() -> str:
    return (
        '<line x1="10" y1="2.4" x2="10" y2="4.6" stroke="#3b82f6" stroke-width="1.2"/>'
        '<circle cx="10" cy="2" r="1.4" fill="#ef4444"/>'
        '<rect x="2.5" y="4.5" width="15" height="12" rx="3" fill="#3b82f6"/>'
        '<rect x="4" y="6.5" width="12" height="6" rx="2" fill="#0b1118"/>'
        '<path d="M6 8.3L8.4 10.7M8.4 8.3L6 10.7M11.6 8.3L14 10.7M14 8.3L11.6 10.7" '
        'stroke="#f1f5f9" stroke-width="1" stroke-linecap="round"/>'
        '<path d="M6 14.2L7.7 13.4L9.3 14.2L10.9 13.4L12.6 14.2L14 13.4" fill="none" '
        'stroke="#0b1118" stroke-width="1" opacity="0.7"/>'
        '<rect x="4" y="16.5" width="3.2" height="2.5" rx="1" fill="#3b82f6"/>'
        '<rect x="12.8" y="16.5" width="3.2" height="2.5" rx="1" fill="#3b82f6"/>'
    )


def eyes_only(dx: float, dy: float) -> str:
    return (
        f'<circle cx="{6.8 + dx}" cy="{10 + dy}" r="2.2" fill="#22d3ee" fill-opacity="0.35"/>'
        f'<circle cx="{13.2 + dx}" cy="{10 + dy}" r="2.2" fill="#22d3ee" fill-opacity="0.35"/>'
        f'<circle cx="{6.8 + dx}" cy="{10 + dy}" r="1.3" fill="#a5f3fc"/>'
        f'<circle cx="{13.2 + dx}" cy="{10 + dy}" r="1.3" fill="#a5f3fc"/>'
    )


def sprite(symbol_id: str) -> str:
    parts = symbol_id.split("-")[1:]
    if parts == ["scared"]:
        return scared_robot()
    kind, direction = parts
    dx, dy = LOOK[direction]
    if kind == "eyes":
        return eyes_only(dx, dy)
    return robot(ROBOT_COLORS[kind], dx, dy)


def convert(svg: str) -> tuple[str, int]:
    return SYMBOL.subn(lambda m: f"{m[1]}{sprite(m[2])}{m[3]}", svg)


def main(paths: list[str]) -> None:
    if not paths:
        sys.exit("usage: robots.py file.svg [file.svg ...]")
    for name in paths:
        path = Path(name)
        converted, count = convert(path.read_text(encoding="utf-8"))
        if count == 0:
            sys.exit(f"{path}: no ghost sprites found, the generator format may have changed")
        path.write_text(converted, encoding="utf-8")
        print(f"{path}: replaced {count} sprites")


if __name__ == "__main__":
    main(sys.argv[1:])
