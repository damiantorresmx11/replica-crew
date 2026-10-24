# Ecosystem: open-source tools for AI app cloning (October 2026)

Every project below was checked against the GitHub API on 2026-10-23
(name, license, rounded stars). Replica Crew does **not** vendor them: each
agent uses one only if it is already installed, and only inside the
clean-room rules. Licenses and copyrights stay with their authors.

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

The recon agent may use these **only** when `replica/scope.md` records that
the user owns the software or holds written authorization (a legacy app
whose source was lost, an interoperability job you are licensed for). For
anyone else's app, the default clean-room rules apply: features and flows
from public sources, no decompiling, no private APIs.

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
