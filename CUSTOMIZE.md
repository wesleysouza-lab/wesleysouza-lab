# Customizing the profile

## Publish

1. Create a **public** repo named exactly like your user: `wesleysouza-lab/wesleysouza-lab`.
2. Copy `README.md` and the `assets/` folder to the repo root.
3. Push. GitHub shows the README on your profile.

Relative image paths (`assets/...`) work on the repo and on the profile page.

## Placeholders to fill (search for `TODO`)

- Role, LinkedIn URL, portfolio URL.
- The three project cards (name, description, stack, repo link). Use public repos only.
- Remove from the tech stack table anything you do not really use.

## Colors

| Token | Hex | Use |
|:--|:--|:--|
| Background | `#07090d` / `#080c11` | panels |
| Cyan | `#22d3ee` | main tech color, borders |
| Amber | `#f59e0b` | highlights, IDs |
| Red | `#ef4444` | rare alert accents |
| Text | `#e2e8f0` / `#94a3b8` | primary / secondary |

Change a color by search and replace across `assets/*.svg` and the badge URLs (`22d3ee`).

## Editing the SVGs

- `header.svg`: text lines are plain `<text>` elements. The name is the large title and the handle is on the `HANDLE:` line.
- `operator-core.svg`: the radar polygon uses center-based coordinates (radius 100 = max). Move the five points to change the shape. The values are self-assessed, keep them honest.
- `console.svg`: edit the `<text>` lines. Keep messages factual, no fake metrics.
- `architecture.svg`: five boxes (`rect` + two `text` lines each). Rename them to your real flow.

SVG fonts fall back to a system monospace, because GitHub blocks web fonts inside images.

## Telemetry without third parties

The cards in section 06 use `github-readme-stats` and `github-readme-activity-graph` public instances, which are rate limited and sometimes down. For a version you control, add a GitHub Action that generates SVGs into the repo on a schedule (for example `lowlighter/metrics`, which needs a personal token stored as a repo secret). Then point the `<img>` tags at the generated files in `assets/`.

## Pac-Man simulation (section 07)

1. Copy `.github/workflows/pacman.yml` to the same path in the profile repo.
2. In the repo, go to Settings, Actions, General, Workflow permissions, and allow read and write.
3. Open the Actions tab, pick "Generate Pac-Man contribution graph" and click "Run workflow". It creates the `output` branch with `pacman-contribution-graph-dark.svg`.
4. The README image only shows after that first run. It then refreshes daily at 03:00 UTC.

The Pac-Man action is referenced on `@main` (the project does not publish version tags), so its behavior can change without notice. Pin it to a commit SHA once it works.

## Notes

- GitHub does not run JavaScript or custom CSS in READMEs. The only motion is SMIL animation inside the SVGs (pulse, radar sweep, cursor). Remove the `<animate>` tags for a fully static look.
- Do not list employer-internal repos, client names or private data in cards or the diagram.
