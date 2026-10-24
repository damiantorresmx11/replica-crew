# Scroll-pinned timeline pattern

What every Awwwards-tier 3D site is actually doing under the hood, and how to build one in React + R3F without paying for the half-day of debugging the first time.

This is the *architecture* reference. For section-fade-only, smaller-budget builds, the regular vertical-page pattern is fine — use this only when the brief calls for "scroll-pinned timeline" as the narrative model.

## The mental model

A scroll-pinned timeline is **not a long page you scroll through**. It is a **long scroll runway** whose only job is to provide a 0..1 progress value. The visible viewport is **pinned** (sticky) inside that runway, and everything inside the viewport — camera, 3D objects, text moments — is driven by progress.

Sections become **moments** (timestamps with fade ranges), not boxes (positions in document flow). The "scroll" the user feels is the timeline scrubbing forward.

## File layout

```
src/
├── App.tsx                  -- runway + sticky viewport + section overlays
├── hooks/
│   └── useScrollProgress.ts -- RAF-throttled 0..1 scroll progress
├── lib/
│   └── timeline.ts          -- stages (opacity ranges) + waypoint tracks (camera/object)
├── components/
│   ├── Scene.tsx            -- R3F Canvas + CameraRig + lights + postprocess
│   └── LogoMark.tsx         -- 3D centerpiece, reads progress from props
└── sections/                -- one file per moment, takes `opacity: number` prop
    ├── Hero.tsx, Intro.tsx, Features.tsx, Specs.tsx, Order.tsx
```

## The four pieces

### 1. Scroll progress hook

RAF-throttle scroll updates so React doesn't render on every scroll event. Without this you'll get jank on long pages.

```ts
// hooks/useScrollProgress.ts
export function useScrollProgress(): number {
  const [progress, setProgress] = useState(0);
  useEffect(() => {
    let raf = 0;
    const update = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      setProgress(max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0);
    };
    const onScroll = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(update); };
    update();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  return progress;
}
```

### 2. Timeline definition

Every moment is a stage with `in / hold / out` (fade-in start, hold center, fade-out end). Every animated 3D property is a `Track` — an array of `[progress, value]` waypoints sampled with eased lerp.

```ts
// lib/timeline.ts
export type Stage = { id: string; in: number; hold: number; out: number };

export const STAGES = {
  hero:     { id: "hero",     in: 0.00, hold: 0.08, out: 0.16 },
  intro:    { id: "intro",    in: 0.18, hold: 0.28, out: 0.38 },
  features: { id: "features", in: 0.40, hold: 0.50, out: 0.60 },
  specs:    { id: "specs",    in: 0.62, hold: 0.72, out: 0.82 },
  order:    { id: "order",    in: 0.84, hold: 0.92, out: 1.00 },
} satisfies Record<string, Stage>;

export function stageOpacity(p: number, s: Stage): number {
  if (p < s.in || p > s.out) return 0;
  if (p < s.hold) return (p - s.in) / (s.hold - s.in);
  return 1 - (p - s.hold) / (s.out - s.hold);
}

type Track = Array<[number, number]>;
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const easeInOut = (t: number) => t < 0.5 ? 2*t*t : 1 - Math.pow(-2*t+2, 2)/2;

export function sample(track: Track, p: number): number {
  if (p <= track[0][0]) return track[0][1];
  if (p >= track.at(-1)![0]) return track.at(-1)![1];
  for (let i = 0; i < track.length - 1; i++) {
    const [pa, va] = track[i], [pb, vb] = track[i+1];
    if (p >= pa && p <= pb) return lerp(va, vb, easeInOut((p - pa) / (pb - pa)));
  }
  return track.at(-1)![1];
}
```

Then define your tracks: `CAM_Z`, `MARK_POS_X`, `MARK_ROT_Y`, `BLOOM`, etc. Sample them all in one `sampleTimeline(p)` function for ergonomics.

### 3. App layout — the sticky-inside-tall pattern

```tsx
const TIMELINE_VH = 600; // 5 viewport heights of scroll runway

export default function App() {
  const progress = useScrollProgress();
  return (
    <>
      <Scene progress={progress} />              {/* fixed inset-0 z-0 canvas */}
      <Header />
      <div style={{ height: `${TIMELINE_VH}vh` }} className="relative">
        <div className="sticky top-0 h-screen w-full overflow-hidden">
          <Hero     opacity={stageOpacity(progress, STAGES.hero)} />
          <Intro    opacity={stageOpacity(progress, STAGES.intro)} />
          {/* ...etc */}
        </div>
      </div>
      <Footer />
    </>
  );
}
```

The outer `div` provides the scroll budget. The inner `sticky top-0 h-screen` pins the viewport. Sections are `absolute inset-0` overlays inside that sticky container — only their opacity changes, never their position.

### 4. Section components

Plain absolute overlays driven by an opacity prop. **Do NOT add `transition: opacity 200ms` in CSS** (see traps below).

```tsx
export function Intro({ opacity }: { opacity: number }) {
  return (
    <section
      style={{ opacity }}
      className="absolute inset-0 flex items-center px-8 md:px-16 pointer-events-none"
    >
      {/* content */}
    </section>
  );
}
```

`pointer-events-none` is important — it lets the user scroll/drag through inactive sections without their text catching events.

### 5. The R3F scene

`CameraRig` reads progress and lerps the camera each frame. Same pattern for the 3D centerpiece.

```tsx
function CameraRig({ progress }: { progress: number }) {
  const { camera } = useThree();
  useFrame((_, dt) => {
    const { cam } = sampleTimeline(progress);
    const lerp = 1 - Math.pow(0.001, dt); // frame-rate-independent
    camera.position.x += (cam.x - camera.position.x) * lerp;
    camera.position.y += (cam.y - camera.position.y) * lerp;
    camera.position.z += (cam.z - camera.position.z) * lerp;
    camera.lookAt(0, 0, 0);
  });
  return null;
}
```

## Premium-look defaults that don't look "rough"

These are the values we landed on after iteration. If your bloom looks like a hot ring around the object, you have one of these wrong.

### Bloom

```tsx
import { Bloom, SMAA, EffectComposer, Vignette } from "@react-three/postprocessing";
import { KernelSize } from "postprocessing";

<EffectComposer multisampling={4}>
  <Bloom
    intensity={0.7}                    // total contribution; usually 0.5–1.6
    luminanceThreshold={0.18}          // low → glow rolls off across more of the image
    luminanceSmoothing={0.85}          // HIGH (0.8+) is critical — soft threshold, not crunchy
    radius={0.92}                      // wide diffuse halo
    kernelSize={KernelSize.HUGE}       // the single biggest visual upgrade — never use SMALL
    mipmapBlur                         // free quality boost
  />
  <SMAA />
  <Vignette eskil={false} offset={0.3} darkness={0.78} />
</EffectComposer>
```

### Materials (metal centerpiece)

Sharp chrome (`roughness 0.05–0.18`) creates razor-thin specular streaks that bloom into harsh ring artifacts. Bumping roughness alone fixes 80% of "rough" lighting complaints.

```tsx
<meshPhysicalMaterial
  color="#e8d6b8"            // slightly muted vs pure white — reads as warm gold
  metalness={1}
  roughness={0.32}           // NOT 0.18 — that's where the harsh edges come from
  clearcoat={0.4}
  clearcoatRoughness={0.45}
  reflectivity={0.7}
  envMapIntensity={0.95}     // 1.4+ blows out highlights and clips into bloom
/>
```

### Background canvas overlay

The whole canvas needs a subtle radial vignette to avoid the bright reflective surface running into hard viewport edges. Apply on the canvas wrapper, not in postprocess (cheaper):

```tsx
<div
  className="fixed inset-0 z-0 pointer-events-none after:content-[''] after:absolute after:inset-0 after:bg-[radial-gradient(ellipse_at_center,transparent_30%,rgba(12,7,3,0.55)_75%)] after:z-10"
>
  <Canvas>...</Canvas>
</div>
```

## Debugging traps we already paid for

Save yourself the half-day. These are non-obvious and each cost real time the first build.

### Trap 1: "Camera X offset doesn't visually displace the mark"

If your camera moves to `(1500, 0, 8000)` and `lookAt(0, 0, 0)`, the camera *rotates* to face the origin — the mark stays dead-center in the frame. Camera position only matters for distance and parallax, not screen-space placement.

**Fix**: move the **mark's position** instead of the camera. Add a `MARK_POS_X` / `MARK_POS_Y` track and apply it in the LogoMark's `useFrame`. Camera stays static or only dollies in Z.

### Trap 2: CSS opacity transitions cause ghost overlap

A `transition: opacity 200ms linear` on each section seems harmless until scroll velocity exceeds the transition duration — then you get TWO sections at opacity > 0 simultaneously, stacked on top of each other.

**Fix**: don't use CSS transitions for stage opacity. The React-state opacity is already smooth because the scroll progress hook is RAF-throttled. The "snappiness" of stages cutting in is actually correct — that's the cinema-cut feel. If you want softer transitions, widen the stage's `in`/`out` range so the `stageOpacity` math itself ramps over more progress space.

### Trap 3: Vite 7 + Node 20.18 → cryptic rolldown error

Vite 7 ships with rolldown which requires Node 20.19+ and pulls a `@rolldown/binding-darwin-*` native binary. Under Node 20.18 you get a multi-page error stack about a missing module that has nothing to do with what you actually broke.

**Fix**: pin Vite to ^5 and `@vitejs/plugin-react` to ^4 in the brief's stack decision. Tailwind v4's `@tailwindcss/vite` plugin is compatible with both. After scaffolding:

```bash
cd <project>
rm -rf node_modules package-lock.json
npm install -D vite@^5 @vitejs/plugin-react@^4
npm install
```

### Trap 4: Screenshot caught mid-transition → chasing phantom bugs

When verifying with `preview_screenshot`, if you screenshot immediately after `preview_eval` scrolls, the camera lerp + section opacities haven't settled yet. You'll see two sections overlapping or the mark in the wrong position and waste an hour debugging code that's actually correct.

**Fix**: `sleep 1.5` between scroll and screenshot. The lerp damping (`Math.pow(0.001, dt)`) reaches steady state in ~0.5–1s, plus you want the React render cycle to catch up.

### Trap 5: The full-page screenshot lies

For pinned-timeline sites, `page.screenshot({ fullPage: true })` captures the DOM rendering of a 60,000px tall page that's mostly empty (because all content lives inside the sticky h-screen). The capture script's `scroll-states/*.png` are what actually show the canvas state at each progress point. Use those to feed `visual_diff.py`, not the full-page PNG.

### Trap 6: `npm install --silent` skips optional native deps

Don't use `--silent` on the initial install for projects with native bindings (Vite, Sharp, esbuild, rollup binaries). The error suppression hides binary install failures and you only find out when `npm run dev` crashes. Plain `npm install` is fine.

## Verification cadence

When checking a pinned-timeline build, screenshot at each stage hold:

```js
// Run via preview_eval, then sleep 1.5s, then preview_screenshot
(() => {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  window.scrollTo(0, max * 0.28);  // intro hold
  return 'intro hold';
})()
```

Capture five frames: 0.0, 0.28, 0.5, 0.72, 0.92. That gives you a complete moment-by-moment view to compare against the original capture's scroll-states.

## When the brief is ambiguous

If you're not sure whether to use this pattern or a vertical-page layout: prefer pinned timeline if the original has any of these signals together: ≥3 stages with the same canvas centerpiece, scroll-driven camera animation, or a `.buf`/splat camera-track file in network log. Otherwise default to vertical-page — it's much cheaper to build and most "good" sites are actually that.
