---
name: replica-crew
description: >-
  Orchestrates the whole Replica pipeline with eleven specialist subagents
  (recon, architect, design, entrepreneur, build, backend, test, diff, brand,
  launch, deploy): runs independent phases in parallel, loops build, test and
  diff until the clone is shippable, and stops for the user only at scope and
  before going live. Use when the user says "clone this app end to end",
  "run the whole replica", "replica crew", "build my own version of X from
  start to finish", "use the 11 agents", or gives an app URL and wants the
  full pipeline instead of one step.
---

# replica-crew

The eleven `replica-*` skills are the playbooks. This skill is the conductor:
it never does a phase's work itself, it dispatches the matching subagent,
reads the short report, decides the next wave, and keeps the user posted.

Subagent types (use whichever exists in this session):

| phase | plugin install | manual install |
| --- | --- | --- |
| each phase `X` | `replica-crew:replica-X` | `replica-X` |

If neither is available, fall back to running the `replica-X` skill in the
main thread, one phase at a time. Same files, same order, just slower.

## Wave 0: scope (main thread, with the user)

Subagents cannot ask the user anything, so settle it here. Ask, or propose
and get one yes:

1. The app and platform (web, iOS, Android, desktop) and its URL.
2. The slice: the core loop users pay for, not "all of it".
3. Who the clone is for, and the project folder to build in.
4. Stack: the project's existing one, or the replica-architect default.
5. How far to go: `plan` (waves 1-2), `build` (to wave 4), or `ship` (all).
6. Ownership: does the user own the target or hold written authorization
   (e.g. their own legacy app with lost source)? Default `no`. Only `yes`
   unlocks the binary tools listed in `docs/ECOSYSTEM.md` for recon.

Read the clean-room rules in `replica-recon` and say them in one line. If the
user wants anything they forbid (copying code, logging into someone else's
account, scraping behind a login, cloning the brand), decline that part and
continue with the rest.

Create `replica/` and `replica/crew-log.md` with a header line. Write the
answers to `replica/scope.md`. Every dispatch prompt includes the path to
`scope.md` and the project root.

## Wave 1: recon

Dispatch `replica-recon`. When it returns, show the user its five-line
summary (core loop, counts, hardest parts, out of scope, size). If the size
is XL, propose a smaller slice before going on. This is the only mid-pipeline
check-in; after it, keep going unless an agent returns `NEEDS_USER`.

## Wave 2: in parallel

Dispatch **architect, design and entrepreneur in one message** (three Agent
calls in the same response). None depends on another; all read recon.

After all three return, merge `replica/fixes-features.csv` into
`replica/features.csv` (append rows, skip duplicates by `feature`). Then the
fixes get built in from the start, not bolted on after a diff.

Stop here if the scope says `plan`.

## Wave 3: build, backend

Dispatch `replica-build`. Then `replica-backend` if the build used a fake data
layer. Never run them in parallel: both edit app code.

## Wave 4: the quality loop

```
repeat up to 3 times:
    replica-test        # fixes S1/S2, writes bugs.md
    replica-diff        # first line: VERDICT: ... (feature score N)
    if verdict is shippable or better: break
    replica-build with only the gap list from parity.md and open bugs
```

After three rounds without `shippable`, stop and show the user the parity
report and the top five gaps. Do not loop forever and do not round numbers up.

Stop here if the scope says `build`.

## Wave 5: brand, launch

Sequential: `replica-brand`, then `replica-launch` (launch needs the name).

## Wave 6: deploy, two steps

1. Dispatch `replica-deploy` for preflight only.
2. Show the user the preflight results and ask for an explicit go. Without
   it, stop. With it, continue the same agent (SendMessage, if the session
   has it) or dispatch again with "user approved go-live on <date>".

## Dispatch prompt template

```
Phase: <X>. Project root: <path>. Scope: <path>/replica/scope.md.
Inputs ready: <files from earlier waves>.
<only for build loops: Gap list: ...>
Follow your replica-<X> playbook. Return your report in the agreed format.
```

Keep prompts short; the playbook is already in the agent's context.

## Reporting to the user

One line per finished phase as it lands (`recon done: 14 screens, 6 flows,
size M`). At the end: what was built, parity verdict and score, open bugs by
severity, what the user must do by hand (keys, accounts, domain, trademark
search), and the live URL if deployed. Numbers come from the agents' reports
and the tools, never estimated.
