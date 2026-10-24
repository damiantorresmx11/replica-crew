"""
Compare a recreation's screenshots against the original capture.

Usage:
    python visual_diff.py <original-capture-dir> <current-capture-dir> <output-dir>

Both capture dirs must contain {desktop,tablet,mobile}-full.png at the top level
(or under raw-capture/ — script will look in both places).

Outputs into <output-dir>:
    diff-desktop.png, diff-tablet.png, diff-mobile.png   (side-by-side + heatmap)
    diff-report.json                                      (per-viewport scores + section breakdown)
    diff-report.md                                        (human-readable summary with fix priorities)

Requires: pip install pillow numpy
"""

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def find_screenshot(directory: Path, viewport: str) -> Path | None:
    for candidate in (directory / f"{viewport}-full.png", directory / "raw-capture" / f"{viewport}-full.png"):
        if candidate.exists():
            return candidate
    return None


def diff_pair(original: Path, current: Path, out_path: Path):
    a = Image.open(original).convert("RGB")
    b = Image.open(current).convert("RGB")

    # Resize 'b' to match 'a' for a fair structural comparison.
    if a.size != b.size:
        b = b.resize(a.size)

    arr_a = np.asarray(a, dtype=np.int16)
    arr_b = np.asarray(b, dtype=np.int16)
    delta = np.abs(arr_a - arr_b).mean(axis=2)  # per-pixel mean channel diff

    # Score: mean diff normalized to 0–100 (lower is better).
    score = float(delta.mean()) / 255.0 * 100.0

    # Heatmap (red = high diff)
    heat = np.zeros((*delta.shape, 3), dtype=np.uint8)
    heat[..., 0] = np.clip(delta * 4, 0, 255).astype(np.uint8)
    heat_img = Image.fromarray(heat)

    # Section-wise breakdown — split into 8 vertical bands
    bands = 8
    band_h = delta.shape[0] // bands
    section_scores = []
    for i in range(bands):
        band = delta[i * band_h : (i + 1) * band_h]
        section_scores.append({
            "band": i,
            "y_range": [i * band_h, (i + 1) * band_h],
            "score": float(band.mean()) / 255.0 * 100.0,
        })

    # Side-by-side composite: original | current | heatmap
    w, h = a.size
    composite = Image.new("RGB", (w * 3, h), "white")
    composite.paste(a, (0, 0))
    composite.paste(b, (w, 0))
    composite.paste(heat_img, (w * 2, 0))
    composite.thumbnail((4000, 4000))  # cap output size
    composite.save(out_path)

    return {"overall_score": score, "sections": section_scores}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("original_dir")
    parser.add_argument("current_dir")
    parser.add_argument("output_dir")
    args = parser.parse_args()

    orig = Path(args.original_dir).expanduser().resolve()
    curr = Path(args.current_dir).expanduser().resolve()
    out = Path(args.output_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    viewports: dict = {}
    for vp in ("desktop", "tablet", "mobile"):
        a = find_screenshot(orig, vp)
        b = find_screenshot(curr, vp)
        if not a or not b:
            viewports[vp] = {"error": f"missing screenshot ({a=}, {b=})"}
            continue
        viewports[vp] = diff_pair(a, b, out / f"diff-{vp}.png")

    scored = [v["overall_score"] for v in viewports.values() if "overall_score" in v]
    report: dict = {
        "viewports": viewports,
        "overall": float(np.mean(scored)) if scored else None,
    }

    (out / "diff-report.json").write_text(json.dumps(report, indent=2))

    # Markdown summary with prioritized worst bands
    lines = ["# Visual diff report", ""]
    lines.append(f"**Overall mean diff:** {report['overall']:.2f} / 100 (lower is better)" if report["overall"] is not None else "_no comparable viewports_")
    lines.append("")
    for vp, data in report["viewports"].items():
        if "error" in data:
            lines.append(f"## {vp}: {data['error']}")
            continue
        lines.append(f"## {vp} — overall {data['overall_score']:.2f}")
        worst = sorted(data["sections"], key=lambda s: -s["score"])[:3]
        lines.append("**Worst-matching bands** (focus fixes here):")
        for b in worst:
            lines.append(f"- y={b['y_range'][0]}–{b['y_range'][1]}: {b['score']:.2f}")
        lines.append("")
    (out / "diff-report.md").write_text("\n".join(lines))
    print(f"Diff report written: {out}")


if __name__ == "__main__":
    main()
