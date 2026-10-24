"""bin_analyze: inventory and identify local binaries for authorized analysis.

    python bin_analyze.py <file> [<file> ...] [--json] [--out DIR]

Read-only. It hashes each input (SHA-256), detects its container format from
magic bytes and structure (not the file extension), reads the architecture and
endianness where possible, flags known runtimes (Go, Flutter AOT, Unity IL2CPP,
Node SEA), and prints the decompiler or disassembler to use with a ready
command line. It writes a manifest.json into --out and never runs a
decompiler, executes the target, or phones home.

Standard library only. Part of the replica-recon binary playbook; run it first
so the agent starts from facts instead of guessing by extension.
"""
import argparse
import hashlib
import json
import os
import shutil
import struct
import sys
import zipfile

PE_MACHINE = {
    0x014C: "x86", 0x8664: "x64", 0x01C0: "arm", 0x01C4: "arm",
    0xAA64: "arm64", 0x0200: "ia64", 0x0166: "mips",
}
ELF_MACHINE = {
    0x03: "x86", 0x3E: "x64", 0x28: "arm", 0xB7: "arm64",
    0x08: "mips", 0xF3: "riscv", 0x15: "ppc", 0x14: "ppc64",
}
MACHO_CPU = {
    0x00000007: "x86", 0x01000007: "x64", 0x0000000C: "arm",
    0x0100000C: "arm64",
}
PYC_MAGIC = {
    3394: "3.7", 3413: "3.8", 3425: "3.9", 3439: "3.10",
    3495: "3.11", 3531: "3.12", 3571: "3.13",
}

# container format -> ordered (tool, command) candidates. {in} and {out} are
# replaced by the input path and the per-input output directory.
TOOL_FOR = {
    "apk": [("jadx", "jadx -d {out}/java {in}"),
            ("apktool", "apktool d {in} -o {out}/resources")],
    "dex": [("jadx", "jadx -d {out}/java {in}")],
    "jar": [("cfr", "java -jar cfr.jar {in} --outputdir {out}/java")],
    "class": [("cfr", "java -jar cfr.jar {in} --outputdir {out}/java")],
    "pe-managed": [("ilspycmd", "ilspycmd -p -o {out}/csharp {in}")],
    "pe-native": [("ghidra", "analyzeHeadless {out}/ghidra project -import {in} -scriptPath <export-scripts> -postScript <export-script>"),
                  ("rizin", "rizin -A -qc \"aa; aac; pdf @ main\" {in}")],
    "elf": [("ghidra", "analyzeHeadless {out}/ghidra project -import {in} -scriptPath <export-scripts> -postScript <export-script>"),
            ("rizin", "rizin -A -qc \"aa; aac; pdf @ main\" {in}")],
    "mach-o": [("ghidra", "analyzeHeadless {out}/ghidra project -import {in} -scriptPath <export-scripts> -postScript <export-script>"),
               ("rizin", "rizin -A -qc \"aa; aac; pdf @ main\" {in}")],
    "pyc": [("pycdc", "pycdc {in}")],
    "asar": [("asar", "npx asar extract {in} {out}")],
    "zip": [("apktool", "apktool d {in} -o {out}/resources")],
    "unknown": [],
}

# runtime -> extra tools, prepended ahead of the container tools.
RUNTIME_TOOL = {
    "go": [("GoReSym", "GoReSym -t -d -p {in}")],
    "flutter": [("blutter", "python -m blutter {in} {out}")],
    "il2cpp": [("Il2CppDumper", "Il2CppDumper global-metadata.dat {in}")],
    "node-sea": [],
}

# Packer / protector / obfuscator fingerprints. key -> (signatures, confidence).
PROTECTION_SIGS = {
    "upx": ([b"UPX!", b"UPX0", b"UPX1"], "high"),
    "themida": ([b"Themida", b"WinLicense"], "high"),
    "vmprotect": ([b"VMProtect", b".vmp0", b".vmp1"], "high"),
    "asprotect": ([b"ASProtect"], "high"),
    "aspack": ([b"ASPack"], "high"),
    "enigma": ([b"Enigma Protector"], "medium"),
    "mpress": ([b"MPRESS", b"MPRESS1"], "high"),
    "pecompact": ([b"PECompact", b"PEC2"], "high"),
    "armadillo": ([b"Armadillo"], "high"),
    "fsg": ([b"FSG!"], "high"),
    "petite": ([b"Petite"], "medium"),
    "confuserex": ([b"ConfuserEx", b"Confuser"], "high"),
    "dotfuscator": ([b"Dotfuscator"], "high"),
    "net-obfuscated": ([b"obfuscated by", b"ObfuscatedBy", b"de4dot"], "medium"),
}

# protection -> unpacking / deobfuscation tool, run after the container tool.
PROTECTION_TOOL = {
    "upx": [("upx", "upx -d {in} -o {out}/unpacked.bin")],
    "themida": [("x64dbg", "dump in x64dbg with ScyllaHide, then rebuild the IAT"),
                ("frida", "frida memory dump of the unpacked image")],
    "vmprotect": [("x64dbg", "dump in x64dbg with ScyllaHide"),
                  ("frida", "frida memory dump")],
    "asprotect": [("x64dbg", "dump in x64dbg with ScyllaHide")],
    "aspack": [("x64dbg", "dump in x64dbg"), ("frida", "frida memory dump")],
    "enigma": [("x64dbg", "dump in x64dbg with ScyllaHide")],
    "mpress": [("upx", "upx -d {in} -o {out}/unpacked.bin")],
    "pecompact": [("x64dbg", "dump in x64dbg"), ("frida", "frida memory dump")],
    "armadillo": [("x64dbg", "dump in x64dbg with ScyllaHide")],
    "fsg": [("upx", "upx -d {in} -o {out}/unpacked.bin")],
    "petite": [("x64dbg", "dump in x64dbg")],
    "confuserex": [("de4dot", "de4dot {in} -o {out}/cleaned")],
    "dotfuscator": [("de4dot", "de4dot {in} -o {out}/cleaned")],
    "net-obfuscated": [("de4dot", "de4dot {in} -o {out}/cleaned")],
}

MCP_HINT = {
    "apk": ["jadx-ai-mcp", "apktool-mcp-server"],
    "dex": ["jadx-ai-mcp"],
    "pe-native": ["GhidraMCP", "ida-pro-mcp"],
    "elf": ["GhidraMCP", "ida-pro-mcp"],
    "mach-o": ["GhidraMCP", "ida-pro-mcp"],
    "go": ["GhidraMCP"],
    "flutter": ["GhidraMCP"],
    "il2cpp": ["GhidraMCP"],
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_head(path, n):
    with open(path, "rb") as fh:
        return fh.read(n)


def detect_pe(data):
    if len(data) < 0x40 or data[:2] != b"MZ":
        return None
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    if e_lfanew + 6 > len(data):
        return None
    if data[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
        return None
    machine = struct.unpack_from("<H", data, e_lfanew + 4)[0]
    arch = PE_MACHINE.get(machine, "0x%04x" % machine)
    managed = (b"mscoree.dll" in data or b"_CorExeMain" in data
               or b"_CorDllMain" in data)
    kind = "pe-managed" if managed else "pe-native"
    return {"format": kind, "arch": arch, "managed": managed,
            "confidence": "high"}


def detect_elf(data):
    if len(data) < 20 or data[:4] != b"\x7fELF":
        return None
    eclass = data[4]
    bits = {1: "32", 2: "64"}.get(eclass, "?")
    endian = {1: "little", 2: "big"}.get(data[5], "?")
    machine = struct.unpack_from("<H" if data[5] == 1 else ">H", data, 18)[0]
    arch = ELF_MACHINE.get(machine, "0x%04x" % machine)
    return {"format": "elf", "arch": arch, "bits": bits, "endian": endian,
            "confidence": "high"}


def is_java_class(data):
    """0xCAFEBABE is also the Mach-O fat magic; use the class version to split."""
    if data[:4] != b"\xca\xfe\xba\xbe" or len(data) < 8:
        return data[:4] == b"\xca\xfe\xba\xbe"
    major = struct.unpack_from(">H", data, 6)[0]
    return 44 <= major <= 90


def detect_macho(data):
    if len(data) < 8:
        return None
    be = struct.unpack_from(">I", data, 0)[0]
    le = struct.unpack_from("<I", data, 0)[0]
    if be == 0xCAFEBABE or le == 0xCAFEBABE:
        if is_java_class(data):
            return None
        return {"format": "mach-o", "arch": "universal", "confidence": "high"}
    if be in (0xFEEDFACE, 0xFEEDFACF) or le in (0xFEEDFACE, 0xFEEDFACF):
        bits = "64" if (be == 0xFEEDFACF or le == 0xFEEDFACF) else "32"
        cpu_le = struct.unpack_from("<I", data, 4)[0]
        cpu_be = struct.unpack_from(">I", data, 4)[0]
        if cpu_le in MACHO_CPU:
            endian, cpu = "little", cpu_le
        elif cpu_be in MACHO_CPU:
            endian, cpu = "big", cpu_be
        else:
            endian, cpu = "little", cpu_le
        arch = MACHO_CPU.get(cpu, "0x%08x" % cpu)
        return {"format": "mach-o", "arch": arch, "bits": bits, "endian": endian,
                "confidence": "high"}
    return None


def detect_dex(data):
    if data[:4] == b"dex\n":
        ver = data[4:7].decode("ascii", "replace")
        return {"format": "dex", "arch": "jvm", "version": ver,
                "confidence": "high"}
    return None


def detect_java_class(data):
    if is_java_class(data):
        return {"format": "class", "arch": "jvm", "confidence": "high"}
    return None


def detect_asar(path, size):
    if size < 4:
        return None
    data = read_head(path, 4)
    n = struct.unpack("<I", data)[0]
    if n <= 0 or n > size - 4 or n > (1 << 24):
        return None
    header = read_head(path, 4 + n)[4:]
    try:
        obj = json.loads(header.decode("utf-8", "replace"))
    except (ValueError, UnicodeDecodeError):
        return None
    if isinstance(obj, dict) and ("files" in obj or "header" in obj):
        return {"format": "asar", "arch": "n/a", "confidence": "high"}
    return None


def detect_pyc(data):
    if len(data) < 4:
        return None
    magic = struct.unpack("<I", data[:4])[0]
    if magic in PYC_MAGIC:
        return {"format": "pyc", "arch": "python",
                "version": PYC_MAGIC[magic], "confidence": "high"}
    return None


def classify_zip(path, size):
    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
    except (zipfile.BadZipFile, OSError):
        return None
    joined = " ".join(names).lower()
    has_manifest = any(n.endswith("AndroidManifest.xml") for n in names)
    has_dex = any(n.endswith(".dex") for n in names)
    has_class = any(n.endswith(".class") for n in names)
    if has_manifest and has_dex:
        fmt = "apk"
    elif has_dex:
        fmt = "dex"
    elif has_class:
        fmt = "jar"
    else:
        fmt = "zip"
    info = {"format": fmt, "arch": "n/a", "confidence": "high"}
    notes = []
    if "libapp.so" in joined:
        notes.append("Flutter AOT payload (libapp.so)")
    if "libil2cpp.so" in joined or "global-metadata.dat" in joined:
        notes.append("Unity IL2CPP payload")
    if notes:
        info["notes"] = notes
    return info


def detect_runtime(data):
    if b"NODE_SEA_BLOB" in data:
        return "node-sea"
    if (b"kDartVmSnapshotData" in data or b"kDartIsolateSnapshotData" in data
            or b"\xdc\xdc\xf5\xf5\xdc\xdc\xf5\xf5" in data):
        return "flutter"
    if b"global-metadata.dat" in data or b"il2cpp" in data.lower():
        return "il2cpp"
    if b"Go build ID:" in data or b"Go buildinf:" in data or b".note.go.buildid" in data:
        return "go"
    return None


def detect_protection(data):
    """Return a list of {name, confidence} for detected packers/obfuscators."""
    found = []
    for name, (sigs, confidence) in PROTECTION_SIGS.items():
        if any(sig in data for sig in sigs):
            found.append({"name": name, "confidence": confidence})
    return found


def detect(path):
    size = os.path.getsize(path)
    blob = read_head(path, min(size, 1 << 20))
    head = blob[:64]
    info = None
    for fn in (detect_pe, detect_elf, detect_macho, detect_dex,
               detect_java_class, detect_pyc):
        r = fn(blob)
        if r:
            info = r
            break
    if info is None:
        asar = detect_asar(path, size)
        if asar:
            info = asar
        elif head[:4] in (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08"):
            info = classify_zip(path, size)
    if info is None:
        info = {"format": "unknown", "arch": "n/a", "confidence": "low",
                "notes": ["no magic bytes matched; inspect with a hex editor"]}
    runtime = detect_runtime(blob)
    if runtime:
        info["runtime"] = runtime
    protection = detect_protection(blob)
    if protection:
        info["protection"] = protection
    return info


def recommend(fmt, runtime, protections, outdir, inpath):
    rows = []
    for prot in protections or []:
        for tool, cmd in PROTECTION_TOOL.get(prot["name"], []):
            probe = shutil.which(tool)
            rows.append({
                "tool": tool,
                "installed": bool(probe),
                "path": probe,
                "cmd": cmd.replace("{out}", outdir).replace("{in}", inpath),
            })
    for tool, cmd in RUNTIME_TOOL.get(runtime, []):
        probe = shutil.which(tool)
        rows.append({
            "tool": tool,
            "installed": bool(probe),
            "path": probe,
            "cmd": cmd.replace("{out}", outdir).replace("{in}", inpath),
        })
    for tool, cmd in TOOL_FOR.get(fmt, []):
        probe = shutil.which(tool)
        rows.append({
            "tool": tool,
            "installed": bool(probe),
            "path": probe,
            "cmd": cmd.replace("{out}", outdir).replace("{in}", inpath),
        })
    mcp = MCP_HINT.get(runtime, []) + MCP_HINT.get(fmt, [])
    return rows, mcp


def analyze(path, outdir):
    size = os.path.getsize(path)
    info = detect(path)
    info.update({
        "path": os.path.abspath(path),
        "size": size,
        "sha256": sha256(path),
    })
    ident = os.path.splitext(os.path.basename(path))[0] or "binary"
    per_input_out = os.path.join(outdir, ident)
    runtime = info.get("runtime")
    protections = info.get("protection")
    tools, mcp = recommend(info["format"], runtime, protections, per_input_out,
                           os.path.abspath(path))
    info["out"] = per_input_out
    info["tools"] = tools
    info["mcp_hint"] = mcp
    return info


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default=os.path.join(".", "replica", "binary"))
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    results = [analyze(f, a.out) for f in a.files]
    manifest = os.path.join(a.out, "manifest.json")
    payload = {"created_by": "bin_analyze", "inputs": results}
    with open(manifest, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    if a.json:
        print(json.dumps(payload, indent=2))
    else:
        for r in results:
            print("%s  %s" % (r["sha256"][:12], r["path"]))
            print("  format=%s arch=%s confidence=%s size=%d%s" % (
                r["format"], r["arch"], r["confidence"], r["size"],
                (" runtime=" + r["runtime"]) if r.get("runtime") else ""))
            for note in r.get("notes", []):
                print("  note: %s" % note)
            for prot in r.get("protection", []):
                print("  protection: %s (%s)" % (prot["name"], prot["confidence"]))
            if r["tools"]:
                pick = next((t for t in r["tools"] if t["installed"]),
                            r["tools"][0])
                print("  recommended: %s" % pick["tool"])
                print("  command: %s" % pick["cmd"])
                missing = [t["tool"] for t in r["tools"] if not t["installed"]]
                if missing:
                    print("  not installed: %s" % ", ".join(missing))
            else:
                print("  no tool mapped for this format; inspect manually")
            if r["mcp_hint"]:
                print("  mcp alternative: %s" % ", ".join(r["mcp_hint"]))
    print("wrote %s" % manifest, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
