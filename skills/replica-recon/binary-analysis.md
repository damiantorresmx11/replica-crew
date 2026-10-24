# Binary analysis with Claude Code and Codex

This playbook belongs to replica-recon. Both hosts run the same workflow,
using installed local tools or a connected decompiler MCP. No paid service
or MCP is required. This supports analysis and authorized source recovery;
it does not promise recovery of the original source project.

## Scope and inputs

Read replica/scope.md first. It must record the user's ownership or written
authorization, local input paths, purpose (analysis or recovery), and permitted
outputs. Reuse authorization already provided; ask only for missing scope.
If absent, return NEEDS_USER to the orchestrator before reading the binary.
Work on a copy. Do not patch, execute, install or load the target. Do not
upload it to third-party services. Do not bypass DRM, licensing or access
controls. Dynamic analysis is a separate explicit scope, never implicit.

## Inventory and tool selection

1. Create replica/binary/ in the user's project. Record the original path,
   size and SHA-256 in manifest.json. Hash the input with Python hashlib in
   chunks or Get-FileHash; record the same hash after analysis.
2. Inspect magic bytes and container entries, not just the file extension.
   Distinguish PE native from managed .NET, ELF, Mach-O, ZIP/APK/JAR and DEX.
   An EXE or DLL is not necessarily .NET. ZIP alone does not prove APK.
   Inspect archives without running their contents, checking entry paths
   for traversal and limiting expanded size before extraction.
3. Read capabilities.json and check the selected executable with command
   discovery (shutil.which / Get-Command). Tool versions and actual paths
   go into the report. doctor.py lists common decompiler CLIs; Ghidra's
   analyzeHeadless and Java JAR tools may need a user-provided absolute path.
   If missing, return PARTIAL with the tool needed. Do not auto-install.

| Format | Installed tool | Output and limitations |
| --- | --- | --- |
| APK / DEX | JADX | reconstructed Java; obfuscation and Kotlin recovery can be incomplete |
| APK resources | Apktool | decoded manifest/resources and smali; not Java source |
| .NET PE assembly | ILSpy CLI (ilspycmd) | reconstructed C# project; native/AOT payloads need native analysis |
| JAR / class | CFR or another installed Java decompiler | reconstructed Java; use local JAR with an absolute path |
| PE native / ELF / Mach-O | Ghidra headless or connected Ghidra MCP | disassembly and pseudocode; symbols/types may be inferred |
| Native inspection | Rizin / llvm-objdump | metadata/disassembly; does not by itself produce high-level source |

## Run static analysis

Use explicit paths and separate argument arrays; never concatenate an input
filename into a shell command. Run one writer per binary, with a timeout and
bounded logs. Keep outputs under replica/binary/<input-id>/; never overwrite
an existing run. Example CLI argument lists (substitute actual paths):

```text
["jadx", "-d", "<new-output>/java", "<input.apk-or.dex>"]
["apktool", "d", "<input.apk>", "-o", "<new-output>/resources"]
["ilspycmd", "-p", "-o", "<new-output>/csharp", "<input.dll>"]
["java", "-jar", "<absolute-cfr.jar>", "<input.jar>", "--outputdir", "<new-output>/java"]
```

For Ghidra, use an isolated project directory and the installed version's
headless importer. Analysis/import alone does not export C pseudocode: use
an installed, inspected export script or a connected decompiler MCP, and
record which functions were actually exported. Never claim decompilation
based only on a successful import or an objdump listing. Native libraries
inside an APK must be analyzed separately. For Flutter AOT, Unity IL2CPP,
packed/encrypted binaries or unsupported architectures, report limitations
and remaining work; do not label metadata or strings as recovered source.

## Evidence and handoff

Write replica/binary/report.md with input IDs and hashes, authorization
reference, detected format/architecture, tool paths and versions, exact
commands, exit codes, output paths, warnings, and coverage. Distinguish
observed facts, inferred behavior and unknowns; cite function/address or
file/line for findings. Redact secrets from reports and keep recovered
artifacts local and out of published source, logs, screenshots and commits.
List incomplete functions and failures even if the process exits zero.

Return DONE only when the requested analysis scope is complete; otherwise
PARTIAL/BLOCKED with the concrete reason and next step. Source recovery
needs a separate build/test check before claiming the recovered app works.
Append the normal recon entry to crew-log.md. Downstream phases read the
report; they must not re-run or overwrite recon's outputs concurrently.

## Tool references

- JADX CLI: https://github.com/skylot/jadx#usage
- ILSpy: https://github.com/icsharpcode/ILSpy
- Apktool: https://apktool.org/
- CFR: https://www.benf.org/other/cfr/
- Ghidra: https://github.com/NationalSecurityAgency/ghidra
