# Replica Crew

**Clone any app's features with 11 Claude Code subagents.** One command takes
an app from "I want my own version of X" to a tested, rebranded product on
your domain: recon, architecture, design system, review mining, build,
backend, end-to-end tests, parity diff, brand, launch and deploy.

Built on the MIT [Replica skill pack](https://github.com/Jakeschincariol/replica-skill)
by Jake Schincariol. Replica Crew adds a specialist subagent per skill, an
orchestrator that runs independent phases in parallel, and a build-test-diff
loop that stops only when the clone is shippable.

> **ES:** Clona las funciones de cualquier app con 11 subagentes de Claude
> Code. Un comando hace recon, arquitectura, diseño, reseñas, construcción,
> backend, pruebas, paridad, marca, lanzamiento y despliegue. Reglas de sala
> limpia: se clonan funciones y flujos, nunca código, marca ni contenido.

```
/replica-crew https://example-app.com   # whole pipeline
/replica-recon                           # or any single phase
```

## How it runs

```
Wave 0  scope (you)          app, slice, stack, how far, ownership
Wave 1  recon                screens, flows, data model, feature matrix
Wave 2  architect | design | entrepreneur     <- in parallel
Wave 3  build -> backend
Wave 4  test -> diff -> build gaps            <- loop, max 3 rounds
Wave 5  brand -> launch
Wave 6  deploy preflight -> your explicit go -> live
```

What changed from running the 11 skills by hand:

- **Specialists.** Each phase runs in its own subagent with its skill
  preloaded, so the main conversation keeps only short reports, not every
  file read.
- **Parallel wave.** Architect, design and the review-reading entrepreneur
  only need recon, so they run at once. The fixes users ask for go into the
  feature matrix **before** the build, not after.
- **Quality loop.** Test and diff repeat with only the gap list until the
  diff verdict is `shippable` (feature score 80+, no open S1/S2), max three
  rounds, then it reports honest numbers.
- **Two stops only.** After recon (scope sanity) and before go-live.
  Subagents that need a human decision return `NEEDS_USER` instead of
  guessing.
- **Audit trail.** Every agent appends a line to `replica/crew-log.md`.

## The eleven agents

| Agent | Skill | Writes |
| --- | --- | --- |
| `replica-recon` | reverse-engineers the app from public sources and your own account | `recon.md`, `features.csv`, `screens/` |
| `replica-architect` | stack, SQL schema, routes, build order | `architecture.md`, `schema.sql` |
| `replica-design` | design tokens and component specs, WCAG checked | `design/` |
| `replica-entrepreneur` | reads real, linked user reviews; fix plan and angle | `feedback.md`, `fixes.md` |
| `replica-build` | screen by screen, every state, clean room | app code, `build-log.md` |
| `replica-backend` | auth, DB rules, Stripe test mode, email, jobs | migrations, `backend.md` |
| `replica-test` | test plan, Playwright, bug log by severity | `test-plan.md`, `bugs.md`, `e2e/` |
| `replica-diff` | feature parity score and layout diff | `parity.md`, `diffs/` |
| `replica-brand` | new name, palette, logo brief, voice, leftover sweep | `brand.md`, `brand.json` |
| `replica-launch` | landing, pricing, store listing lint | `launch/` |
| `replica-deploy` | preflight gate, DNS, production, monitoring | `deploy.md` |

Six standard-library Python tools ship with the skills: `imgdiff.py`,
`parity.py`, `reviews.py`, `contrast.py`, `sweep.py`, `listing.py`.
No API key, no signup, no pip install.

## Install

Claude Code plugin (agents are namespaced `replica-crew:replica-*`):

```
/plugin marketplace add damiantorresmx11/replica-crew
/plugin install replica-crew@replica-crew
```

Manual (plain names):

```bash
git clone https://github.com/damiantorresmx11/replica-crew
cp -r replica-crew/replica-* ~/.claude/skills/
cp replica-crew/agents/*.md ~/.claude/agents/
```

Other agents (Codex, Cursor, Gemini CLI): read [`AGENTS.md`](AGENTS.md).
Each `replica-*/SKILL.md` is plain Markdown and works as a prompt on its own.

Requirements: Python 3.8+. Optional: Node for Playwright, a browser MCP for
recon. Tests: `python -m unittest discover -s tests -v`.

## Ecosystem

[`docs/ECOSYSTEM.md`](docs/ECOSYSTEM.md) maps 30 open-source tools for AI
app cloning (verified 2026-10-23): ai-website-cloner-template,
screenshot-to-code, open-lovable, REA, Chrome DevTools MCP, Playwright MCP,
dembrandt, design-extract, BackstopJS, pixelmatch, GhidraMCP, jadx and
apktool MCPs, and more, with the phase and agent each one plugs into. Agents
use them only if already installed.

## Rules (inherited from Replica, enforced by every agent)

- Rebuild **what an app does**, never what it owns: no source code, bundles,
  private APIs, logos, icons, licensed fonts, copy or content.
- Public sources and your own account only. No logging into other accounts,
  no paywall tricks, no scraping behind logins, no hammering their servers.
- Binary reverse-engineering tools are only for software you own or are
  authorized to analyze, recorded in `replica/scope.md`.
- No fabricated reviews, testimonials, numbers or "available" checks.
- Nothing launches under the original's name: the sweep must be clean and
  you give the go.

This is not legal advice. Read the original's terms, run the trademark
checks `replica-brand` lists, and talk to a lawyer before you charge money.

## Credits and license

MIT. Replica skills and tools © 2026 Jake Schincariol
([upstream README](docs/UPSTREAM-README.md)). Agents, orchestrator and docs
© 2026 Damian Torres / [DMLABS](https://dmlabs.mx).
