"""replica-doctor: read-only scan of this machine's toolchains.

    python doctor.py              # human-readable report
    python doctor.py --json       # machine-readable, for the orchestrator
    python doctor.py --target android   # only what that target needs

It NEVER installs anything, changes config, or phones home. It runs `--version`
style probes and checks a few paths, then says which Replica Crew target types
this machine can build today and what is missing for the rest.
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys

# tool -> (probe args, homepage for the "how to get it" hint)
# probe args may be None: the tool is only checked for presence on PATH.
TOOLS = {
    "jadx": (["--version"], "github.com/skylot/jadx"),
    "apktool": (["--version"], "apktool.org"),
    "ilspycmd": (["--version"], "github.com/icsharpcode/ILSpy"),
    "rizin": (["-v"], "rizin.re"),
    "llvm-objdump": (["--version"], "llvm.org"),
    "objdump": (["--version"], "gnu.org (binutils)"),
    "analyzeHeadless": (None, "ghidra-sre.org"),
    "ghidra": (None, "ghidra-sre.org"),
    "blutter": (None, "github.com/worawit/blutter"),
    "il2cppdumper": (None, "github.com/Perfare/Il2CppDumper"),
    "pycdc": (None, "github.com/zrax/pycdc"),
    "GoReSym": (None, "github.com/mandiant/GoReSym"),
    "frida": (["--version"], "frida.re"),
    "asar": (["--version"], "github.com/electron/asar"),
    "upx": (["--version"], "github.com/upx/upx"),
    "de4dot": (None, "github.com/0xd4d/de4dot"),
    "diec": (None, "github.com/horsicq/Detect-It-Easy"),
    "x64dbg": (None, "x64dbg.com"),
    "x32dbg": (None, "x64dbg.com"),
    "gdb": (["--version"], "gnu.org (GDB)"),
    "binwalk": (None, "github.com/ReFirmLabs/binwalk"),
    "cutter": (None, "cutter.re"),
    "strings": (["--version"], "gnu.org (binutils)"),
    "node": (["--version"], "nodejs.org"),
    "npm": (["--version"], "nodejs.org"),
    "python3": (["--version"], "python.org"),
    "git": (["--version"], "git-scm.com"),
    "docker": (["--version"], "docker.com"),
    "java": (["-version"], "adoptium.net"),
    "gradle": (["--version"], "gradle.org"),
    "flutter": (["--version"], "flutter.dev"),
    "adb": (["version"], "developer.android.com/tools/adb"),
    "dotnet": (["--version"], "dotnet.microsoft.com"),
    "cargo": (["--version"], "rustup.rs"),
    "go": (["version"], "go.dev"),
    "cmake": (["--version"], "cmake.org"),
    "godot": (["--version"], "godotengine.org"),
    "blender": (["--version"], "blender.org"),
    "ffmpeg": (["-version"], "ffmpeg.org"),
    "playwright": (["--version"], "playwright.dev (npx playwright)"),
    "gh": (["--version"], "cli.github.com"),
    "claude": (["--version"], "claude.com/claude-code"),
    "codex": (["--version"], "developers.openai.com/codex"),
}

# reverse-engineering MCP servers, detected by scanning host config files.
RE_MCP = {
    "GhidraMCP": ["ghidra"],
    "ida-pro-mcp": ["ida-pro", "ida_pro"],
    "jadx-ai-mcp": ["jadx"],
    "apktool-mcp-server": ["apktool"],
    "frida-mcp": ["frida"],
}

# target type -> (need-all, need-any-of, notes)
TARGETS = {
    "web": (["node"], [["npm"]],
            "Static sites and web apps (Next.js, React, Vue). The core target."),
    "desktop": (["node"], [],
                "Electron desktop apps run on Node alone. For Tauri add Rust (cargo); "
                "for native add .NET or Python/Qt."),
    "android": (["java"], [["flutter", "gradle"]],
                "Android apps via Flutter (recommended) or native Gradle. An emulator or "
                "a device with adb is needed to test."),
    "game": (["node"], [],
             "Web-canvas games (Phaser, Three.js, PixiJS) run on Node alone. For a native "
             "engine add Godot; Blender helps for 3D assets."),
    "mashup": (["node"], [],
               "An original game that blends two games' *mechanics* (e.g. voxel building "
               "+ open-world driving). Web-canvas on Node, or add Godot. Your own engine "
               "and assets only; see TARGETS.md."),
}

ANDROID_SDK = [os.environ.get("ANDROID_HOME"), os.environ.get("ANDROID_SDK_ROOT"),
               os.path.expanduser("~/Android/Sdk"),
               os.path.expanduser("~/AppData/Local/Android/Sdk")]


def probe(tool):
    """Return (present, version_line_or_None)."""
    exe = shutil.which(tool)
    if not exe:
        return False, None
    args = TOOLS[tool][0]
    if args is None:
        return True, "present"
    try:
        r = subprocess.run([exe] + args, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=20)
    except Exception as e:  # noqa: BLE001 - a broken tool is just "unknown version"
        return True, "present (version probe failed: %s)" % e.__class__.__name__
    text = ((r.stdout or "") + (r.stderr or "")).strip()
    # Windows app-execution-alias stubs and broken shims answer, but aren't real.
    for dead in ("was not found", "could not be loaded", "is not recognized",
                 "No such file"):
        if dead in text:
            return False, None
    out = text.splitlines()
    return True, (out[0].strip() if out else "present")


def scan():
    found = {}
    for tool in TOOLS:
        present, ver = probe(tool)
        if present:
            found[tool] = ver
    android_sdk = next((p for p in ANDROID_SDK if p and os.path.isdir(p)), None)
    targets = {}
    for name, (need_all, need_any, note) in TARGETS.items():
        missing = [t for t in need_all if t not in found]
        groups_ok = all(any(t in found for t in grp) for grp in need_any)
        ready = not missing and groups_ok
        needs = list(missing)
        for grp in need_any:
            if not any(t in found for t in grp):
                needs.append(" or ".join(grp))
        if name == "android" and not android_sdk:
            needs.append("Android SDK (set ANDROID_HOME)")
            ready = False
        targets[name] = {"ready": ready, "needs": needs, "note": note}
    return {
        "os": "%s %s" % (platform.system(), platform.release()),
        "machine": platform.machine(),
        "cpus": os.cpu_count(),
        "python": platform.python_version(),
        "android_sdk": android_sdk,
        "tools": found,
        "re_mcp": mcp_servers(),
        "targets": targets,
    }


def mcp_servers():
    """Detect known RE MCP servers by scanning host config files (read-only)."""
    paths = [
        os.path.expanduser("~/.claude.json"),
        os.path.expanduser("~/.codex/config.toml"),
        os.path.expanduser("~/.codex/config.json"),
        ".mcp.json",
    ]
    text = ""
    for p in paths:
        try:
            with open(p, encoding="utf-8", errors="ignore") as fh:
                text += fh.read()
        except OSError:
            continue
    lower = text.lower()
    return {name: any(tok in lower for tok in toks)
            for name, toks in RE_MCP.items()}


def how_to_get(tool_expr):
    for tool in TOOLS:
        if tool in tool_expr:
            return TOOLS[tool][1]
    return ""


def human(info, only=None):
    L = ["Replica Crew machine scan (read-only)",
         "  OS: %s (%s), %s CPUs, Python %s" % (
             info["os"], info["machine"], info["cpus"], info["python"]),
         "", "Toolchains found:"]
    L += ["  %-11s %s" % (t, v) for t, v in sorted(info["tools"].items())] or ["  (none)"]
    re_mcp = info.get("re_mcp", {})
    L.append("")
    L.append("Reverse-engineering MCP servers (from host config):")
    L += ["  %-20s %s" % (n, "yes" if v else "no") for n, v in sorted(re_mcp.items())] or ["  (none)"]
    L.append("")
    L.append("What you can build now:")
    for name, t in info["targets"].items():
        if only and name != only:
            continue
        mark = "YES" if t["ready"] else "no "
        L.append("  [%s] %-8s %s" % (mark, name, t["note"]))
        if t["needs"]:
            hints = ", ".join("%s (%s)" % (n, how_to_get(n)) for n in t["needs"])
            L.append("        missing: %s" % hints)
    L.append("")
    ready = [n for n, t in info["targets"].items() if t["ready"]]
    L.append("Ready targets: %s" % (", ".join(ready) if ready else "none yet"))
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--target", choices=list(TARGETS))
    a = ap.parse_args(argv)
    info = scan()
    if a.json:
        if a.target:
            info = {**info, "targets": {a.target: info["targets"][a.target]}}
        print(json.dumps(info, indent=2))
    else:
        print(human(info, a.target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
