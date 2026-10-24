# Ecosystem: 80+ open-source tools for AI app cloning (October 2026)

Every project below was checked against the GitHub API on 2026-10-23 or
2026-10-24 (name, license, rounded stars). **Bundled** means its skill ships
inside this repo under `skills/` (see `THIRD_PARTY_NOTICES.md`). Everything
else is an app, library, MCP server or list, or has no license that allows
redistribution, so it is linked, not copied. Agents use those only if they
are already installed, and only inside the clean-room rules.

Bundled: replica-skill (11 skills), clone-website, clone-team, web-clone,
clone-study, design-mirror, stitch-extract-design-md,
stitch-extract-static-html, design-md, site-md, stitch-react-components,
shadcn-ui, restyle, video-to-ui, app-store-screenshots, ui-image-to-code.

## Full pipelines and clone skills

| Project | License | Stars | What it does | Phase | Type |
| --- | --- | --- | --- | --- | --- |
| [Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill) | MIT | ~5.1k | 11 Claude skills: recon to deploy. **Replica Crew is built on it.** | all | skills |
| [JCodesMore/ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template) | MIT | ~37k | `/clone-website` skill: recon, assets, components, assembly | recon, build | skill |
| [Jane-xiaoer/claude-skill-web-clone](https://github.com/Jane-xiaoer/claude-skill-web-clone) | MIT | ~1.1k | Faithful clone of static, React or WebGL sites | recon, build | skill |
| [firecrawl/open-lovable](https://github.com/firecrawl/open-lovable) | MIT | ~29k | Rebuilds a site as a React app from a URL | recon, build | app |
| [abi/screenshot-to-code](https://github.com/abi/screenshot-to-code) | MIT | ~81k | Screenshot to HTML/Tailwind/React/Vue | build | app |
| [Varalix-Digitech-Solutions/clone-team](https://github.com/Varalix-Digitech-Solutions/clone-team) | MIT | ~26 | Agent team cloning UI and behaviour | all | agents |
| [luukalleman/clone-study](https://github.com/luukalleman/clone-study) | MIT | ~26 | Studies and recreates award-level sites | design, build | skill |
| [brightdata/skills](https://github.com/brightdata/skills) (`design-mirror`) | MIT | ~268 | Captures a site's look and applies it to your project (needs Bright Data) | design | skill |
| [morluto/rea](https://github.com/morluto/rea) | MIT | see note | "Reverse Engineer Anything": agents + Ghidra/IDA/Hopper, JS/Electron, .NET | recon, binary RE | MCP + CLI |
| [AIshihzong/awesome-reverse-engineer-anything](https://github.com/AIshihzong/awesome-reverse-engineer-anything) | CC0-1.0 | ~141 | Curated list, with a legal section | reference | list |

Note on REA: the API reports ~374k stars, press figures jump from ~30k to
~348k within two weeks. Do not read the star count as a quality signal.

## Browser and recon

| Project | License | Stars | Phase | Type |
| --- | --- | --- | --- | --- |
| [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Apache-2.0 | ~54k | recon, test | MCP |
| [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | Apache-2.0 | ~39k | recon, test | MCP |
| [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | Apache-2.0 | ~44k | recon, test | CLI |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | MIT | ~119k | recon, test | library |
| [firecrawl/firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server) | MIT | ~7.7k | recon (sitemaps) | MCP |

## Design extraction

| Project | License | Stars | Type |
| --- | --- | --- | --- |
| [dembrandt/dembrandt](https://github.com/dembrandt/dembrandt) | MIT | ~3.8k | CLI, design tokens from a URL |
| [Manavarya09/design-extract](https://github.com/Manavarya09/design-extract) | MIT | ~4.3k | CLI, DTCG tokens |
| [arvindrk/extract-design-system](https://github.com/arvindrk/extract-design-system) | MIT | ~253 | CLI |
| [projectwallace/css-analyzer](https://github.com/projectwallace/css-analyzer) | MIT | ~366 | library, CSS stats |
| [BuilderIO/figma-html](https://github.com/BuilderIO/figma-html) | MIT | ~3.7k | site to editable Figma |

Use them to **measure** roles and scales. Never export the target's logos,
icons, images or licensed fonts; `replica-design` explains why.

## Visual diff and fidelity

| Project | License | Stars | Type |
| --- | --- | --- | --- |
| [garris/BackstopJS](https://github.com/garris/BackstopJS) | MIT | ~7.2k | visual regression CLI |
| [mapbox/pixelmatch](https://github.com/mapbox/pixelmatch) | ISC | ~7.0k | pixel diff library |
| [reg-viz/reg-suit](https://github.com/reg-viz/reg-suit) | MIT | ~1.3k | visual regression with reports |
| [NoviScl/Design2Code](https://github.com/NoviScl/Design2Code) | MIT | ~603 | screenshot-to-code fidelity metrics |

## Binary reverse engineering (owned or authorized software only)

| Project | License | Stars | Target |
| --- | --- | --- | --- |
| [LaurieWired/GhidraMCP](https://github.com/LaurieWired/GhidraMCP) | Apache-2.0 | ~11.5k | native binaries via Ghidra |
| [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) | MIT | ~13k | IDA Pro (paid license) |
| [zinja-coder/jadx-ai-mcp](https://github.com/zinja-coder/jadx-ai-mcp) | Apache-2.0 | ~2.9k | Android APK (JADX) |
| [zinja-coder/apktool-mcp-server](https://github.com/zinja-coder/apktool-mcp-server) | Apache-2.0 | ~679 | Android resources and smali |
| [dnakov/frida-mcp](https://github.com/dnakov/frida-mcp) | MIT | ~458 | runtime instrumentation |

Decompilers and CLI tools (linked, not bundled). The `bin_analyze.py`
inventory script and the `binary-analysis.md` playbook reference these:

| Project | License | Stars | Target |
| --- | --- | --- | --- |
| [skylot/jadx](https://github.com/skylot/jadx) | Apache-2.0 | ~51.2k | APK/DEX to Java |
| [iBotPeaches/Apktool](https://github.com/iBotPeaches/Apktool) | Apache-2.0 | ~26.6k | APK resources and smali |
| [icsharpcode/ILSpy](https://github.com/icsharpcode/ILSpy) | MIT | ~26.8k | .NET to C# |
| [NationalSecurityAgency/ghidra](https://github.com/NationalSecurityAgency/ghidra) | Apache-2.0 | ~93.7k | native PE/ELF/Mach-O |
| [rizinorg/rizin](https://github.com/rizinorg/rizin) | LGPL-3.0 | ~4.0k | disassembly/analysis |
| [worawit/blutter](https://github.com/worawit/blutter) | MIT | ~2.8k | Flutter AOT (libapp.so) |
| [Perfare/Il2CppDumper](https://github.com/Perfare/Il2CppDumper) | MIT | ~9.5k | Unity IL2CPP |
| [mandiant/GoReSym](https://github.com/mandiant/GoReSym) | MIT | ~1.1k | Go symbol recovery |
| [electron/asar](https://github.com/electron/asar) | MIT | ~2.9k | Electron asar unpack |
| [zrax/pycdc](https://github.com/zrax/pycdc) | GPL-3.0 | ~4.7k | Python bytecode |

Packers, unpackers, debuggers and deobfuscators for protected binaries
(linked, not bundled). Used when a binary is packed, protected or obfuscated
and `scope.md` authorizes the work:

| Project | License | Stars | Target |
| --- | --- | --- | --- |
| [upx/upx](https://github.com/upx/upx) | GPL-2.0 | ~18.0k | static unpack (UPX, MPRESS, FSG) |
| [0xd4d/de4dot](https://github.com/0xd4d/de4dot) | GPL-3.0 | ~7.4k | .NET deobfuscation (ConfuserEx, Dotfuscator) |
| [horsicq/Detect-It-Easy](https://github.com/horsicq/Detect-It-Easy) | MIT | ~11.8k | packer/protector detection |
| [x64dbg/x64dbg](https://github.com/x64dbg/x64dbg) | GPL-3.0 | ~50.0k | debugger, dynamic unpacking |
| [x64dbg/ScyllaHide](https://github.com/x64dbg/ScyllaHide) | GPL-3.0 | ~4.4k | anti-debug/anti-VM bypass |
| [ReFirmLabs/binwalk](https://github.com/ReFirmLabs/binwalk) | MIT | ~14.5k | firmware and embedded extraction |
| [rizinorg/cutter](https://github.com/rizinorg/cutter) | GPL-3.0 | ~20.1k | Rizin GUI |

The recon agent may use these **only** when `replica/scope.md` records that
the user owns the software or holds written authorization (a legacy app
whose source was lost, an interoperability job you are licensed for). Once
that scope is recorded, the authorized-analysis mode turns on and recon runs
the full toolbox. For anyone else's app, the default clean-room rules apply:
features and flows from public sources, no decompiling, no private APIs.

## Where each tool plugs in

| Agent | Optional tools |
| --- | --- |
| recon | Chrome DevTools MCP, Playwright MCP, Firecrawl sitemap; binary MCPs only with ownership |
| design | dembrandt, design-extract (values only) |
| entrepreneur | Apple reviews RSS, HN Algolia API, Reddit official API |
| build | shadcn/ui, Radix, React Aria |
| backend | Stripe, Supabase, Firebase MCPs in test mode |
| test | Playwright, axe-core, Chrome DevTools MCP on the clone |
| diff | bundled `imgdiff.py`; pixelmatch, BackstopJS, reg-suit for clone regressions |
| deploy | the host's own CLI, with the user's go |

## Added 2026-10-24

### Figma and design-to-code

| Project | License | Stars | Type | Notes |
| --- | --- | --- | --- | --- |
| [GLips/Figma-Context-MCP](https://github.com/GLips/Figma-Context-MCP) | MIT | ~16k | MCP | Figma layout for agents |
| [grab/cursor-talk-to-figma-mcp](https://github.com/grab/cursor-talk-to-figma-mcp) | MIT | ~7.1k | MCP | read/write Figma from Claude, Codex, Cursor |
| [figma/mcp-server-guide](https://github.com/figma/mcp-server-guide) | none detected | ~2.1k | plugin + 32 skills | official guide; not bundled (no license) |
| [awdr74100/figwright](https://github.com/awdr74100/figwright) | MIT | ~1.2k | MCP + skills | skills need its MCP |
| [gethopp/figma-mcp-bridge](https://github.com/gethopp/figma-mcp-bridge) | MIT | ~830 | MCP | |
| [arinspunk/claude-talk-to-figma-mcp](https://github.com/arinspunk/claude-talk-to-figma-mcp) | MIT | ~670 | MCP | |
| [HuolalaTech/huolala-figma-mcp](https://github.com/HuolalaTech/huolala-figma-mcp) | Apache-2.0 | ~85 | MCP + skills | Figma to React, React Native, Kotlin |
| [southleft/figma-console-mcp-skills](https://github.com/southleft/figma-console-mcp-skills) | MIT | ~93 | 23 skills | includes a design parity check; needs its MCP |
| [Shades-Media-Group/PageRecast](https://github.com/Shades-Media-Group/PageRecast) | MIT | new | tool | page to Figma |
| [Yueyin-Tql/htmlToFigma](https://github.com/Yueyin-Tql/htmlToFigma) | MIT | ~10 | MCP | URL or HTML to Figma |

### DESIGN.md and design systems

| Project | License | Stars | Notes |
| --- | --- | --- | --- |
| [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | Apache-2.0 | ~8.6k | 6 skills bundled |
| [google-labs-code/design.md](https://github.com/google-labs-code/design.md) | Apache-2.0 | ~28k | DESIGN.md spec for agents |
| [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | MIT | ~123k | DESIGN.md files of known brands (reference only; do not ship a brand's look) |
| [bergside/awesome-design-skills](https://github.com/bergside/awesome-design-skills) | MIT | ~3.3k | 67 style skills |
| [plugin87/ux-ui-agent-skills](https://github.com/plugin87/ux-ui-agent-skills) | MIT | ~2.9k | 27 UX/UI skills that depend on repo-internal files: install that plugin whole instead of bundling |
| [Dragoon0x/prism-design-extractor](https://github.com/Dragoon0x/prism-design-extractor) | MIT | new | URL, screenshot or PDF to design artifacts |

### More clone templates and screenshot-to-code skills

| Project | License | Stars | Notes |
| --- | --- | --- | --- |
| [Mahanaicoach/ai-site-cloner](https://github.com/Mahanaicoach/ai-site-cloner) | MIT | ~20 | Claude, Codex and Copilot skills; `restyle` bundled |
| [UHolli/ai-website-cloner](https://github.com/UHolli/ai-website-cloner) | MIT | ~150 | derivative of JCodesMore's template |
| [samibajwaisking/website-cloner](https://github.com/samibajwaisking/website-cloner) | unclear | ~17 | single-HTML clone |
| [veyralabsgroup/webcloner](https://github.com/veyralabsgroup/webcloner) | none | ~8 | not bundled (no license) |
| [oil-oil/draw-ui](https://github.com/oil-oil/draw-ui) | none | ~510 | mockup and screenshot to code; not bundled |
| [zhu-guli326/image2_UI](https://github.com/zhu-guli326/image2_UI) | MIT | ~350 | Codex screenshot-to-UI (250 MB repo) |
| [aidenfausto/screenshot-to-modular-code](https://github.com/aidenfausto/screenshot-to-modular-code) | MIT | ~4 | |
| [zwq-top/ui-image-to-code-studio](https://github.com/zwq-top/ui-image-to-code-studio) | MIT | ~2 | bundled as `ui-image-to-code` |
| [mmohajer9/video-to-ui](https://github.com/mmohajer9/video-to-ui) | MIT | ~13 | bundled |
| [huanglvjing/spotpatch](https://github.com/huanglvjing/spotpatch) | MIT | ~130 | click an element, get its code path |
| [wandb/openui](https://github.com/wandb/openui) | Apache-2.0 | ~23k | app |
| [tldraw/make-real](https://github.com/tldraw/make-real) | none | ~5.4k | archived |

### Store screenshots (launch)

| Project | License | Stars | Notes |
| --- | --- | --- | --- |
| [ParthJadhav/app-store-screenshots](https://github.com/ParthJadhav/app-store-screenshots) | MIT | ~7.6k | bundled |
| [bitomule/Koubou](https://github.com/bitomule/Koubou) | MIT | ~210 | YAML to store screenshots, CLI + skill |
| [hypersocialinc/shots](https://github.com/hypersocialinc/shots) | none | ~250 | |
| [realZachi/shotluma](https://github.com/realZachi/shotluma) | MIT | ~150 | local editor |

### API documentation from your own traffic

Use only on **your own** app or an API you are authorized to document. For
anyone else's app the clean-room rule (no private APIs) applies.

| Project | License | Stars | Notes |
| --- | --- | --- | --- |
| [alufers/mitmproxy2swagger](https://github.com/alufers/mitmproxy2swagger) | not detected | ~9.7k | mitmproxy or HAR to OpenAPI |
| [jonluca/har-to-openapi](https://github.com/jonluca/har-to-openapi) | MIT | ~135 | HAR to OpenAPI |

### Page capture (own sites, archiving, offline study)

| Project | License | Stars |
| --- | --- | --- |
| [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) | Apache-2.0 | ~86k |
| [Y2Z/monolith](https://github.com/Y2Z/monolith) | CC0-1.0 | ~15.5k |
| [gildas-lormeau/SingleFile](https://github.com/gildas-lormeau/SingleFile) | AGPL-3.0 | ~22.7k |
| [website-scraper/node-website-scraper](https://github.com/website-scraper/node-website-scraper) | MIT | ~1.8k |
| [goclone-dev/goclone](https://github.com/goclone-dev/goclone) | MIT | ~2.3k |

### Finding more skills

[anthropics/skills](https://github.com/anthropics/skills),
[vercel-labs/skills](https://github.com/vercel-labs/skills) (skills.sh),
[skilld-dev/skilld](https://github.com/skilld-dev/skilld),
[LinklyAI/best-skills](https://github.com/LinklyAI/best-skills),
[ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills),
[VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills),
[hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code),
[travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills),
[BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills).

## Games, engines and 3D (added 2026-10-24)

MCP servers and skills that drive a game engine from Claude Code or Codex.
Verified via the GitHub API on 2026-10-24 (license, stars, last push). Agents
use these only if installed, for a `game` or `mashup` target, and only on the
user's own project; the clean-room rule still bars using another game's assets
or decompiled code.

### Godot

| Project | License | Stars | Type |
| --- | --- | --- | --- |
| [htdt/godogen](https://github.com/htdt/godogen) | MIT | ~7.2k | autonomous Godot dev for Claude Code and Codex |
| [Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp) | MIT | ~6.3k | MCP server |
| [hi-godot/godot-ai](https://github.com/hi-godot/godot-ai) | MIT | ~3.2k | MCP + AI tools |
| [jame581/GodotPrompter](https://github.com/jame581/GodotPrompter) | MIT | ~870 | skills for Godot 4.x |

### Unity

| Project | License | Stars | Type |
| --- | --- | --- | --- |
| [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp) | MIT | ~15k | MCP server (was justinpbarnett/unity-mcp) |
| [IvanMurzak/Unity-MCP](https://github.com/IvanMurzak/Unity-MCP) | Apache-2.0 | ~4.5k | MCP + skills + CLI |
| [Besty0728/Unity-Skills](https://github.com/Besty0728/Unity-Skills) | MIT | ~1.9k | skills |

### Unreal Engine

| Project | License | Stars | Type |
| --- | --- | --- | --- |
| [EpicGames/unreal-engine-skills-for-claude-code-plugin](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin) | MIT | ~1.6k | skills plugin (verify it is really Epic's org before trusting) |
| [ChiR24/Unreal_mcp](https://github.com/ChiR24/Unreal_mcp) | MIT | ~970 | MCP server + C++ plugin |
| [quodsoler/unreal-engine-skills](https://github.com/quodsoler/unreal-engine-skills) | MIT | ~400 | 27 C++ skills |

### Blender and Roblox

| Project | License | Stars | Type |
| --- | --- | --- | --- |
| [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) | MIT | ~32k | MCP server (now ahujasid/mcp-for-blender) |
| [EL4CTEO/blender-skills](https://github.com/EL4CTEO/blender-skills) | MIT | ~460 | Blender skills, Claude + Codex |
| [boshyxd/robloxstudio-mcp](https://github.com/boshyxd/robloxstudio-mcp) | MIT | ~500 | Roblox Studio MCP |
| [Chrrxs/robloxstudio-mcp](https://github.com/Chrrxs/robloxstudio-mcp) | MIT | ~330 | Roblox Studio MCP (active) |

### Multi-engine collections

| Project | License | Stars | Type |
| --- | --- | --- | --- |
| [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | MIT | ~27k | 49 agents + 72 skills |
| [gamedev-skills/awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) | Apache-2.0 | ~3.6k | 74 skills: Godot, Unity, Unreal, Phaser |

### Modding frameworks (owned games only)

For a game the user owns and records in `scope.md`. Not agent tools by
themselves; the agent writes mods against them.

| Project | License | Stars | Target |
| --- | --- | --- | --- |
| [UE4SS-RE/RE-UE4SS](https://github.com/UE4SS-RE/RE-UE4SS) | MIT | ~3.0k | Unreal games |
| [BepInEx/BepInEx](https://github.com/BepInEx/BepInEx) | LGPL-2.1 | ~8.9k | Unity / Mono games |
| [LaurieWired/GhidraMCP](https://github.com/LaurieWired/GhidraMCP) | Apache-2.0 | ~11.5k | native binaries (free Ghidra) |
