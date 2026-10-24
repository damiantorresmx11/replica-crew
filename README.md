# Replica Crew

**Everything for cloning software with coding agents, in one repo, for Claude
Code and Codex.** Web pages, web apps, desktop apps, Android apps, games, and
original game mashups. One command takes a target from "I want my own version
of X" to a tested, rebranded product, with 11 specialist subagents. First it
scans your computer, read-only, and tells you which target types it can build.
The repo bundles 15 more open-source clone, design-extraction and UI-to-code
skills, and maps 80+ related tools.

> **ES:** Todo para clonar software con agentes de código, en un solo repo,
> para Claude Code y Codex: páginas y apps web, apps de escritorio, apps
> Android, videojuegos y mezclas originales de videojuegos (p. ej. mecánicas
> de Minecraft con las de GTA V). Primero escanea tu computadora, sin tocar
> nada, y te dice qué puedes construir. 11 subagentes más 15 skills de
> clonado integradas. Sala limpia: se clonan funciones y mecánicas, nunca
> código, arte, marca ni contenido.

```
Claude Code:  /replica-crew https://example-app.com
Codex:        $replica-crew https://example-app.com
```

Five target types (`web`, `desktop`, `android`, `game`, `mashup`): see
[`docs/TARGETS.md`](docs/TARGETS.md). To set up and scan the machine in one
step, paste the prompt in [`docs/INSTALL_PROMPT.md`](docs/INSTALL_PROMPT.md).
Check the machine any time: `python skills/replica-capabilities/doctor.py`.

## Binary decompilation (Claude Code and Codex)

Both hosts support authorized static analysis of APK/DEX, .NET assemblies,
Java bytecode and native PE/ELF/Mach-O binaries through `replica-recon`.
Use an installed decompiler (JADX, ILSpy, CFR, Ghidra) or a connected MCP.
The agents inventory inputs, record hashes, run the appropriate tool and
write `replica/binary/report.md` with evidence and recovery limitations.
The default goal is to understand behavior and build an independent app from
scratch. Recon hands a functional `replica/behavior-spec.md` to the builders;
raw recovered code is kept separate. If analysis is restricted, agents continue
with permitted documentation, screenshots and behavior observations.
Record ownership/authorization and analysis scope in `replica/scope.md`.
Recovered code stays out of product-mode clones.

```text
Claude Code: /replica-crew Analyze my local binary <path>; I own it. Static decompilation only.
Codex:       $replica-crew Analyze my local binary <path>; I own it. Static decompilation only.
```

See the shared [binary workflow](skills/replica-recon/binary-analysis.md).
Build tools are optional for analysis-only work; decompilers are not bundled
or installed automatically.

## Install

```bash
git clone https://github.com/damiantorresmx11/replica-crew
python replica-crew/scripts/install.py          # Claude Code and/or Codex
python replica-crew/scripts/install.py --mcp    # + Playwright and Chrome DevTools MCP
```

Or by hand:

| host | command |
| --- | --- |
| Claude Code | `/plugin marketplace add damiantorresmx11/replica-crew` then `/plugin install replica-crew@replica-crew` |
| Codex | copy `skills/*` to `~/.agents/skills/` and `codex/agents/*.toml` to `~/.codex/agents/` |
| Codex plugin marketplace | `codex plugin marketplace add damiantorresmx11/replica-crew` |
| any other agent | read [`AGENTS.md`](AGENTS.md); every `SKILL.md` is plain Markdown |

Requirements: Python 3.8+. Node for Playwright and some bundled skills.
Tests: `python -m unittest discover -s tests -v`.

## First run: install + scan your machine

Prefer a hands-off setup? Paste this whole block to Claude Code or Codex. It
installs the toolkit, scans your computer read-only, and tells you which
target types you can build before anything else runs. The agent installs only
the toolkit; it never installs languages, SDKs or drivers for you. (Also kept
at [`docs/INSTALL_PROMPT.md`](docs/INSTALL_PROMPT.md).)

```text
You are setting up "Replica Crew" (https://github.com/damiantorresmx11/replica-crew),
a toolkit of skills and subagents for cloning apps, websites, desktop apps,
Android apps and games with coding agents. Do this in order and stop at the
first blocker.

STEP 1 - INSTALL THE TOOLKIT (this is the only thing you install).
- Detect whether you are Claude Code or Codex from your own tools.
- Claude Code:
    /plugin marketplace add damiantorresmx11/replica-crew
    /plugin install replica-crew@replica-crew
- Codex: clone the repo to a temp dir and run its installer:
    git clone --depth 1 https://github.com/damiantorresmx11/replica-crew
    python replica-crew/scripts/install.py
  (It copies skills to ~/.agents/skills and the 11 agents to ~/.codex/agents.)
- If git or python is missing, stop and tell me the one command to install it
  for my OS. Do not work around it.

STEP 2 - SCAN THIS COMPUTER (read-only, installs nothing, no network).
- Find doctor.py inside the installed "replica-capabilities" skill (look under
  ~/.agents/skills, ~/.claude/skills, ~/.claude/plugins, or the cloned repo's
  skills/ folder).
- Run:  python <path>/doctor.py --json
- The scan only runs "--version" probes and checks a few folders. It reads my
  OS, CPU count, and which toolchains I have: Node, npm, Python, Git, Docker,
  Java, Gradle, Flutter, Android SDK, .NET, Rust (cargo), Go, CMake, Godot,
  Blender, FFmpeg, Playwright, adb, gh. It writes nothing except its own report.
- If you cannot find or run doctor.py, say so and stop; do not guess my setup.

STEP 3 - TELL ME WHAT I CAN BUILD.
From the JSON "targets" block, give me a short table of the five target types
(web, desktop, android, game, mashup) with READY or NOT-READY for each, and for
every NOT-READY one, the exact tools to install and their official sites (the
scan already names them). Then one line: "Ready now: <list>."

STEP 4 - ASK, DON'T ASSUME.
Ask me which target and which app/site/game I want to clone. Do not start recon
or the build until I answer. If I pick a NOT-READY target, list what to install,
let me install it, then re-run STEP 2 - never install it for me, never fake the
scan, and never promise a stack my machine can't build, test or run.

STEP 5 - RULES YOU KEEP THE WHOLE TIME.
- Clean room: rebuild features, flows and mechanics from public sources and my
  own account or my owned copy. Never copy the original's code, assets, art,
  audio, trademarks or content, and never decompile a binary or load/mod a game
  I do not own unless I state in writing that I own it or am authorized.
- Never create accounts, buy domains, type passwords, or paste live keys.
- Nothing ships under the original's name, and nothing goes live without my go.

Report each step's result in one or two lines. Begin with STEP 1.
```

## Three modes

| mode | for | engine |
| --- | --- | --- |
| `product` (default) | your **own** product with the features of someone else's app | 11 Replica agents, clean room |
| `faithful` | a site you **own or are authorized** to copy: migrate your site, restore a lost codebase, client work under contract | `clone-team`, `clone-website`, `web-clone`, `stitch-extract-static-html` |
| `study` | learn how a premium site is built, kept local, assets substituted | `clone-study` |

## Product mode: how it runs

```
Wave -1 capabilities         read-only machine scan: which targets are buildable
Wave 0  scope (you)          target type, app, slice, stack, how far, ownership
Wave 1  recon                screens, flows, data model, feature matrix
Wave 2  architect | design | entrepreneur     <- in parallel
Wave 3  build -> backend
Wave 4  test -> diff -> build gaps            <- loop, max 3 rounds
Wave 5  brand -> launch
Wave 6  deploy preflight -> your explicit go -> live
```

- **Specialists.** Each phase runs in its own subagent (Claude:
  `replica-crew:replica-X`; Codex: custom agent `replica-X`), so the main
  conversation keeps only short reports.
- **Parallel wave.** Architect, design and the review-reading entrepreneur
  run at once; the fixes users ask for enter the feature matrix before the
  build.
- **Quality loop.** Test and diff repeat on the gap list until the verdict
  is `shippable` (feature score 80+, no open S1/S2), max three rounds.
- **Two stops only.** After recon and before go-live. Agents that need a
  human decision return `NEEDS_USER` instead of guessing.
- **Audit trail.** Every agent appends to `replica/crew-log.md`.

## The eleven agents

| Agent | Does | Writes |
| --- | --- | --- |
| `replica-recon` | maps the app from public sources and your own account | `recon.md`, `features.csv`, `screens/` |
| `replica-architect` | stack, SQL schema, routes, build order | `architecture.md`, `schema.sql` |
| `replica-design` | design tokens and component specs, WCAG checked | `design/` |
| `replica-entrepreneur` | reads real, linked user reviews; fix plan and angle | `feedback.md`, `fixes.md` |
| `replica-build` | screen by screen, every state | app code, `build-log.md` |
| `replica-backend` | auth, DB rules, Stripe test mode, email, jobs | migrations, `backend.md` |
| `replica-test` | test plan, Playwright, bug log by severity | `test-plan.md`, `bugs.md`, `e2e/` |
| `replica-diff` | feature parity score and layout diff | `parity.md`, `diffs/` |
| `replica-brand` | new name, palette, logo brief, voice, leftover sweep | `brand.md`, `brand.json` |
| `replica-launch` | landing, pricing, store listing lint | `launch/` |
| `replica-deploy` | preflight gate, DNS, production, monitoring | `deploy.md` |

Six standard-library Python tools ship with them: `imgdiff.py`,
`parity.py`, `reviews.py`, `contrast.py`, `sweep.py`, `listing.py`.

## Bundled skills (15 third-party, all MIT or Apache-2.0)

| skill | from | used in |
| --- | --- | --- |
| `clone-team` | Varalix-Digitech-Solutions/clone-team | faithful: whole sites with a 4-agent team |
| `clone-website` | JCodesMore/ai-website-cloner-template | faithful: pages to Next.js fast |
| `web-clone` | Jane-xiaoer/claude-skill-web-clone | faithful: WebGL, Canvas, Three.js |
| `clone-study` | luukalleman/clone-study | study mode |
| `design-mirror` | brightdata/skills | apply a look to your existing app (Bright Data key) |
| `stitch-extract-design-md`, `stitch-extract-static-html`, `design-md`, `site-md`, `stitch-react-components`, `shadcn-ui` | google-labs-code/stitch-skills | recon, design, build |
| `video-to-ui` | mmohajer9/video-to-ui | recon from walkthrough videos |
| `ui-image-to-code` | zwq-top/ui-image-to-code-studio | build from your own wireframes |
| `restyle` | Mahanaicoach/ai-site-cloner | brand |
| `app-store-screenshots` | ParthJadhav/app-store-screenshots | launch |

Each keeps its license (`LICENSE.upstream`) and source commit
(`UPSTREAM.md`). Details: [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Ecosystem

[`docs/ECOSYSTEM.md`](docs/ECOSYSTEM.md) maps 70+ tools verified on GitHub
in October 2026: REA, screenshot-to-code, open-lovable, Chrome DevTools and
Playwright MCP, Figma MCPs, dembrandt, design-extract, DESIGN.md, BackstopJS,
pixelmatch, GhidraMCP, jadx and apktool MCPs, mitmproxy2swagger, crawl4ai and
more, with the phase and agent each one fits. Apps, libraries and MCP servers
are linked rather than copied: they are separate products with their own
runtimes and release cycles.

## Rules

- Product mode rebuilds **what an app does**, never what it owns: no source
  code, bundles, private APIs, logos, icons, licensed fonts, copy or content.
- Public sources and your own account only. No logging into other accounts,
  no paywall tricks, no scraping behind logins, no hammering their servers.
- Faithful mode and binary reverse-engineering tools only for software you
  own or are authorized to copy or analyze, recorded in `replica/scope.md`.
- No fabricated reviews, testimonials, numbers or "available" checks.
- Nothing launches under the original's name, and nothing goes live without
  your go.

This is not legal advice. Read the original's terms, run the trademark
checks `replica-brand` lists, and talk to a lawyer before you charge money.

## Credits and license

MIT. Replica skills and tools © 2026 Jake Schincariol
([Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill),
[upstream README](docs/UPSTREAM-README.md)). Bundled skills © their authors
under their own licenses. Agents, orchestrator, installer and docs © 2026
Damian Torres / [DMLABS](https://dmlabs.mx).
