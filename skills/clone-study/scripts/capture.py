"""
Capture a target website systematically for clone-study analysis.

Usage:
    python capture.py <url> <output-dir> [--scroll-step 600] [--video-seconds 30]

Requires: pip install playwright && playwright install chromium

Outputs into <output-dir>/raw-capture/:
    desktop-full.png, tablet-full.png, mobile-full.png
    scroll-states/scroll-<y>.png       (every --scroll-step pixels)
    recording.webm                     (automated scroll-through)
    dom-snapshot.html                  (post-hydration DOM)
    network-log.json                   (every request: url, type, size, status)
    computed-styles.json               (visible elements' computed styles)
    console-log.txt
    fonts.json                         (loaded font faces)
    detected-globals.json              (window.THREE, gsap, Lenis, etc.)
    performance.json                   (paint timing)
"""

import argparse
import asyncio
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright

VIEWPORTS = [
    ("desktop", 1920, 1080),
    ("tablet", 768, 1024),
    ("mobile", 390, 844),
]

# Globals to probe for on the page after load — common premium-site libraries.
LIBRARY_PROBES = [
    "THREE", "gsap", "Lenis", "ScrollTrigger", "Lottie", "lottie",
    "motion", "Splitting", "barba", "Locomotive", "Hey",
    "__NEXT_DATA__", "__NUXT__", "$nuxt",
]


def slugify(url: str) -> str:
    parsed = urlparse(url)
    base = (parsed.netloc + parsed.path).strip("/")
    return re.sub(r"[^a-z0-9-]+", "-", base.lower()).strip("-") or "site"


async def capture(url: str, out_dir: Path, scroll_step: int, video_seconds: int):
    raw = out_dir / "raw-capture"
    (raw / "scroll-states").mkdir(parents=True, exist_ok=True)

    network_log = []
    console_log = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Recording context — desktop viewport, video on.
        rec_context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(raw),
            record_video_size={"width": 1920, "height": 1080},
        )
        rec_page = await rec_context.new_page()

        rec_page.on("console", lambda msg: console_log.append(f"[{msg.type}] {msg.text}"))
        rec_page.on("response", lambda r: network_log.append({
            "url": r.url,
            "status": r.status,
            "type": r.headers.get("content-type", ""),
            "size": int(r.headers.get("content-length", 0) or 0),
        }))

        await rec_page.goto(url, wait_until="networkidle", timeout=60_000)
        await rec_page.wait_for_timeout(2000)  # let entrance animations settle

        # 1. DOM snapshot
        dom = await rec_page.content()
        (raw / "dom-snapshot.html").write_text(dom, encoding="utf-8")

        # 2. Library/global detection
        detected = await rec_page.evaluate(
            """(probes) => {
                const out = {};
                for (const k of probes) {
                    try { out[k] = typeof window[k] !== 'undefined'; }
                    catch (e) { out[k] = false; }
                }
                return out;
            }""",
            LIBRARY_PROBES,
        )
        (raw / "detected-globals.json").write_text(json.dumps(detected, indent=2))

        # 3. Loaded fonts
        fonts = await rec_page.evaluate("""() => {
            const out = [];
            for (const f of document.fonts) {
                if (f.status === 'loaded') {
                    out.push({ family: f.family, weight: f.weight, style: f.style });
                }
            }
            return out;
        }""")
        (raw / "fonts.json").write_text(json.dumps(fonts, indent=2))

        # 4. Computed styles for visible text + interactive elements
        styles = await rec_page.evaluate("""() => {
            const interesting = document.querySelectorAll(
                'h1, h2, h3, h4, p, a, button, [role="button"], li, span'
            );
            const out = [];
            const limit = Math.min(interesting.length, 400);
            for (let i = 0; i < limit; i++) {
                const el = interesting[i];
                const cs = getComputedStyle(el);
                const r = el.getBoundingClientRect();
                if (r.width === 0 || r.height === 0) continue;
                out.push({
                    tag: el.tagName.toLowerCase(),
                    text: (el.innerText || '').slice(0, 60),
                    fontFamily: cs.fontFamily,
                    fontSize: cs.fontSize,
                    fontWeight: cs.fontWeight,
                    lineHeight: cs.lineHeight,
                    letterSpacing: cs.letterSpacing,
                    color: cs.color,
                    background: cs.backgroundColor,
                    padding: cs.padding,
                    margin: cs.margin,
                    borderRadius: cs.borderRadius,
                    boxShadow: cs.boxShadow,
                    transition: cs.transition,
                });
            }
            return out;
        }""")
        (raw / "computed-styles.json").write_text(json.dumps(styles, indent=2))

        # 5. Performance timing
        perf = await rec_page.evaluate("""() => {
            const out = { paint: [], navigation: null };
            for (const entry of performance.getEntriesByType('paint')) {
                out.paint.push({ name: entry.name, startTime: entry.startTime });
            }
            const nav = performance.getEntriesByType('navigation')[0];
            if (nav) out.navigation = { domContentLoaded: nav.domContentLoadedEventEnd, load: nav.loadEventEnd };
            return out;
        }""")
        (raw / "performance.json").write_text(json.dumps(perf, indent=2))

        # 6. Scroll-state screenshots + record video by scrolling
        page_height = await rec_page.evaluate("document.body.scrollHeight")
        scroll_y = 0
        idx = 0
        scroll_duration_ms = max(video_seconds * 1000, 5000)
        steps = max(1, page_height // scroll_step)
        per_step_ms = scroll_duration_ms // steps

        while scroll_y < page_height:
            await rec_page.evaluate(f"window.scrollTo({{ top: {scroll_y}, behavior: 'instant' }})")
            await rec_page.wait_for_timeout(per_step_ms)
            await rec_page.screenshot(
                path=str(raw / "scroll-states" / f"scroll-{scroll_y:05d}.png"),
                full_page=False,
            )
            scroll_y += scroll_step
            idx += 1

        # 7. Full-page screenshots at each viewport (in fresh contexts to avoid scroll state)
        await rec_context.close()  # finalizes the video

        for name, w, h in VIEWPORTS:
            ctx = await browser.new_context(viewport={"width": w, "height": h})
            page = await ctx.new_page()
            await page.goto(url, wait_until="networkidle", timeout=60_000)
            await page.wait_for_timeout(1500)
            await page.screenshot(path=str(raw / f"{name}-full.png"), full_page=True)
            await ctx.close()

        await browser.close()

    # 8. Persist network + console logs
    (raw / "network-log.json").write_text(json.dumps(network_log, indent=2))
    (raw / "console-log.txt").write_text("\n".join(console_log))

    # Rename the video to recording.webm
    videos = list(raw.glob("*.webm"))
    if videos:
        videos[0].rename(raw / "recording.webm")
        for extra in videos[1:]:
            extra.unlink()

    print(f"Capture complete: {raw}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("output_dir", help="Workspace dir; raw-capture/ created inside")
    parser.add_argument("--scroll-step", type=int, default=600)
    parser.add_argument("--video-seconds", type=int, default=30)
    args = parser.parse_args()

    out_dir = Path(args.output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    asyncio.run(capture(args.url, out_dir, args.scroll_step, args.video_seconds))


if __name__ == "__main__":
    main()
