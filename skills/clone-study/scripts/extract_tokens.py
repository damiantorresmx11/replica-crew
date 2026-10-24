"""
Extract design tokens from a clone-study capture.

Usage:
    python extract_tokens.py <capture-dir>

Reads <capture-dir>/raw-capture/{computed-styles.json, fonts.json, *-full.png}
Outputs <capture-dir>/tokens.json — structured tokens, plus a Tailwind-config-shaped
'tailwind' subtree ready to drop into the recreation project.
"""

import argparse
import json
import re
from collections import Counter
from pathlib import Path


def parse_color(s: str):
    """Return (r,g,b) from rgb()/rgba() strings, else None."""
    m = re.match(r"rgba?\(([^)]+)\)", s or "")
    if not m:
        return None
    parts = [p.strip() for p in m.group(1).split(",")]
    try:
        r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
        a = float(parts[3]) if len(parts) > 3 else 1.0
        if a < 0.05:
            return None
        return (r, g, b)
    except (ValueError, IndexError):
        return None


def to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def parse_px(s: str):
    m = re.match(r"(-?\d*\.?\d+)px", s or "")
    return float(m.group(1)) if m else None


def cluster_colors(colors, max_distance=20):
    """Greedy color clustering — group colors within max_distance euclidean."""
    clusters = []
    for c, count in Counter(colors).most_common():
        placed = False
        for cluster in clusters:
            cr, cg, cb = cluster["centroid"]
            if abs(cr - c[0]) + abs(cg - c[1]) + abs(cb - c[2]) <= max_distance:
                cluster["count"] += count
                cluster["members"].append(c)
                placed = True
                break
        if not placed:
            clusters.append({"centroid": c, "count": count, "members": [c]})
    clusters.sort(key=lambda x: -x["count"])
    return clusters


def extract(capture_dir: Path):
    raw = capture_dir / "raw-capture"
    styles = json.loads((raw / "computed-styles.json").read_text())
    fonts = json.loads((raw / "fonts.json").read_text())

    # ─── Colors ──────────────────────────────────────────────────────
    fg_colors, bg_colors = [], []
    for s in styles:
        c = parse_color(s.get("color", ""))
        if c:
            fg_colors.append(c)
        b = parse_color(s.get("background", ""))
        if b:
            bg_colors.append(b)

    fg_clusters = cluster_colors(fg_colors)[:8]
    bg_clusters = cluster_colors(bg_colors)[:8]

    palette = {
        "text": [to_hex(c["centroid"]) for c in fg_clusters],
        "background": [to_hex(c["centroid"]) for c in bg_clusters],
    }

    # ─── Typography ──────────────────────────────────────────────────
    type_combos = Counter()
    families = Counter()
    sizes = Counter()
    weights = Counter()
    for s in styles:
        fam = (s.get("fontFamily") or "").split(",")[0].strip().strip('"\'')
        sz = parse_px(s.get("fontSize", ""))
        wt = s.get("fontWeight", "")
        if fam and sz:
            type_combos[(fam, round(sz), wt)] += 1
            families[fam] += 1
            sizes[round(sz)] += 1
            weights[wt] += 1

    typography = {
        "families": [f for f, _ in families.most_common(5)],
        "sizes": sorted({s for s, _ in sizes.most_common(8)}),
        "weights": [w for w, _ in weights.most_common(5)],
        "loaded_fonts": fonts,
        "top_combinations": [
            {"family": f, "size_px": sz, "weight": w, "count": c}
            for (f, sz, w), c in type_combos.most_common(10)
        ],
    }

    # ─── Spacing ─────────────────────────────────────────────────────
    spacing_values = Counter()
    for s in styles:
        for prop in ("padding", "margin"):
            for token in (s.get(prop) or "").split():
                v = parse_px(token)
                if v and v > 0:
                    spacing_values[round(v)] += 1
    spacing = sorted({v for v, _ in spacing_values.most_common(12)})

    # Detect base unit (gcd-ish: most common small divisor)
    base_unit = None
    for candidate in (4, 8, 6, 5):
        if all(v % candidate == 0 for v in spacing if v <= 64):
            base_unit = candidate
            break

    # ─── Border radius ───────────────────────────────────────────────
    radii = Counter()
    for s in styles:
        v = parse_px(s.get("borderRadius", ""))
        if v is not None:
            radii[round(v)] += 1
    radius_scale = sorted({v for v, _ in radii.most_common(6)})

    # ─── Shadows ─────────────────────────────────────────────────────
    shadows = Counter()
    for s in styles:
        sh = (s.get("boxShadow") or "").strip()
        if sh and sh != "none":
            shadows[sh] += 1
    top_shadows = [sh for sh, _ in shadows.most_common(5)]

    # ─── Easing curves from transition declarations ─────────────────
    easings = Counter()
    for s in styles:
        for match in re.finditer(r"cubic-bezier\([^)]+\)|ease[-a-z]*", s.get("transition") or ""):
            easings[match.group(0)] += 1
    top_easings = [e for e, _ in easings.most_common(5)]

    # ─── Tailwind-shaped output ──────────────────────────────────────
    tailwind = {
        "theme": {
            "extend": {
                "colors": {
                    "ink": palette["text"][0] if palette["text"] else "#0a0a0a",
                    "surface": palette["background"][0] if palette["background"] else "#ffffff",
                    "muted": palette["text"][1] if len(palette["text"]) > 1 else "#666666",
                    "accent": next(
                        (c for c in palette["text"] + palette["background"]
                         if c not in ("#000000", "#ffffff", "#0a0a0a")),
                        "#000000",
                    ),
                },
                "fontFamily": {
                    "display": typography["families"][:1] or ["sans-serif"],
                    "body": typography["families"][1:2] or typography["families"][:1] or ["sans-serif"],
                },
                "fontSize": {f"t{i}": f"{sz / 16}rem" for i, sz in enumerate(typography["sizes"])},
                "borderRadius": {f"r{i}": f"{v}px" for i, v in enumerate(radius_scale)},
                "boxShadow": {f"s{i}": sh for i, sh in enumerate(top_shadows)},
                "transitionTimingFunction": {f"e{i}": e for i, e in enumerate(top_easings)},
            }
        }
    }

    out = {
        "palette": palette,
        "typography": typography,
        "spacing": {"values_px": spacing, "base_unit_px": base_unit},
        "radius_px": radius_scale,
        "shadows": top_shadows,
        "easings": top_easings,
        "tailwind": tailwind,
    }
    (capture_dir / "tokens.json").write_text(json.dumps(out, indent=2))
    print(f"Tokens written: {capture_dir / 'tokens.json'}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("capture_dir")
    args = parser.parse_args()
    extract(Path(args.capture_dir).expanduser().resolve())


if __name__ == "__main__":
    main()
