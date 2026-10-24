"""Install Replica Crew for Claude Code and/or Codex.

    python scripts/install.py              # both, whatever is on PATH
    python scripts/install.py --codex      # only Codex
    python scripts/install.py --claude     # only Claude Code
    python scripts/install.py --mcp        # also add the free browser MCP servers
    python scripts/install.py --uninstall  # remove what this script copied

Claude Code gets the plugin (skills + 11 subagents) from the GitHub
marketplace. Codex gets the skills in ~/.agents/skills and the 11 custom
agents in ~/.codex/agents. Existing folders with the same name are left alone
unless --force.
"""
import argparse
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")
CODEX_SKILLS = os.path.join(HOME, ".agents", "skills")
CODEX_AGENTS = os.path.join(HOME, ".codex", "agents")
MARKETPLACE = "damiantorresmx11/replica-crew"
# Free, no-key browser MCP servers used by recon and test.
MCP = {
    "playwright": ["npx", "-y", "@playwright/mcp@latest"],
    "chrome-devtools": ["npx", "-y", "chrome-devtools-mcp@latest"],
}


def run(cmd):
    print("  $ " + " ".join(cmd))
    exe = shutil.which(cmd[0])
    if not exe:
        print("    skipped: %s not on PATH" % cmd[0])
        return False
    r = subprocess.run([exe] + cmd[1:], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    print("    " + (out[-1] if out else "ok"))
    return r.returncode == 0


def skills():
    root = os.path.join(REPO, "skills")
    return sorted(d for d in os.listdir(root) if os.path.isfile(os.path.join(root, d, "SKILL.md")))


def codex(force, uninstall):
    print("Codex")
    os.makedirs(CODEX_SKILLS, exist_ok=True)
    os.makedirs(CODEX_AGENTS, exist_ok=True)
    for name in skills():
        dst = os.path.join(CODEX_SKILLS, name)
        if uninstall:
            if os.path.isfile(os.path.join(dst, "SKILL.md")):
                shutil.rmtree(dst)
            continue
        if os.path.exists(dst) and not force:
            print("  kept existing skill %s (use --force to replace)" % name)
            continue
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(os.path.join(REPO, "skills", name), dst,
                        ignore=shutil.ignore_patterns("node_modules", "__pycache__"))
    agents_src = os.path.join(REPO, "codex", "agents")
    for fn in sorted(os.listdir(agents_src)):
        dst = os.path.join(CODEX_AGENTS, fn)
        if uninstall:
            if os.path.exists(dst):
                os.remove(dst)
            continue
        shutil.copyfile(os.path.join(agents_src, fn), dst)
    verb = "removed" if uninstall else "installed"
    print("  %s %d skills in %s and %d agents in %s" % (
        verb, len(skills()), CODEX_SKILLS, len(os.listdir(agents_src)), CODEX_AGENTS))


def claude(uninstall):
    print("Claude Code")
    if uninstall:
        run(["claude", "plugin", "uninstall", "replica-crew@replica-crew"])
        return
    run(["claude", "plugin", "marketplace", "add", MARKETPLACE])
    run(["claude", "plugin", "marketplace", "update", "replica-crew"])
    run(["claude", "plugin", "install", "replica-crew@replica-crew"])


def mcp(targets):
    print("MCP servers")
    for name, cmd in MCP.items():
        if "claude" in targets:
            run(["claude", "mcp", "add", "--scope", "user", name, "--"] + cmd)
        if "codex" in targets:
            run(["codex", "mcp", "add", name, "--"] + cmd)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--claude", action="store_true")
    ap.add_argument("--codex", action="store_true")
    ap.add_argument("--mcp", action="store_true", help="add Playwright and Chrome DevTools MCP servers")
    ap.add_argument("--force", action="store_true", help="replace same-named Codex skills")
    ap.add_argument("--uninstall", action="store_true")
    a = ap.parse_args(argv)
    targets = [t for t in ("claude", "codex") if getattr(a, t)]
    if not targets:
        targets = [t for t in ("claude", "codex") if shutil.which(t)]
    if not targets:
        sys.exit("Neither claude nor codex is on PATH. Pass --codex to install files anyway.")
    if "codex" in targets:
        codex(a.force, a.uninstall)
    if "claude" in targets:
        claude(a.uninstall)
    if a.mcp and not a.uninstall:
        mcp(targets)
    print("Done. Claude: /replica-crew <url>. Codex: $replica-crew <url>.")


if __name__ == "__main__":
    main()
