# AGENTS.md

Instructions for any coding agent (Codex, Cursor, Gemini CLI, Claude Code)
working with Replica Crew.

## What this repo is

A pipeline for rebuilding an app's **features and flows** (never its code,
brand or content) in eleven phases. Each phase is a playbook in
`replica-<phase>/SKILL.md`. `replica-crew/SKILL.md` is the orchestrator.
`agents/replica-<phase>.md` are Claude Code subagent definitions.

## Using it without Claude Code

1. Read `replica-crew/SKILL.md` for the order and the waves.
2. For each phase, read `replica-<phase>/SKILL.md` and follow it. If your tool
   supports sub-agents or parallel tasks, give each phase its own task and
   run `architect`, `design` and `entrepreneur` together after `recon`.
3. All state lives in `replica/` inside the user's project, so phases can run
   in separate sessions.
4. Run the Python tools with `python` (standard library only), from the
   folder they live in or by full path.

## Hard rules

- Public sources and the user's own account only. No source code, bundles,
  private APIs, decompiling, logos, fonts, copy, or scraping behind logins.
- Binary reverse engineering only if `replica/scope.md` records ownership or
  written authorization.
- No fabricated reviews, metrics, test results or availability checks.
- Never create accounts, buy domains, type passwords or paste live keys.
- Never deploy without the user's explicit go.

## Repo checks

```
python -m unittest discover -s tests -v
python scripts/gen_agents.py agents   # regenerate the 11 agent files
```
