# The install + capability-scan prompt

Paste the block below to a coding agent (Claude Code or Codex) the first time
you set up Replica Crew. It tells the agent to install the plugin, scan your
computer read-only, and report what you can build before anything else runs.
The agent installs the toolkit itself - it never installs languages, SDKs or
drivers for you; it only tells you what to add.

---

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

---

## What the scan actually touches

`doctor.py` is a single standard-library Python file. It:

- reads environment variables (`ANDROID_HOME`, `ANDROID_SDK_ROOT`, `PATH`);
- runs each known tool with a version flag (e.g. `node --version`), with a
  20-second timeout, and ignores a tool that is absent or whose probe fails;
- checks whether a few directories exist (the Android SDK locations);
- prints a report (and writes `replica/capabilities.json` when the orchestrator
  asks).

It does not write to system folders, does not change `PATH` or any config, does
not download anything, and opens no network connection. You can read the whole
file before running it: `skills/replica-capabilities/doctor.py`.
