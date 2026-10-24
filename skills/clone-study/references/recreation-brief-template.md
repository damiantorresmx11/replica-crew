# Recreation brief — `<site-slug>`

Original URL: `<url>`
Captured: `<date>`
Workspace: `~/clone-study/<site-slug>/`

---

## 1. Stack decision

| Layer | Original (detected) | Recreation (chosen) | Reason |
|---|---|---|---|
| Framework | _e.g. Next.js 14_ | Vite + React (via scaffold) | Simpler dev loop; SSR not needed for a study build |
| Styling | _e.g. Tailwind_ | Tailwind v4 (scaffold default) | Match |
| Animation | _e.g. GSAP + Lenis_ | Framer Motion + Lenis | Framer is scaffold default; Lenis matches scroll feel |
| 3D | _e.g. R3F + custom shaders_ | _Skip / R3F + drei / R3F + custom shaders_ | _state honestly_ |

## 2. Design tokens

Drop this into `tailwind.config.ts` (extracted by `extract_tokens.py`):

```ts
// paste the `tailwind` subtree from tokens.json here
```

Notable details:
- Base spacing unit: `<n>px`
- Headline typography: `<family>` at `<size>/<weight>` with letter-spacing `<value>`
- Signature shadow / glow: `<box-shadow value>`
- Notable easing: `<cubic-bezier>` — this single curve carries a lot of the "feel"

## 3. Section breakdown

For each section, fill this block. Embed the screenshot inline.

### Section 1 — `<purpose, e.g. "Hero">`

![hero](raw-capture/scroll-states/scroll-00000.png)

- **Layout pattern**: split / stacked / grid-N / asymmetric / overlay
- **Viewport heights**: ~1.0
- **Notable elements**: oversized headline, magnetic CTA button, ambient background gradient
- **Entry animation**: text reveal (split by word, 60ms stagger, 900ms ease-out-cubic), CTA fades in 800ms after headline

### Section 2 — `<purpose>`
…

(Continue for every section.)

## 4. Animation spec

| ID | Section | Trigger | Target | Properties | Duration | Easing | Notes |
|---|---|---|---|---|---|---|---|
| hero-headline | 1 | load+200ms | `h1.hero` | translateY, opacity | 900ms | cubic-bezier(.16,1,.3,1) | split by word, 60ms stagger |
| nav-pill-magnet | header | hover | `nav a` | translate (cursor-tracked) | continuous | spring | strength 0.3 |
| feature-pin | 3 | scroll-pinned | `section.features` | progress 0→1 → background fades, card swap | 3vh pin | linear | Lenis required for smoothness |

## 5. Asset substitution

| Original | Type | Substituted with | Notes |
|---|---|---|---|
| `hero-bg.webp` | Photo | Unsplash — search "warm gradient minimal" | matched palette (#f5e6d3 → #c89b7b) |
| `Söhne` | Font | Inter (Google Fonts) | closest tone |
| `logo.svg` | Brand | placeholder wordmark "STUDIO" in Inter Bold | logo off-limits |

## 6. Copy direction

Original copy stays on the original site. Generate replacement copy in this tone:

- **Tone**: punchy / editorial / playful / corporate-cool / etc.
- **Audience**: who is this written for
- **Reading level**: short sentences vs. flowing paragraphs
- **Vocabulary cues**: what kind of words show up (e.g. "We don't do funnels. We do presence." style)

Replacement headlines should hit the same emotional beats as the original without copying phrasing.

## 7. Difficulty flags

Sections or features that may not match perfectly without manual work. Be honest.

- ⚠️ **Section 4 (3D scene)** — original uses a bespoke GLB with baked lighting. Substituting with Sketchfab model + drei `<Environment>`. Will look 70% as good, not 100%.
- ⚠️ **Custom cursor with audio** — flagged as out of scope for v1 build.
- ⚠️ **WebGL distortion on hover** — recreatable with R3F + custom fragment shader; budget extra time.

## 8. Build order

Build in this order to avoid getting stuck on hard sections early:

1. Scaffold + tokens applied
2. Section 1 (hero) without animations
3. All sections with static layout
4. Layer in animations section by section, easy → hard
5. Polish pass
6. Diff loop

This order means the user sees the full page taking shape before any deep animation work.
