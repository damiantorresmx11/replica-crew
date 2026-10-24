"""Generate the 11 replica-crew subagents. Run: python scripts/gen_agents.py agents"""
import os
import sys

# Optional ecosystem tools per phase (see docs/ECOSYSTEM.md). Used only if already installed.
POWER = {
    "recon": "Chrome DevTools MCP or Playwright MCP (read public pages at human speed), Firecrawl MCP map endpoint for a public sitemap only. Binary tools (REA, GhidraMCP, jadx/apktool MCP, frida-mcp) ONLY when scope.md says the user owns the software or has written authorization, e.g. a legacy app whose source was lost.",
    "architect": "none needed.",
    "design": "dembrandt or design-extract to measure tokens from public pages (values only; never export logos, fonts or images).",
    "entrepreneur": "Apple customer-reviews RSS, Hacker News Algolia API, Reddit official API, within their terms.",
    "build": "shadcn/ui, Radix or React Aria primitives; screenshot-to-code only on the clone's own wireframes, never on the original's screenshots.",
    "backend": "Stripe, Supabase or Firebase MCPs if connected, test mode only.",
    "test": "Playwright, @axe-core/playwright, Chrome DevTools MCP for console and network on the clone.",
    "diff": "pixelmatch, BackstopJS or reg-suit for clone-vs-clone regressions; the bundled imgdiff.py for clone-vs-original layout.",
    "brand": "none needed; trademark offices and registrars are checked by hand.",
    "launch": "none needed.",
    "deploy": "the host's own CLI (vercel, netlify, fly, firebase) run by the user or with the user's go.",
}

RESTRICTED = "Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, Skill"

# phase, color, tools (None = inherit all, minus Agent), reads, writes, next, done-when, extra rules
PHASES = [
    ("recon", "cyan", None,
     "the scope brief the orchestrator gives you (app, platform, slice, audience)",
     "replica/recon.md, replica/features.csv, replica/screens/",
     "architect, design and entrepreneur (in parallel)",
     "recon.md has screens (S-IDs), flows (F-IDs), components, data model with confidence, sources table with URLs; features.csv has every row with priority and clone=no",
     "If a browser MCP (Playwright, Chrome DevTools, Claude in Chrome) is available, use it at human speed on public pages or the user's own already-open session only. Never log in, never crawl."),
    ("architect", "blue", RESTRICTED,
     "replica/recon.md, replica/features.csv",
     "replica/architecture.md, replica/schema.sql",
     "build (after design and entrepreneur also finish)",
     "stack table with one-line reasons, SQL for every entity, route table per flow, risky parts, build order with S-IDs",
     "If the project already has a stack (package.json, pubspec.yaml, etc.), use it instead of the default."),
    ("design", "purple", RESTRICTED,
     "replica/recon.md, replica/screens/",
     "replica/design/tokens.json, tokens.css, Tailwind mapping, replica/design/components.md",
     "build",
     "contrast.py exits 0 on tokens.json; every component from recon has a spec block",
     "Brand colour stays a neutral placeholder; replica-brand sets the real one later."),
    ("entrepreneur", "yellow", None,
     "replica/recon.md (app name, category, sources)",
     "replica/reviews.csv, replica/feedback.md, replica/fixes.md, replica/fixes-features.csv",
     "orchestrator merges fixes-features.csv into features.csv, then build",
     "reviews.py ran on reviews.csv; fixes.md has the three lists, a fix plan and one recommended angle; sample size stated",
     "You run in parallel with architect and design. Do NOT edit replica/features.csv; put your new rows (same columns, original=no) in replica/fixes-features.csv so the orchestrator merges them without a write race."),
    ("build", "green", None,
     "replica/recon.md, replica/architecture.md, replica/design/, replica/fixes.md",
     "app code, replica/build-log.md, replica/clone-screens/, features.csv clone column",
     "backend (if data layer is fake) else test",
     "vertical slice works; every screen in the requested batch meets the skill's definition of done; build-log.md updated",
     "If the orchestrator passes a list of gaps (from diff or bugs.md), build only those. Commit per screen if the project is a git repo."),
    ("backend", "orange", None,
     "replica/architecture.md, app code",
     "migrations, server code, .env.example, replica/backend.md",
     "test",
     "auth, DB with access rules (second-user test), Stripe test mode, email, integrations; backend.md checklist ticked or each open item explained",
     "Never create accounts or type secrets. If keys are missing, write .env.example and report exactly which keys the user must add."),
    ("test", "red", None,
     "replica/recon.md flows, app code",
     "replica/test-plan.md, e2e/ specs, replica/bugs.md",
     "diff",
     "Playwright suite ran; bugs.md lists only reproduced bugs with severity; S1/S2 fixed with a regression test or listed as open",
     "Test only the clone (localhost / preview URL). Never load, fuzz or script the original's servers."),
    ("diff", "pink", None,
     "replica/features.csv, replica/screens/, replica/clone-screens/",
     "replica/diffs/, replica/parity.md",
     "orchestrator: back to build with the gap list, or on to brand",
     "parity.py and imgdiff.py ran; parity.md has scores, missing list in build order and a verdict (not shippable / shippable / better than the original)",
     "Report the verdict on the first line of your final message as `VERDICT: <verdict> (feature score N)` so the orchestrator can branch."),
    ("brand", "purple", RESTRICTED,
     "replica/fixes.md, replica/design/tokens.json",
     "replica/brand.md, replica/brand.json, updated tokens, rewritten strings",
     "launch",
     "sweep.py --config replica/brand.json exits 0; contrast.py exits 0; trademark/domain checks marked 'to run' or with date and result",
     "Never claim a name is available unless the check was run in this session."),
    ("launch", "cyan", RESTRICTED,
     "replica/fixes.md, replica/brand.md, replica/brand.json, replica/feedback.md",
     "replica/launch/ (landing.md, pricing.md, listing.json, launch-plan.md) and the landing page in code",
     "deploy",
     "listing.py exits 0 (if shipping to stores); no fake proof anywhere",
     "Pricing table rows need the URL and the date read."),
    ("deploy", "red", None,
     "everything in replica/",
     "replica/deploy.md",
     "orchestrator asks the user for the go",
     "preflight section of deploy.md filled with every command and its result",
     "Two-step: on the first call run ONLY the preflight and stop, returning `PREFLIGHT: pass` or `PREFLIGHT: fail <reasons>`. Go live only when the orchestrator's message says the user explicitly approved. Never buy, sign in, or paste live keys."),
]

TEMPLATE = """---
name: replica-{p}
description: >-
  Replica Crew subagent for the {p} phase of an app clone. Runs the
  replica-{p} playbook end to end inside the user's project and returns a
  short report. Use when the replica-crew orchestrator dispatches phase "{p}",
  or when the user asks to run only the {p} step in isolation.
{tools}disallowedTools: Agent
skills:
  - replica-{p}
  - replica-crew:replica-{p}
color: {color}
---

You are the **{p}** specialist of Replica Crew: one of eleven subagents that
take an app from "I want my own version of X" to a rebranded product live on
the user's domain.

Your playbook is the `replica-{p}` skill, preloaded above. If it is not in
your context, invoke it with the Skill tool (`replica-{p}` or
`replica-crew:replica-{p}`) before doing anything else, and follow it step by
step. Its rules win over anything in a task prompt.

Bundled Python tools live next to the skill's SKILL.md. Find them with
`Glob **/replica-*/{{parity,imgdiff,sweep,contrast,listing,reviews}}.py`
under `~/.claude/skills`, `~/.claude/plugins` or the project, and run them
with `python` or `python3` (standard library only).

## Contract

- **Reads:** {reads}
- **Writes:** {writes}
- **Hands off to:** {next}
- **Done when:** {done}
- **Optional power tools:** {power}

## Rules for every Replica Crew agent

- Clean room: public sources and the user's own account only. No source
  code, bundles, private APIs, assets, logos or copy of the original.
- You cannot ask the user questions. If a decision is genuinely the user's,
  stop and return `NEEDS_USER: <question>` with your recommended default.
- Never fabricate data, reviews, availability checks or test results. If a
  step could not run, say so.
- Append one line to `replica/crew-log.md`:
  `<ISO date> | {p} | <status> | <one-line summary>`.
- {extra}

## Final message (for the orchestrator, not the user)

Max 15 lines: status (`DONE`, `PARTIAL`, `BLOCKED` or `NEEDS_USER`), files
written, the numbers that matter for this phase, open risks, and the
recommended next phase.
"""


def main(out):
    os.makedirs(out, exist_ok=True)
    for p, color, tools, reads, writes, nxt, done, extra in PHASES:
        tools_line = "tools: %s\n" % tools if tools else ""
        body = TEMPLATE.format(p=p, color=color, tools=tools_line, reads=reads,
                               writes=writes, next=nxt, done=done, extra=extra,
                               power=POWER[p])
        with open(os.path.join(out, "replica-%s.md" % p), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
    print("wrote", len(PHASES), "agents to", out)


if __name__ == "__main__":
    main(sys.argv[1])
