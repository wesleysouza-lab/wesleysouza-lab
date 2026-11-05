# Customizing the Player Evolution System

## How the profile is built

| Section | Source | Updates |
|:--|:--|:--|
| Battle banner | `assets/banner-battle.svg` | static file, animated with SMIL |
| Player Status, Level Up, Experience Log | `.github/scripts/player_stats.py` | daily, from real public GitHub data |
| Shadow Army graph | Pac-Man Action + `.github/scripts/shadow_theme.py` | daily, from real contributions |
| Notification, Skill Tree, Quests, Shadow units, Dungeon map | `assets/*.svg` | static files, edit by hand |

The daily workflow (`.github/workflows/pacman.yml`, "Update the Player system") writes the generated files to the `output` branch. If any step fails, nothing is published and the previous images stay up.

The banner hunter and the creature are original silhouettes drawn for this profile. No character art from the anime is used.

## Level, rank and XP

All inputs come from the public GitHub API. The result is a symbolic gamification, not a professional rank.

```
XP    = contributions in the last 365 days × 10
      + public repositories (not forks)  × 50
      + stars across public repositories × 25
LEVEL = 1 + floor(sqrt(XP / 50))      # level L starts at 50 × (L-1)² XP
RANK  = E (Lv 1-4) · D (5-9) · C (10-19) · B (20-34) · A (35-49) · S (50+)
```

Achievements unlock from the same data: first public repository, 10 and 100 contributions in a year, 5 public repositories, first star, a 7-day streak.

To change the weights, thresholds or achievements, edit the constants at the top of `player_stats.py` and `summarize()`. To change name, class or title, edit `PROFILE`.

Preview locally without calling the API:

```bash
gh api graphql -f query='query($login:String!){user(login:$login){repositories(ownerAffiliations:OWNER,privacy:PUBLIC,first:100){nodes{isFork stargazerCount primaryLanguage{name}}} contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}' -f login=wesleysouza-lab --jq '.data.user' > user.json
python3 .github/scripts/player_stats.py out --input user.json
```

## Palette

| Token | Hex | Use |
|:--|:--|:--|
| Void | `#07060b` / `#0f0a1c` | backgrounds |
| Violet | `#8b5cf6` / `#a78bfa` / `#c4b5fd` | frames, primary accents |
| Spectral blue | `#60a5fa` | status, the player |
| Cold white | `#f5f3ff` / `#ede9fe` | text |
| Magenta | `#e879f9` | level up, rare highlights |

## Static files

- `banner-battle.svg`: the 4 s combat loop (lunge, slash, knockback) and the system window. Player, name and class are plain `<text>`.
- `system-notification.svg`: four lines on a 12 s loop.
- `skill-tree.svg`: six categories; skills unlock in order. Keep only tools you really use.
- `quest-*.svg`: one card per quest (daily, main, side, completed). The link is set in the README, around each image.
- `shadow-units.svg`: Vesper, Onyx and Umbra are original names. Replace each "TODO: public repo" with the project the unit represents.
- `dungeon-map.svg`, `quest-panels.svg`, `system-divider.svg`: decoration and the data-flow diagram.

GitHub renders SMIL animation inside SVG images, but blocks web fonts, JavaScript and clicks inside them. Links work only on the `<a>` around an image.

## Publication checklist

- [ ] Replace every `TODO`: `PROFILE["title"]` in `player_stats.py`, LinkedIn, portfolio, quests main and side, shadow units.
- [ ] Quests and units list public repos only. No employer code, client names or private data.
- [ ] Remove from the skill tree anything you do not use.
- [ ] Settings, Actions, General: workflow permissions set to read and write.
- [ ] After merging, run "Update the Player system" once from the Actions tab.
- [ ] Open the profile with Ctrl+F5 (images are cached for a few minutes) and check desktop and phone width.
- [ ] Pin the Actions to commit SHAs once everything is stable.
