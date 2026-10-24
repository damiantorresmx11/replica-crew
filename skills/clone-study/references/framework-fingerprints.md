# Framework and library fingerprints

How to identify what stack a target site is built on, from data captured by `scripts/capture.py`. Confidence matters more than certainty — record what you saw and how strong the signal was.

## Top-level frameworks

| Framework | Strong signals | Weak signals |
|---|---|---|
| **Next.js** | `<script id="__NEXT_DATA__">` in DOM, `_next/static/` in network log, `__next` div wrapper | `next/font` CSS class names, hydration warnings in console |
| **Nuxt** | `window.__NUXT__`, `__nuxt` div, `_nuxt/` in network paths | Vue devtools hint in console |
| **Astro** | `data-astro-cid-*` attributes on elements, `_astro/` chunks | Minimal JS, mostly static HTML |
| **SvelteKit** | `data-sveltekit-*` attributes, `_app/immutable/` chunks | `data-svelte-h` markers |
| **Remix** | `__remixContext` global, `data-remix-route` | Loader functions in network |
| **Plain Vite + React** | `assets/index-<hash>.js`, no framework data | React devtools available, no SSR markup |
| **Webflow** | `data-wf-page` attribute, `webflow.js` in scripts | Lots of `.w-*` class names |
| **Framer (sites)** | `framerusercontent.com` assets, `data-framer-*` | |

## Animation libraries

| Library | Strong signals |
|---|---|
| **GSAP** | `window.gsap` truthy, `gsap.min.js` in network, `gsap-*` classes |
| **GSAP ScrollTrigger** | `window.ScrollTrigger`, `pin-spacer` divs in DOM |
| **Framer Motion** | `motion-*` data attributes, transform style with will-change |
| **Motion One** | `motion.dev` script source, smaller footprint than Framer |
| **Lenis** (smooth scroll) | `window.Lenis`, `html.lenis` class, `lenis-*` classes on `<html>` |
| **Locomotive Scroll** | `data-scroll-container`, `data-scroll-section` attrs |
| **Lottie** | `lottie.js` script, `<svg>` with sequential `<g>` transformations |
| **SplitType / Splitting** | `<span>` per character/word in headings with `splitting`/`split-line` classes |

## 3D / WebGL

| Library | Strong signals |
|---|---|
| **Three.js** (vanilla) | `window.THREE`, `<canvas>` with `webgl`/`webgl2` context, no React |
| **React Three Fiber** | `r3f-*` data attributes, `<Canvas>` wrapper detectable in DevTools |
| **OGL** | smaller bundle, `ogl` in chunk filenames |
| **PixiJS** | `pixi.min.js`, 2D-only canvas |
| **Spline** | `spline-viewer` custom element, `prod.spline.design` URLs |

## Styling approach

| Approach | Signals |
|---|---|
| **Tailwind** | Many utility classes per element (`flex items-center justify-between gap-4 text-sm font-medium`), no other CSS class noise |
| **CSS Modules** | Class names like `Header_logo__a3Bx9` (component name + name + hash) |
| **styled-components / Emotion** | Class names like `sc-jSUZER`, `css-1abc234` |
| **Vanilla CSS / SCSS** | Semantic class names without hashes |
| **CSS-in-JS at build** (Vanilla Extract, Panda) | Hashed class names but with readable prefixes |

## Heuristics

- **Bundle filenames are gold.** A network log entry like `/_next/static/chunks/framework-abc123.js` instantly resolves framework + version family.
- **Console warnings often spill the framework.** "Hydration mismatch" → React-based SSR. "Vue warn" → Vue family.
- **The DOM root element pattern is distinctive.** `<div id="__next">`, `<div id="__nuxt">`, `<astro-island>`, `<div id="root">` (Vite plain).
- **Prefer specific over general.** "Next.js" beats "React app." Saying "probably 14.x" beats "Next.js."

## Output format

Add to `analysis.json`:

```json
{
  "stack": {
    "framework": { "name": "Next.js", "version_guess": "14", "confidence": "high" },
    "styling": { "name": "Tailwind", "confidence": "high" },
    "animation": [
      { "name": "GSAP", "confidence": "high" },
      { "name": "Lenis", "confidence": "medium" }
    ],
    "3d": [],
    "evidence": [
      "<script id=\"__NEXT_DATA__\"> present",
      "/_next/static/chunks/framework-...js in network log",
      "window.gsap is defined",
      "html element has class 'lenis lenis-smooth'"
    ]
  }
}
```
