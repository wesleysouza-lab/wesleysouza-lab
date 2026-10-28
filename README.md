<!-- Profile README for github.com/wesleysouza-lab/wesleysouza-lab. See CUSTOMIZE.md. Items marked TODO are placeholders. -->

<div align="center">
  <img src="assets/header.svg" alt="Wesley Souza, developer profile header" width="100%">
</div>

<img src="assets/divider.svg" alt="" width="100%">

## `// 01 · OPERATOR PROFILE`

<table>
<tr>
<td valign="top" width="60%">

```text
ID ............ Wesley Souza
HANDLE ........ @wesleysouza-lab
UNIT .......... AI & Technology team · RBBR
ROLE .......... TODO: your title
BASE .......... Brazil (UTC-3)
LANGUAGES ..... Portuguese (native) · English (technical)
```

I build the data and automation layer that turns operational systems into
decisions: pipelines, APIs and dashboards. I like boring, verifiable
engineering: tests first, small PRs and no secrets in code.

**Specialties:** data pipelines · BigQuery · FastAPI services · internal dashboards · AI-assisted workflows

[![LinkedIn](https://img.shields.io/badge/LinkedIn-TODO-0b1118?style=flat-square&logo=linkedin&logoColor=22d3ee&labelColor=0b1118&color=22d3ee)](https://www.linkedin.com/in/TODO)
[![Email](https://img.shields.io/badge/Email-wesley.souza@rbbr.com.br-0b1118?style=flat-square&logo=gmail&logoColor=22d3ee&labelColor=0b1118&color=22d3ee)](mailto:wesley.souza@rbbr.com.br)
[![Portfolio](https://img.shields.io/badge/Portfolio-TODO-0b1118?style=flat-square&logo=googlechrome&logoColor=22d3ee&labelColor=0b1118&color=22d3ee)](https://TODO.example.com)

</td>
<td valign="top" width="40%" align="center">
<img src="assets/operator-core.svg" alt="Focus map: Python, Data, Cloud, AI, Backend" width="100%">
</td>
</tr>
</table>

<img src="assets/divider.svg" alt="" width="100%">

## `// 02 · SYSTEM CONSOLE`

<img src="assets/console.svg" alt="Console: system initialized, developer environment ready, engineering modules loaded" width="100%">

<img src="assets/divider.svg" alt="" width="100%">

## `// 03 · NEURAL NETWORK · TECH STACK`

<!-- TODO: remove anything you do not actually use. -->

| Module | Technologies |
|:--|:--|
| **Programming languages** | ![Python](https://img.shields.io/badge/Python-0b1118?style=flat-square&logo=python&logoColor=22d3ee&color=22d3ee) ![JavaScript](https://img.shields.io/badge/JavaScript-0b1118?style=flat-square&logo=javascript&logoColor=22d3ee&color=22d3ee) ![SQL](https://img.shields.io/badge/SQL-0b1118?style=flat-square&logo=postgresql&logoColor=22d3ee&color=22d3ee) |
| **Frontend engineering** | ![HTML5](https://img.shields.io/badge/HTML5-0b1118?style=flat-square&logo=html5&logoColor=22d3ee&color=22d3ee) ![CSS3](https://img.shields.io/badge/CSS3-0b1118?style=flat-square&logo=css3&logoColor=22d3ee&color=22d3ee) ![Playwright](https://img.shields.io/badge/Playwright-0b1118?style=flat-square&logo=playwright&logoColor=22d3ee&color=22d3ee) |
| **Backend systems** | ![FastAPI](https://img.shields.io/badge/FastAPI-0b1118?style=flat-square&logo=fastapi&logoColor=22d3ee&color=22d3ee) ![Poetry](https://img.shields.io/badge/Poetry-0b1118?style=flat-square&logo=poetry&logoColor=22d3ee&color=22d3ee) ![Pytest](https://img.shields.io/badge/Pytest-0b1118?style=flat-square&logo=pytest&logoColor=22d3ee&color=22d3ee) |
| **Databases** | ![BigQuery](https://img.shields.io/badge/BigQuery-0b1118?style=flat-square&logo=googlebigquery&logoColor=22d3ee&color=22d3ee) ![SAP HANA](https://img.shields.io/badge/SAP%20HANA-0b1118?style=flat-square&logo=sap&logoColor=22d3ee&color=22d3ee) |
| **DevOps & infrastructure** | ![Google Cloud](https://img.shields.io/badge/Google%20Cloud-0b1118?style=flat-square&logo=googlecloud&logoColor=22d3ee&color=22d3ee) ![Cloud Run](https://img.shields.io/badge/Cloud%20Run-0b1118?style=flat-square&logo=googlecloud&logoColor=22d3ee&color=22d3ee) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-0b1118?style=flat-square&logo=githubactions&logoColor=22d3ee&color=22d3ee) |
| **Tools & workflow** | ![Git](https://img.shields.io/badge/Git-0b1118?style=flat-square&logo=git&logoColor=22d3ee&color=22d3ee) ![Linux](https://img.shields.io/badge/Linux%20(WSL)-0b1118?style=flat-square&logo=linux&logoColor=22d3ee&color=22d3ee) ![Claude Code](https://img.shields.io/badge/Claude%20Code-0b1118?style=flat-square&logo=anthropic&logoColor=22d3ee&color=22d3ee) ![Obsidian](https://img.shields.io/badge/Obsidian-0b1118?style=flat-square&logo=obsidian&logoColor=22d3ee&color=22d3ee) |

<img src="assets/divider.svg" alt="" width="100%">

## `// 04 · SYSTEM ARCHITECTURE`

<img src="assets/architecture.svg" alt="Data flow: sources to ingestion jobs to BigQuery to FastAPI on Cloud Run to dashboards, guarded by a CI quality gate" width="100%">

<sub>Generic flow of the systems I work on. Internal repositories are private, so details are omitted on purpose.</sub>

<details>
<summary><code>INSPECT MODULE</code> · click a stage to expand</summary>
<br>

<details>
<summary><b>01 · Sources</b> <code>SAP HANA · APIs · Sheets</code></summary>
<br>Operational data comes from the ERP (SAP HANA), partner APIs and spreadsheets. Every source is read with the least access it needs, and credentials live in a secret manager, never in code.
</details>

<details>
<summary><b>02 · Ingest</b> <code>Python · Poetry · Cloud Run</code></summary>
<br>Each job is an independent Poetry project with its own <code>src/</code> and <code>tests/</code>, deployed to Cloud Run. Jobs validate external input before writing anything.
</details>

<details>
<summary><b>03 · Store</b> <code>BigQuery</code></summary>
<br>Data moves through layers: <code>raw</code> keeps what arrived, <code>core</code> cleans and models it, <code>dm</code> serves each business question.
</details>

<details>
<summary><b>04 · Serve</b> <code>FastAPI · Cloud Run</code></summary>
<br>Small FastAPI services expose the data to the interfaces, with authentication in front and one responsibility per service.
</details>

<details>
<summary><b>05 · Interface</b> <code>Dashboards</code></summary>
<br>Internal dashboards for operations teams. Front-end changes are checked with browser tests (Playwright) before they count as verified.
</details>

<details>
<summary><b>CI · Quality gate</b> <code>ruff · tests · secrets scan</code></summary>
<br>Every pull request is checked on the lines it changes: lint, tests with at least 80% coverage, secret scanning and complexity. A human decides every merge.
</details>

<details>
<summary><b>AI agents</b> <code>Claude Code</code></summary>
<br>Agents prepare changes and run checks. People review and decide.
</details>

</details>

<img src="assets/divider.svg" alt="" width="100%">

## `// 05 · ACTIVE PROJECTS`

<!-- TODO: replace with public repos. Do not list private or employer-internal code. -->

<table>
<tr>
<td valign="top" width="33%">
<img src="assets/card-top.svg" alt="" width="100%"><br>
<code>PRJ-001</code> · <b>TODO project name</b><br>
<sub>One-line description of what it does and for whom.</sub><br>
<sub><code>Python</code> <code>FastAPI</code></sub><br>
<sub>🟢 active · <a href="https://github.com/wesleysouza-lab/TODO">repo</a></sub>
</td>
<td valign="top" width="33%">
<img src="assets/card-top.svg" alt="" width="100%"><br>
<code>PRJ-002</code> · <b>TODO project name</b><br>
<sub>One-line description of what it does and for whom.</sub><br>
<sub><code>Python</code> <code>BigQuery</code></sub><br>
<sub>🟡 in progress · <a href="https://github.com/wesleysouza-lab/TODO">repo</a></sub>
</td>
<td valign="top" width="33%">
<img src="assets/card-top.svg" alt="" width="100%"><br>
<code>PRJ-003</code> · <b>TODO project name</b><br>
<sub>One-line description of what it does and for whom.</sub><br>
<sub><code>JavaScript</code> <code>HTML</code></sub><br>
<sub>⚪ planned · <a href="https://github.com/wesleysouza-lab/TODO">repo</a></sub>
</td>
</tr>
</table>

<img src="assets/divider.svg" alt="" width="100%">

## `// 06 · GITHUB TELEMETRY`

<div align="center">

<a href="https://github.com/wesleysouza-lab"><img height="165" alt="GitHub stats: commits, PRs, issues, stars" src="https://github-readme-stats.vercel.app/api?username=wesleysouza-lab&show_icons=true&hide_border=true&bg_color=080c11&title_color=22d3ee&icon_color=f59e0b&text_color=e2e8f0&ring_color=22d3ee&count_private=true"></a>

</div>

<details>
<summary><code>ACTIVITY HISTORY</code> (expand)</summary>
<br>

<img alt="Contribution graph" width="100%" src="https://github-readme-activity-graph.vercel.app/graph?username=wesleysouza-lab&bg_color=080c11&color=e2e8f0&line=22d3ee&point=f59e0b&area=true&area_color=22d3ee&hide_border=true">

<sub>These cards come from public third-party services and can be slow or offline. If they are, the alt text is shown and nothing breaks. For a version with no external dependency, see "Telemetry without third parties" in CUSTOMIZE.md.</sub>

</details>

<img src="assets/divider.svg" alt="" width="100%">

## `// 07 · SIMULATION DECK`

<!-- Generated daily by .github/workflows/pacman.yml from your real contributions. Empty until the first run. -->

<div align="center">
  <img src="https://raw.githubusercontent.com/wesleysouza-lab/wesleysouza-lab/output/pacman-contribution-graph-dark.svg" alt="Pac-Man simulation eating the contribution graph" width="100%">
</div>

<sub>Pac-Man plays on my real contribution graph. It is generated by a scheduled GitHub Action, not a live feed.</sub>

<img src="assets/divider.svg" alt="" width="100%">

## `// 08 · COMMUNICATION PROTOCOL`

| Channel | Address |
|:--|:--|
| LinkedIn | [TODO](https://www.linkedin.com/in/TODO) |
| Email | [wesley.souza@rbbr.com.br](mailto:wesley.souza@rbbr.com.br) |
| Portfolio | [TODO](https://TODO.example.com) |
| GitHub | [@wesleysouza-lab](https://github.com/wesleysouza-lab) |

<div align="center">

<sub><code>SYSTEM STANDING BY</code></sub>

</div>
