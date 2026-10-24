# AGENTS.md

Instructions for any coding agent (Codex, Claude Code, Cursor, Gemini CLI)
working with or inside Replica Crew.

## What this repo is

One repo with everything needed to clone apps and websites with coding
agents:

- `skills/replica-crew/SKILL.md`: the orchestrator and single entry point.
  It picks a mode (`product`, `faithful`, `study`) and runs the phases.
- `skills/replica-<phase>/`: the eleven Replica playbooks (recon, architect,
  design, entrepreneur, build, backend, test, diff, brand, launch, deploy).
- `skills/replica-recon/bin_analyze.py` and `binary-analysis.md`: inventory,
  format detection and tool selection for authorized binary analysis.
- `skills/<other>/`: 15 bundled third-party skills (faithful clones, design
  extraction, UI to code, store screenshots). See `THIRD_PARTY_NOTICES.md`.
- `agents/*.md`: the eleven phase subagents for Claude Code.
- `codex/agents/*.toml`: the same eleven subagents for Codex.
- `docs/ECOSYSTEM.md`: 70+ related tools, bundled or linked.

## Install

```
python scripts/install.py            # Claude Code and/or Codex, whatever is on PATH
python scripts/install.py --codex    # skills to ~/.agents/skills, agents to ~/.codex/agents
python scripts/install.py --mcp      # also Playwright and Chrome DevTools MCP servers
```

## Using it from Codex

1. Start with `$replica-crew <app or site url>`.
2. The orchestrator spawns the custom agents `replica-recon`, ...,
   `replica-deploy`. Spawn `replica-architect`, `replica-design` and
   `replica-entrepreneur` in the same turn after recon.
3. All state lives in `replica/` inside the user's project, so phases can run
   in separate sessions.
4. Python tools are standard library only: `python <path>/parity.py ...`.

## Hard rules

- `product` mode (default): public sources and the user's own account only.
  No source code, bundles, private APIs, decompiling, logos, fonts, copy, or
  scraping behind logins.
- `faithful` mode and binary reverse engineering only if `replica/scope.md`
  records that the user owns the target or holds written authorization.
- No fabricated reviews, metrics, test results or availability checks.
- Never create accounts, buy domains, type passwords or paste live keys.
- Never deploy without the user's explicit go.

## Repo checks

```
python -m unittest discover -s tests -v
python scripts/gen_agents.py      # regenerate agents/*.md and codex/agents/*.toml
```
