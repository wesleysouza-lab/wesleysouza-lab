"""Render the Player Status, Level Up and Experience Log panels from real GitHub data.

Everything shown as a number comes from the public GitHub API. Level and rank are
a symbolic gamification of that data (formula below), not a professional rank.

Usage:
    GITHUB_TOKEN=... python3 player_stats.py OUT_DIR
    python3 player_stats.py OUT_DIR --input data.json   # offline, for previews
"""

import argparse
import json
import math
import os
import sys
import urllib.request
from datetime import date
from html import escape
from pathlib import Path

LOGIN = "wesleysouza-lab"
PROFILE = {
    "name": "Wesley Souza",
    "class": "Data Engineer",
    "title": "TODO: your title",
}

XP_PER_CONTRIBUTION = 10
XP_PER_REPO = 50
XP_PER_STAR = 25
# Level L starts at 50 * (L - 1)^2 XP.
LEVEL_STEP = 50
RANKS = [("E", 1), ("D", 5), ("C", 10), ("B", 20), ("A", 35), ("S", 50)]

QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, first: 100) {
      nodes { isFork stargazerCount primaryLanguage { name } }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""

VIOLET, VIOLET_SOFT, VIOLET_PALE = "#8b5cf6", "#a78bfa", "#c4b5fd"
BLUE, MAGENTA, WHITE, TEXT = "#60a5fa", "#e879f9", "#f5f3ff", "#ede9fe"
MUTED, DIM = "#9b95b8", "#6b6585"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Courier New',monospace"
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"


def fetch(token: str) -> dict:
    body = json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode()
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-player-stats",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors") or not payload.get("data", {}).get("user"):
        raise RuntimeError(f"GitHub API returned no user data: {payload.get('errors')}")
    return payload["data"]["user"]


def longest_streak(days: list[dict]) -> int:
    best = current = 0
    for day in days:
        current = current + 1 if day["contributionCount"] > 0 else 0
        best = max(best, current)
    return best


def monthly_totals(days: list[dict]) -> list[tuple[str, int]]:
    totals: dict[str, int] = {}
    for day in days:
        month = day["date"][:7]
        totals[month] = totals.get(month, 0) + day["contributionCount"]
    return sorted(totals.items())[-12:]


def level_for(xp: int) -> int:
    return 1 + math.isqrt(xp // LEVEL_STEP)


def rank_for(level: int) -> str:
    return [name for name, start in RANKS if level >= start][-1]


def summarize(user: dict) -> dict:
    repos = [r for r in user["repositories"]["nodes"] if not r["isFork"]]
    calendar = user["contributionsCollection"]["contributionCalendar"]
    days = [d for week in calendar["weeks"] for d in week["contributionDays"]]
    contributions = calendar["totalContributions"]
    stars = sum(r["stargazerCount"] for r in repos)
    languages: dict[str, int] = {}
    for repo in repos:
        if repo["primaryLanguage"]:
            name = repo["primaryLanguage"]["name"]
            languages[name] = languages.get(name, 0) + 1

    xp = contributions * XP_PER_CONTRIBUTION + len(repos) * XP_PER_REPO + stars * XP_PER_STAR
    level = level_for(xp)
    streak = longest_streak(days)
    achievements = [
        ("AWAKENING", "first public repository", len(repos) >= 1),
        ("FIRST BLOOD", "10 contributions in a year", contributions >= 10),
        ("HUNDRED STRIKES", "100 contributions in a year", contributions >= 100),
        ("SHADOW EXTRACTION", "5 public repositories", len(repos) >= 5),
        ("RECOGNIZED", "first star received", stars >= 1),
        ("UNBROKEN", "7-day contribution streak", streak >= 7),
    ]
    return {
        "contributions": contributions,
        "repos": len(repos),
        "stars": stars,
        "streak": streak,
        "languages": sorted(languages, key=languages.get, reverse=True)[:3],
        "months": monthly_totals(days),
        "xp": xp,
        "level": level,
        "rank": rank_for(level),
        "level_floor": LEVEL_STEP * (level - 1) ** 2,
        "level_ceiling": LEVEL_STEP * level**2,
        "achievements": achievements,
        "updated": date.today().isoformat(),
    }


def frame(width: int, height: int, title: str) -> str:
    w, h = width, height
    tab = len(title) * 11 + 40
    left = (w - tab) // 2
    return (
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f0a1c"/>'
        f'<stop offset="1" stop-color="#07060b"/></linearGradient>'
        f'<linearGradient id="xp" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6d28d9"/>'
        f'<stop offset="0.7" stop-color="{VIOLET_SOFT}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>'
        f'<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter></defs>'
        f'<path d="M14 1H{w - 14}L{w - 1} 14V{h - 14}L{w - 14} {h - 1}H14L1 {h - 14}V14Z" fill="url(#bg)" stroke="{VIOLET}" stroke-opacity="0.7"/>'
        f'<path d="M1 30V14L14 1H44M{w - 44} 1H{w - 14}L{w - 1} 14V30M{w - 1} {h - 30}V{h - 14}L{w - 14} {h - 1}H{w - 44}'
        f'M44 {h - 1}H14L1 {h - 14}V{h - 30}" fill="none" stroke="{VIOLET_PALE}" stroke-width="2"/>'
        f'<path d="M{left + 10} 16H{left + tab - 10}L{left + tab} 26V38H{left}V26Z" fill="#160d29" stroke="{VIOLET_SOFT}" stroke-opacity="0.8"/>'
        f'<text x="{w // 2}" y="31" font-family="{MONO}" font-size="12" fill="{TEXT}" letter-spacing="6" text-anchor="middle">{title}</text>'
    )


def xp_bar(x: int, y: int, width: int, pct: float, loop: bool) -> str:
    fill = max(4, round(width * pct))
    timing = (
        f'values="0;{fill};{fill};0" keyTimes="0;0.35;0.9;1" dur="6s" repeatCount="indefinite"'
        if loop
        else f'from="0" to="{fill}" dur="1.6s" begin="0.3s" fill="freeze"'
    )
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="10" rx="2" fill="#1d1533"/>'
        f'<rect x="{x}" y="{y}" width="0" height="10" rx="2" fill="url(#xp)"><animate attributeName="width" {timing}/></rect>'
        + "".join(
            f'<line x1="{x + width * i // 10}" y1="{y}" x2="{x + width * i // 10}" y2="{y + 10}" stroke="#07060b" stroke-width="2"/>'
            for i in range(1, 10)
        )
    )


def render_status(s: dict) -> str:
    pct = (s["xp"] - s["level_floor"]) / (s["level_ceiling"] - s["level_floor"])
    rows = [
        ("PLAYER", LOGIN, VIOLET_PALE),
        ("NAME", PROFILE["name"], WHITE),
        ("CLASS", PROFILE["class"], TEXT),
        ("TITLE", PROFILE["title"], MAGENTA if PROFILE["title"].startswith("TODO") else TEXT),
    ]
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 330" width="860" height="330" role="img" '
        f'aria-label="Player status. Level {s["level"]}, rank {s["rank"]}, {s["xp"]} XP. '
        f'{s["contributions"]} contributions in the last year, {s["repos"]} public repositories, {s["stars"]} stars, '
        f'best streak {s["streak"]} days. Symbolic, computed from public GitHub activity.">',
        frame(860, 330, "STATUS"),
        f'<g font-family="{MONO}">',
    ]
    for i, (label, value, color) in enumerate(rows):
        y = 78 + i * 28
        out.append(f'<text x="36" y="{y}" font-size="12" fill="{MUTED}">{label}</text>')
        out.append(f'<text x="130" y="{y}" font-size="13" fill="{color}">{escape(value)}</text>')
    out.append(f'<text x="36" y="190" font-size="12" fill="{MUTED}">STATUS</text>')
    out.append(f'<circle cx="135" cy="185" r="4" fill="{BLUE}"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    out.append(f'<text x="146" y="190" font-size="13" fill="{BLUE}" letter-spacing="2">EVOLVING</text>')

    out.append(f'<text x="520" y="70" font-size="11" fill="{BLUE}" letter-spacing="4" text-anchor="middle">LEVEL</text>')
    out.append(f'<text x="520" y="150" font-family="{SANS}" font-size="84" font-weight="800" fill="{VIOLET}" text-anchor="middle" filter="url(#glow)" opacity="0.8">{s["level"]}</text>')
    out.append(f'<text x="520" y="150" font-family="{SANS}" font-size="84" font-weight="800" fill="{WHITE}" text-anchor="middle">{s["level"]}</text>')

    out.append('<g transform="translate(700 112)">')
    out.append(f'<polygon points="0,-52 45,-26 45,26 0,52 -45,26 -45,-26" fill="{VIOLET}" filter="url(#glow)"><animate attributeName="opacity" values="0.2;0.55;0.2" dur="3s" repeatCount="indefinite"/></polygon>')
    out.append(f'<polygon points="0,-52 45,-26 45,26 0,52 -45,26 -45,-26" fill="#120b22" stroke="{VIOLET_PALE}" stroke-width="1.5"/>')
    out.append(f'<text y="17" font-family="{SANS}" font-size="48" font-weight="800" fill="{WHITE}" text-anchor="middle">{s["rank"]}</text>')
    out.append(f'<text y="74" font-size="10" fill="{VIOLET_PALE}" text-anchor="middle" letter-spacing="4">RANK</text>')
    out.append("</g>")

    stats = [
        ("CONTRIBUTIONS", f'{s["contributions"]}', "last 365 days"),
        ("PUBLIC REPOS", f'{s["repos"]}', "not counting forks"),
        ("STARS", f'{s["stars"]}', "across public repos"),
        ("BEST STREAK", f'{s["streak"]}d', "in the last year"),
    ]
    for i, (label, value, note) in enumerate(stats):
        x = 36 + i * 198
        out.append(f'<path d="M{x} 212H{x + 186}V252H{x}Z" fill="#120d1f" stroke="{VIOLET}" stroke-opacity="0.35"/>')
        out.append(f'<text x="{x + 12}" y="229" font-size="9" fill="{MUTED}" letter-spacing="2">{label}</text>')
        out.append(f'<text x="{x + 12}" y="246" font-size="9" fill="{DIM}">{note}</text>')
        out.append(f'<text x="{x + 174}" y="242" font-size="18" font-weight="700" fill="{WHITE}" text-anchor="end">{value}</text>')

    out.append(f'<text x="36" y="280" font-size="11" fill="{BLUE}" letter-spacing="3">EXPERIENCE</text>')
    out.append(f'<text x="824" y="280" font-size="11" fill="{TEXT}" text-anchor="end">{s["xp"]} / {s["level_ceiling"]} XP · next level</text>')
    out.append(xp_bar(36, 288, 788, pct, loop=False))
    out.append(f'<text x="36" y="318" font-size="9" fill="{DIM}">symbolic gamification of public GitHub activity · not a professional rank · updated {s["updated"]}</text>')
    out.append("</g></svg>")
    return "\n".join(out)


def render_level_up(s: dict) -> str:
    pct = (s["xp"] - s["level_floor"]) / (s["level_ceiling"] - s["level_floor"])
    current = [name for name, _ in RANKS].index(s["rank"])
    xs = [80 + i * 140 for i in range(len(RANKS))]
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 340" width="860" height="340" role="img" '
        f'aria-label="Level up system. Rank track from E to S, current rank {s["rank"]} at level {s["level"]}. '
        f'Achievements unlocked: {", ".join(a[0].title() for a in s["achievements"] if a[2]) or "none yet"}.">',
        frame(860, 340, "LEVEL UP SYSTEM"),
        f'<g font-family="{MONO}">',
        f'<line x1="{xs[0]}" y1="92" x2="{xs[-1]}" y2="92" stroke="#1d1533" stroke-width="3"/>',
    ]
    if current:
        out.append(f'<line x1="{xs[0]}" y1="92" x2="{xs[current]}" y2="92" stroke="url(#xp)" stroke-width="3"/>')
    out.append(
        f'<circle r="3" fill="{MAGENTA}"><animateMotion dur="2.4s" repeatCount="indefinite" path="M{xs[0]} 92H{xs[current] + 60}"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.8;1" dur="2.4s" repeatCount="indefinite"/></circle>'
    )
    for i, ((name, start), x) in enumerate(zip(RANKS, xs)):
        reached = i <= current
        fill = "#2e1065" if reached else "#0d0817"
        stroke = VIOLET_PALE if reached else "#3b2d5c"
        text = WHITE if reached else "#4a4266"
        if i == current:
            out.append(
                f'<circle cx="{x}" cy="92" r="26" fill="none" stroke="{MAGENTA}"><animate attributeName="r" values="26;40" dur="2s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0.9;0" dur="2s" repeatCount="indefinite"/></circle>'
            )
        out.append(f'<polygon points="{x},66 {x + 23},79 {x + 23},105 {x},118 {x - 23},105 {x - 23},79" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        out.append(f'<text x="{x}" y="101" font-family="{SANS}" font-size="24" font-weight="800" fill="{text}" text-anchor="middle">{name}</text>')
        end = RANKS[i + 1][1] - 1 if i + 1 < len(RANKS) else None
        span = f"Lv {start}-{end}" if end else f"Lv {start}+"
        out.append(f'<text x="{x}" y="136" font-size="9" fill="{MUTED if reached else DIM}" text-anchor="middle">{span}</text>')
        if i == current:
            out.append(f'<text x="{x}" y="54" font-size="9" fill="{MAGENTA}" text-anchor="middle" letter-spacing="2">YOU ARE HERE</text>')

    out.append(f'<text x="36" y="168" font-size="10" fill="{BLUE}" letter-spacing="3">ACHIEVEMENTS</text>')
    for i, (name, desc, unlocked) in enumerate(s["achievements"]):
        x = 36 + (i % 2) * 262
        y = 180 + (i // 2) * 44
        stroke = VIOLET_SOFT if unlocked else "#2a2140"
        out.append(f'<path d="M{x} {y}H{x + 250}V{y + 36}H{x}Z" fill="{"#160d29" if unlocked else "#0b0814"}" stroke="{stroke}"/>')
        if unlocked:
            out.append(
                f'<path d="M{x} {y}H{x + 250}V{y + 36}H{x}Z" fill="none" stroke="{MAGENTA}" stroke-width="2" opacity="0" filter="url(#glow)">'
                f'<animate attributeName="opacity" values="0;0.9;0;0" keyTimes="0;0.06;0.25;1" dur="7s" begin="{i * 0.7:.1f}s" repeatCount="indefinite"/></path>'
            )
            out.append(f'<path d="M{x + 14} {y + 18}L{x + 18} {y + 23}L{x + 26} {y + 12}" fill="none" stroke="{MAGENTA}" stroke-width="2"/>')
        else:
            out.append(f'<rect x="{x + 13}" y="{y + 16}" width="12" height="10" rx="1" fill="none" stroke="#4a4266"/>')
            out.append(f'<path d="M{x + 15} {y + 16}V{y + 13}A4 4 0 0 1 {x + 23} {y + 13}V{y + 16}" fill="none" stroke="#4a4266"/>')
        out.append(f'<text x="{x + 36}" y="{y + 16}" font-size="10" font-weight="700" fill="{WHITE if unlocked else "#4a4266"}" letter-spacing="1.5">{name}</text>')
        out.append(f'<text x="{x + 36}" y="{y + 29}" font-size="9" fill="{MUTED if unlocked else "#3b3354"}">{desc}</text>')

    # LEVEL UP window popping on a loop
    out.append('<g transform="translate(700 236)">')
    out.append('<g><animateTransform attributeName="transform" type="scale" values="0.7;1.06;1;1;0.7" keyTimes="0;0.08;0.14;0.9;1" dur="6s" repeatCount="indefinite"/>')
    out.append('<animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;0.08;0.14;0.9;1" dur="6s" repeatCount="indefinite"/>')
    out.append(f'<path d="M-118 -54H108L118 -44V54H-108L-118 44Z" fill="#0f0a1c" stroke="{MAGENTA}" stroke-opacity="0.8"/>')
    out.append(f'<text y="-22" font-family="{SANS}" font-size="26" font-weight="800" fill="{MAGENTA}" text-anchor="middle" filter="url(#glow)">LEVEL UP!</text>')
    out.append(f'<text y="-22" font-family="{SANS}" font-size="26" font-weight="800" fill="#fdf4ff" text-anchor="middle">LEVEL UP!</text>')
    out.append(f'<text y="2" font-size="11" fill="{TEXT}" text-anchor="middle" letter-spacing="2">LEVEL {s["level"]} · RANK {s["rank"]}</text>')
    out.append(xp_bar(-100, 16, 200, pct, loop=True))
    out.append(f'<text y="44" font-size="9" fill="{MUTED}" text-anchor="middle">+{XP_PER_CONTRIBUTION} XP per contribution</text>')
    out.append("</g></g>")
    out.append("</g></svg>")
    return "\n".join(out)


def render_xp_log(s: dict) -> str:
    months = s["months"]
    peak = max((n for _, n in months), default=0) or 1
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 230" width="860" height="230" role="img" '
        f'aria-label="Experience log: contributions per month over the last year, {s["contributions"]} in total, '
        f'{s["contributions"] * XP_PER_CONTRIBUTION} XP earned from contributions.">',
        frame(860, 230, "EXPERIENCE LOG"),
        f'<g font-family="{MONO}">',
        f'<text x="36" y="66" font-size="10" fill="{BLUE}" letter-spacing="3">CONTRIBUTIONS PER MONTH</text>',
        f'<text x="824" y="66" font-size="11" fill="{TEXT}" text-anchor="end">{s["contributions"]} contributions · {s["contributions"] * XP_PER_CONTRIBUTION} XP</text>',
        f'<line x1="36" y1="186" x2="824" y2="186" stroke="{VIOLET}" stroke-opacity="0.35"/>',
    ]
    slot = 788 / max(len(months), 1)
    for i, (month, count) in enumerate(months):
        x = 36 + i * slot + slot * 0.2
        width = slot * 0.6
        height = max(2, round(96 * count / peak))
        out.append(
            f'<rect x="{x:.1f}" y="186" width="{width:.1f}" height="0" fill="url(#xp)" opacity="{1 if count else 0.25}">'
            f'<animate attributeName="height" from="0" to="{height}" dur="1.2s" begin="{0.1 * i:.1f}s" fill="freeze"/>'
            f'<animate attributeName="y" from="186" to="{186 - height}" dur="1.2s" begin="{0.1 * i:.1f}s" fill="freeze"/></rect>'
        )
        if count:
            out.append(f'<text x="{x + width / 2:.1f}" y="{180 - height}" font-size="10" fill="{WHITE}" text-anchor="middle">{count}</text>')
        out.append(f'<text x="{x + width / 2:.1f}" y="202" font-size="9" fill="{MUTED}" text-anchor="middle">{date.fromisoformat(month + "-01").strftime("%b")}</text>')
    langs = " · ".join(s["languages"]) or "no public code yet"
    out.append(f'<text x="36" y="220" font-size="9" fill="{DIM}">public repositories: {s["repos"]} · languages: {escape(langs)} · updated {s["updated"]}</text>')
    out.append("</g></svg>")
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("out_dir")
    parser.add_argument("--input", help="raw user JSON instead of calling the API")
    args = parser.parse_args()

    if args.input:
        user = json.loads(Path(args.input).read_text(encoding="utf-8"))
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            sys.exit("GITHUB_TOKEN is not set")
        user = fetch(token)

    stats = summarize(user)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "player-status.svg").write_text(render_status(stats), encoding="utf-8")
    (out / "level-up.svg").write_text(render_level_up(stats), encoding="utf-8")
    (out / "xp-log.svg").write_text(render_xp_log(stats), encoding="utf-8")
    print(f"level {stats['level']} rank {stats['rank']} xp {stats['xp']} contributions {stats['contributions']}")


if __name__ == "__main__":
    main()
