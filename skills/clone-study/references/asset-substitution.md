# Asset substitution playbook

Original assets stay on the original site. The recreation uses substitutes. This is non-negotiable for ethical, legal, and practical reasons (the user is making a public video — using Lusion's bespoke 3D model in a clone is a real problem).

The good news: substitution rarely hurts the recreation's quality if you choose carefully.

## Substitution table by asset type

### Fonts

| If original uses... | Substitute with... |
|---|---|
| Custom foundry font (Pangram Pangram, GT, Klim) | Closest Google Font: GT Walsheim → **Inter** or **General Sans** (Fontshare); GT Sectra → **Fraunces**; Söhne → **Inter** |
| Adobe Fonts (Typekit) | Google Fonts equivalent or **Fontshare** (free for commercial use) |
| Variable display font | **Hubot Sans**, **Mona Sans**, **Inter Variable** — all free and high quality |
| Serif editorial | **Fraunces**, **Playfair Display**, **Crimson Pro** |
| Mono / technical | **JetBrains Mono**, **IBM Plex Mono**, **Geist Mono** |

Fontshare (https://www.fontshare.com) is your best friend — most look "premium" and are licensed for commercial use.

### Photography

| If original uses... | Substitute with... |
|---|---|
| Brand photography (people, products) | **Unsplash** (https://unsplash.com), **Pexels**, or generate with image AI matching the original's color/mood |
| Stock photos | Unsplash equivalent, search by mood not subject |
| Editorial product shots | Unsplash or generated; keep similar composition and lighting |
| Founder/team headshots | **Generated.photos** for placeholder humans, or "person silhouette" placeholders |

When using Unsplash images, prefer ones from the same general mood/palette as the original. Color matching matters more than subject matching.

### Iconography

| If original uses... | Substitute with... |
|---|---|
| Custom icon set | **Lucide** (default in scaffold), **Tabler Icons**, **Phosphor** |
| Heroicons / Feather | Lucide (already in scaffold) |
| Animated icons | Lucide + Framer Motion, or **Lordicon** (free tier) |

### 3D models (.glb, .gltf)

| If original uses... | Substitute with... |
|---|---|
| Bespoke product 3D | **Sketchfab** (filter to free + CC), **Poly Haven** for environments |
| Generic shapes (sphere, torus) | Build from primitives in three.js — no asset needed |
| Character models | Mixamo (free with Adobe account), or stylized placeholder |
| Environment / scene | **Poly Haven** (CC0), **Quaternius** (CC0) |

### 3D Gaussian splats (`.splat`, `.ply`, `SplatsWorker.js`, custom `.buf`)

Splat-rendered hero objects (Lusion's coaster, photoreal product scans) need source capture data you don't have. Three viable substitutes, ranked best to worst for the *hero centerpiece* role:

1. **User's SVG logo → ExtrudeGeometry** — if the user has any vector mark (logo, monogram, custom glyph), this is by far the strongest swap. Three.js `SVGLoader` + `ExtrudeGeometry` produces a beveled 3D solid that looks Lusion-tier under the right material + bloom (see scroll-pinned-timeline reference for premium defaults). Bonus: it's user-owned IP, no licensing footnote needed, and the "we extruded the brand mark" angle is great video material. The first build of this skill used this exact swap to recreate a splat-based site convincingly.
2. **User scans the substitute themselves** — Polycam (iOS/Android, free tier) does a Gaussian splat scan in 5 minutes from a phone walkaround. Best for "real product" recreations where extruded vector wouldn't fit (e.g., the original is a physical object, not a brand mark). Render with `<Splat>` from `@react-three/drei`.
3. **Free public splat** — Sketchfab now has a "Gaussian Splatting" filter; Polycam Explore and Luma's gallery have public CC splats. Lower ownership/relatability but lowest effort.

If the 3D is truly the centerpiece (Bruno Simon's drivable car, a custom papercraft world), the recreation can't be faithful even with these substitutes — note this explicitly in the brief and pick a different target unless the user accepts the gap.

### Lottie / animation JSON

| If original uses... | Substitute with... |
|---|---|
| Custom Lottie | **LottieFiles** (https://lottiefiles.com) free tier, search by mood |
| After Effects export | LottieFiles equivalent |

### Video / audio

| If original uses... | Substitute with... |
|---|---|
| Brand video clips | **Pexels Videos** (CC), **Coverr** |
| Background loops | Generate procedural video (gradient + noise) or Pexels |
| Audio cues | **Freesound.org** (CC), generate with web audio API |

### Logos

The brand's actual logo is off-limits. Either:
- Use a **placeholder wordmark** in the same typography family ("STUDIO", "AGENCY", a fictional brand)
- Generate a simple geometric mark in the same general style (3-letter monogram, abstract symbol)

## Color matching

When substituting, match the **color** of the original asset more carefully than the subject. A clone that uses Unsplash photos in the same palette as the original feels much closer than one with subject-matched but tonally different photos.

Use the extracted palette from `tokens.json` to filter substitutes — Unsplash supports color search.

## Recording the substitutions

Every substitution goes into the recreation brief's asset table:

| Original (location) | Type | Substituted with | Notes |
|---|---|---|---|
| `hero-image.webp` | Photography | Unsplash photo by Annie Spratt — `unsplash.com/photos/abc123` | Matched palette: warm earth tones |
| `Custom display font "Söhne Buch"` | Font | Inter via Google Fonts | Closest free equivalent in tone |
| `model.glb` (3D vase) | 3D model | Built from primitive cylinder in R3F | Original was bespoke; recreated geometry |

This table also feeds the teardown doc — viewers want to know what was swapped.
