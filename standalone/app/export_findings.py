#!/usr/bin/env python3
"""Export findings to JSONL + optional chart PNG/SVG. No network."""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


def write_jsonl(rows: list[dict], dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return dest


def write_csv(rows: list[dict], dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    keys: list[str] = []
    for row in rows:
        for k in row:
            if k not in keys:
                keys.append(k)
    with dest.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    return dest


def chart_xy(points: list[tuple[float, float]], dest: Path, title: str = "finding") -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    dest.parent.mkdir(parents=True, exist_ok=True)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=140)
    ax.plot(xs, ys, color="#c5d0d8", linewidth=1.6)
    ax.set_title(title)
    ax.set_facecolor("#12161b")
    fig.patch.set_facecolor("#0b0d10")
    ax.tick_params(colors="#9aa7b4")
    ax.spines["bottom"].set_color("#24303a")
    ax.spines["left"].set_color("#24303a")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(dest)
    plt.close(fig)
    return dest


def bundle(name: str, rows: list[dict], out_dir: Path, points: list[tuple[float, float]] | None = None) -> dict:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = out_dir / f"{name}-{stamp}"
    out: dict = {"name": name, "utc": stamp}
    out["jsonl"] = str(write_jsonl(rows, Path(str(base) + ".jsonl")))
    out["csv"] = str(write_csv(rows, Path(str(base) + ".csv")))
    if points:
        out["png"] = str(chart_xy(points, Path(str(base) + ".png"), title=name))
        out["svg"] = str(chart_xy(points, Path(str(base) + ".svg"), title=name))
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--name", default="findings")
    p.add_argument("--in-json", required=True, help="JSON list of objects")
    p.add_argument("--out", default="out")
    p.add_argument("--x", help="numeric key for chart X")
    p.add_argument("--y", help="numeric key for chart Y")
    args = p.parse_args(argv)
    rows = json.loads(Path(args.in_json).read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise SystemExit("input must be a JSON list")
    points = None
    if args.x and args.y:
        points = [(float(r[args.x]), float(r[args.y])) for r in rows]
    print(json.dumps(bundle(args.name, rows, Path(args.out), points), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
