"""Turn a run directory into publication figures.

Kept deliberately thin: read only from --run, write only to --out, so a figure
can always be traced back to the metrics.json that produced it.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description="export figures from a run directory")
    ap.add_argument("--run", required=True, help="directory holding metrics.json")
    ap.add_argument("--out", default="docs/figures")
    args = ap.parse_args()

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    run = Path(args.run)
    metrics = json.loads((run / "metrics.json").read_text(encoding="utf-8"))

    report = {k: v for k, v in metrics["report"].items() if isinstance(v, dict)}
    labels = sorted(report)
    f1 = [report[k]["f1-score"] for k in labels]

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(4, 3), dpi=300)
    ax.bar(labels, f1, color="0.35")
    ax.set_ylabel("F1 score")
    ax.set_ylim(0, 1)
    ax.set_title(f"seed={metrics['seed']}, n_test={metrics['n_test']}")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()

    for ext in ("png", "pdf"):
        path = out / f"per_class_f1.{ext}"
        fig.savefig(path)
        print(f"wrote {path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
