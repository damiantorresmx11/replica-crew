#!/usr/bin/env node
// faithful-capture: make a verbatim local copy of a web page the user OWNS or
// is authorized to copy (migration, backup, lost-source recovery). It keeps the
// page's own CSS, assets and scripts, so the real animations re-run locally.
//
// This copies the ORIGINAL site's code and assets (the owner's copyright). It is
// gated: it refuses to run unless authorization is recorded. Output is local;
// it never publishes or hosts anything.
//
//   node capture.mjs <url> [--out DIR] [--scope PATH] [--i-have-authorization]
//                     [--chrome PATH] [--wait MS] [--no-scripts]
//
// Authorization: either `--i-have-authorization`, or a scope file (default
// ./replica/scope.md, or --scope PATH) whose text says the user owns / is
// authorized to copy the target (an "Authorization" section, "I own",
// "authorized", "written permission", etc.). Otherwise it stops and explains.
//
// Requires single-file-cli (npm i single-file-cli) and a Chrome/Chromium.

import { existsSync, readFileSync, mkdirSync, readdirSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";
import path from "node:path";

function parseArgs(argv) {
  const a = { wait: 3000, scripts: true, out: "replica/capture", scope: "replica/scope.md" };
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    const t = argv[i];
    if (t === "--i-have-authorization") a.auth = true;
    else if (t === "--no-scripts") a.scripts = false;
    else if (t === "--out") a.out = argv[++i];
    else if (t === "--scope") a.scope = argv[++i];
    else if (t === "--chrome") a.chrome = argv[++i];
    else if (t === "--wait") a.wait = Number(argv[++i]);
    else if (t.startsWith("--")) fail(`unknown option ${t}`);
    else rest.push(t);
  }
  a.url = rest[0];
  return a;
}

function fail(msg) {
  console.error("faithful-capture: " + msg);
  process.exit(1);
}

// Authorization is the user's to assert. We require it to be explicit, and we
// never infer it from the target site's own content.
function authorized(a) {
  if (a.auth) return "flag --i-have-authorization";
  if (existsSync(a.scope)) {
    const t = readFileSync(a.scope, "utf8").toLowerCase();
    const says =
      /##\s*authorization/.test(t) ||
      /\bi (own|have (written )?permission|am authorized)\b/.test(t) ||
      /\bauthoriz(ed|ation)\b/.test(t) ||
      /\bownership:\s*yes\b/.test(t);
    if (says) return `scope file ${a.scope}`;
  }
  return null;
}

function findChrome(explicit) {
  if (explicit) return explicit;
  const envp = [process.env.CHROME_PATH, process.env.CHROME_EXECUTABLE].filter(Boolean);
  const guesses = [
    ...envp,
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    (process.env.LOCALAPPDATA || "") + "/Google/Chrome/Application/chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ];
  return guesses.find((p) => p && existsSync(p)) || null;
}

function resolveSingleFile() {
  const require = createRequire(import.meta.url);
  for (const id of ["single-file-cli/single-file", "single-file-cli"]) {
    try {
      return require.resolve(id);
    } catch {
      /* try next */
    }
  }
  return null;
}

function main() {
  const a = parseArgs(process.argv.slice(2));
  if (!a.url || !/^https?:\/\//.test(a.url)) fail("pass a http(s) URL to capture");

  const why = authorized(a);
  if (!why) {
    fail(
      "refusing to capture: no authorization recorded.\n" +
        "  This copies the original site's code and assets (the owner's copyright).\n" +
        "  Run it only on a site you own or are authorized to copy, and either:\n" +
        `    - add an 'Authorization' note (or 'ownership: yes') to ${a.scope}, or\n` +
        "    - pass --i-have-authorization\n" +
        "  See the skill's SKILL.md."
    );
  }
  console.log(`faithful-capture: authorization = ${why}`);

  const chrome = findChrome(a.chrome);
  if (!chrome) fail("no Chrome/Chromium found; pass --chrome <path> or set CHROME_PATH");
  const sf = resolveSingleFile();
  if (!sf) fail("single-file-cli not installed. Run: npm i single-file-cli");

  mkdirSync(a.out, { recursive: true });
  const host = new URL(a.url).hostname.replace(/[^a-z0-9.-]/gi, "_");
  const outfile = `${host}.html`;

  const args = [
    sf,
    `--browser-executable-path=${chrome}`,
    `--block-scripts=${a.scripts ? "false" : "true"}`,
    "--browser-wait-until=networkIdle",
    `--browser-wait-delay=${a.wait}`,
    "--load-deferred-content=true",
    "--remove-hidden-elements=false",
    "--manifest",
    `--filename-template=${outfile}`,
    a.url,
  ];
  console.log(`faithful-capture: capturing ${a.url}\n  chrome: ${chrome}\n  scripts kept: ${a.scripts}\n  out: ${path.resolve(a.out, outfile)}`);
  const r = spawnSync(process.execPath, args, { cwd: a.out, stdio: "inherit" });
  if (r.status !== 0) fail("single-file exited with code " + r.status);

  const saved = readdirSync(a.out).filter((f) => f.endsWith(".html"));
  console.log(
    `\nfaithful-capture: done. ${saved.join(", ")} in ${path.resolve(a.out)}\n` +
      "  Local only. The capture is the original site's copyrighted code/assets;\n" +
      "  do not publish or host it without the owner's written permission."
  );
}

main();
