# Animation and scroll behavior detection

Premium sites get most of their "wow" from animation. Catalog the animations carefully — this is what separates a clone that feels right from one that feels dead.

## How to observe

1. Watch `raw-capture/recording.webm` at **0.25× speed** in a video player. Important details (sub-100ms easings, stagger offsets) are invisible at full speed.
2. Step through `raw-capture/scroll-states/` images sequentially. Diff adjacent frames mentally to see what changes between scroll positions.
3. Cross-reference with `detected-globals.json` — if `gsap` and `ScrollTrigger` are present, scroll-pinned sections are likely.

## Trigger taxonomy

For each notable animation, classify the trigger:

- **load** — fires once on page load (hero entrance)
- **scroll-position** — fires when an element crosses a scroll threshold (most common)
- **scroll-velocity** — depends on scroll speed (skew, parallax, momentum-driven)
- **scroll-pinned** — element pins in place while scroll continues, with progress driving an internal animation (Apple-style)
- **hover** — pointer enter/leave
- **click** — pointer down
- **time** — runs continuously (orbiting elements, marquee)
- **cursor-track** — element follows or reacts to cursor position
- **viewport-resize** — rebuilds on resize

## Property taxonomy

What's actually changing? Common premium-site combinations:

- **Text reveals** — split into chars/words, animate `transform: translateY()` + `opacity` with stagger
- **Image reveals** — `clip-path: inset()` animating from full inset to zero
- **Card hover** — scale 1 → 1.03, shadow grows, subtle rotation, often with magnetic cursor pull
- **Parallax** — `transform: translateY()` driven by scroll position at different rates per layer
- **Pinned section storytelling** — scroll progress drives a timeline (text changes, images swap, 3D rotates)
- **Marquee** — infinite horizontal `transform: translateX()` with negative duration easing
- **Number counter** — `requestAnimationFrame` interpolating an integer
- **WebGL postprocess** — RGB shift, distortion intensified by scroll velocity

## Estimating timing

Frame-by-frame is the reliable way:
- Step the video by frames (most players: `,` and `.` keys)
- Note the frame number when an animation starts and ends
- Convert: at 30fps, frame_count × 33ms = duration

For scroll-driven animations, instead measure the scroll distance the animation occupies, not seconds.

## Easing identification

Capture's `computed-styles.json` includes `transition` declarations — easing curves often appear there literally as `cubic-bezier(0.16, 1, 0.3, 1)` or named (`ease-out-cubic`). For JS-driven animations (GSAP, Framer), the curve is in the bundle; estimate by feel:

- **Slow start, fast end** → ease-in (rare on premium sites; feels heavy)
- **Fast start, slow end** → ease-out (most common — feels responsive)
- **Slow start AND end** → ease-in-out (smooth but can feel sluggish)
- **Overshoot then settle** → spring physics (Framer Motion, GSAP back/elastic)
- **Linear** → never use for UI; only for marquees/loaders

## Output format

Add to `analysis.json`:

```json
{
  "animations": [
    {
      "id": "hero-text-reveal",
      "trigger": "load",
      "delay_ms": 200,
      "target": "h1.hero-title",
      "properties": ["translateY", "opacity"],
      "duration_ms": 900,
      "easing": "cubic-bezier(0.16, 1, 0.3, 1)",
      "notes": "split by word, 60ms stagger, starts after 200ms initial delay"
    },
    {
      "id": "feature-cards-pinned",
      "trigger": "scroll-pinned",
      "scroll_distance_px": 2400,
      "target": "section.features",
      "properties": ["card visibility cycles", "background-color"],
      "notes": "section pins for ~3 viewport heights; scroll progress 0→1 cycles through 4 cards with cross-fade"
    }
  ]
}
```

## What you're allowed to skip

If a section uses an animation that's clearly bespoke (custom shader doing fluid simulation, hand-tuned physics on draggable objects), document it but don't promise to recreate it 1:1. Mark it in the recreation brief under "Difficulty flags."
