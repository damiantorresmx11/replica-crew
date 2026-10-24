# Third-party notices

Replica Crew bundles skills from other open-source projects. Each bundled
folder keeps its original license as `LICENSE.upstream` and its source and
commit in `UPSTREAM.md`. Copyright stays with the original authors.

| folder | source | license | changes |
| --- | --- | --- | --- |
| `skills/replica-*` (11) | [Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill) | MIT | unmodified; copyright line in `LICENSE` |
| `skills/app-store-screenshots` | [ParthJadhav/app-store-screenshots](https://github.com/ParthJadhav/app-store-screenshots) | MIT | unmodified |
| `skills/clone-study` | [luukalleman/clone-study](https://github.com/luukalleman/clone-study) | MIT | unmodified |
| `skills/clone-team` | [Varalix-Digitech-Solutions/clone-team](https://github.com/Varalix-Digitech-Solutions/clone-team) | MIT | unmodified |
| `skills/clone-website` | [JCodesMore/ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template) | MIT | unmodified |
| `skills/design-md` | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | Apache-2.0 | unmodified |
| `skills/design-mirror` | [brightdata/skills](https://github.com/brightdata/skills) | MIT | unmodified |
| `skills/restyle` | [Mahanaicoach/ai-site-cloner](https://github.com/Mahanaicoach/ai-site-cloner) | MIT | unmodified |
| `skills/shadcn-ui` | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | Apache-2.0 | unmodified |
| `skills/site-md` | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | Apache-2.0 | unmodified |
| `skills/stitch-extract-design-md` | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | Apache-2.0 | modified (name only) |
| `skills/stitch-extract-static-html` | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | Apache-2.0 | modified (name only) |
| `skills/stitch-react-components` | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | Apache-2.0 | modified (name only) |
| `skills/ui-image-to-code` | [zwq-top/ui-image-to-code-studio](https://github.com/zwq-top/ui-image-to-code-studio) | MIT | unmodified |
| `skills/video-to-ui` | [mmohajer9/video-to-ui](https://github.com/mmohajer9/video-to-ui) | MIT | modified (nested plugin manifest removed) |
| `skills/web-clone` | [Jane-xiaoer/claude-skill-web-clone](https://github.com/Jane-xiaoer/claude-skill-web-clone) | MIT | unmodified |

Projects that are full applications, libraries or MCP servers are **not**
bundled. They are listed with links in `docs/ECOSYSTEM.md`, and the free
browser MCP servers can be added with `python scripts/install.py --mcp`.

`skills/clone-team/scripts/usage-watchdog.mjs` (upstream) reads your local
Claude Code OAuth token to poll Anthropic's own usage endpoint
(`api.anthropic.com`). It only runs if the clone-team Manager starts it.
